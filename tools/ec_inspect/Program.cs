// Standalone inspector for Enhanced Client UOP files.
// Run: dotnet run --project tools/ec_inspect -- "<EC folder path>"

using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Text;

string ecPath = args.Length > 0 ? args[0] : @"C:\Games\Electronic Arts\Ultima Online Enhanced";

string[] files =
{
    "LegacyTexture.uop",
    "LegacyTerrain.uop",
    "Texture.uop",
    "TerrainTexture.uop",
    "TerrainDefinition.uop",
    "GameData.uop",
    "AnimationDefinition.uop",
    "AnimationSequence.uop",
    "AnimationFrame1.uop",
};

string[][] candidatePatternsByFile =
{
    new[] {
        "build/legacytexture/{0:D8}.dds", "build/legacytexture/{0}.dds", "build/legacytexture/{0:X8}.dds",
        "build/legacytexture/{0:D6}.dds", "build/legacytexture/{0:D8}_0.dds", "build/legacytexture/{0:D8}.tga",
        "build/legacytexture/{0:D8}.bin",
        "legacytexture/{0:D8}.dds", "legacytexture/{0}.dds",
        "build/legacytexture/{0:D8}/0.dds",
        "build/legacytexture/{0:D6}/{0:D2}.dds",
        "build/texture/{0:D8}.dds"
    },
    new[] {
        "build/legacyterrain/{0:D8}.bin", "build/legacyterrain/{0}.bin", "build/legacyterrain/{0:X8}.bin",
        "build/legacyterrain/{0:D8}.xml", "build/legacyterrain/{0}.xml",
        "build/legacyterrain/{0:D8}.dat",
        "legacyterrain/{0:D8}.bin",
        "build/terraindefinition/{0:D8}.bin"
    },
    new[] { "build/texture/{0:D8}.dds", "build/texture/{0:D8}.bin" },
    new[] { "build/terraintexture/{0:D8}.dds", "build/terraintexture/{0:D8}.bin" },
    new[] { "build/terraindefinition/{0:D8}.bin", "build/terrain/{0:D8}.bin" },
    new[] { "build/gamedata/{0:D8}.bin", "build/gamedata/{0:D8}.dat" },
    new[] { "build/animationdefinition/{0:D8}.bin", "build/animation/{0:D8}.bin" },
    new[] { "build/animationsequence/{0:D8}.bin" },
    new[] {
        "build/animationframe1/{0:D8}.bin", "build/animationframe1/{0}.bin",
        "build/animationframe1/{0:D6}/{0:D2}.bin", "build/animationframe/{0:D6}/{0:D2}.bin",
        "build/animationframe/{0:D8}.bin", "build/animationframe/{0:D8}.amou",
        "build/animationframe1/{0:D8}.amou",
        "build/animation/{0:D6}/{0:D2}.bin"
    },
};

for (int i = 0; i < files.Length; i++)
{
    var path = Path.Combine(ecPath, files[i]);
    if (!File.Exists(path)) { Console.WriteLine($"\nMISSING: {path}"); continue; }
    InspectUop(path, candidatePatternsByFile[i]);
}

static void InspectUop(string path, string[] candidatePatterns)
{
    Console.WriteLine();
    Console.WriteLine("=== " + path + " ===");
    using var fs = File.OpenRead(path);
    using var br = new BinaryReader(fs);

    uint magic = br.ReadUInt32();
    if (magic != 0x50594D) { Console.WriteLine($"Bad magic 0x{magic:X}"); return; }
    uint version = br.ReadUInt32();
    uint timestamp = br.ReadUInt32();
    long nextBlock = br.ReadInt64();
    uint blockSize = br.ReadUInt32();
    int countHint = br.ReadInt32();
    Console.WriteLine($"version={version} blockSize={blockSize} countHint={countHint}");

    var entries = new List<(long Off, int Comp, int Decomp, ulong Hash, short Flag, int HeaderLen)>();
    fs.Seek(nextBlock, SeekOrigin.Begin);
    do
    {
        int filesCount = br.ReadInt32();
        nextBlock = br.ReadInt64();
        for (int k = 0; k < filesCount; k++)
        {
            long offset = br.ReadInt64();
            int headerLength = br.ReadInt32();
            int compressedLength = br.ReadInt32();
            int decompressedLength = br.ReadInt32();
            ulong hash = br.ReadUInt64();
            uint dataHash = br.ReadUInt32();
            short flag = br.ReadInt16();
            if (offset != 0)
                entries.Add((offset + headerLength, compressedLength, decompressedLength, hash, flag, headerLength));
        }
        fs.Seek(nextBlock, SeekOrigin.Begin);
    } while (nextBlock != 0);

    Console.WriteLine($"Total entries: {entries.Count}");

    // Build hash set
    var hashSet = new HashSet<ulong>();
    foreach (var e in entries) hashSet.Add(e.Hash);

    foreach (var pat in candidatePatterns)
    {
        int hits = 0;
        int probeMax = Math.Max(0x14000, entries.Count * 4);
        // For animation-style nested pattern, probe more
        if (pat.Contains("{0:D6}/{0:D2}")) probeMax = 2000 * 100;
        for (int k = 0; k < probeMax; k++)
        {
            var name = string.Format(pat, k);
            ulong h = UopHash(name);
            if (hashSet.Contains(h)) hits++;
        }
        Console.WriteLine($"  pattern '{pat}' -> {hits} hits");
    }

    // Dump first 6 entries: hex of compressed start + first decompressed bytes (if zlib)
    Console.WriteLine("Sample entries (raw + decompressed magic):");
    int n = Math.Min(6, entries.Count);
    for (int i = 0; i < n; i++)
    {
        var e = entries[i];
        fs.Seek(e.Off, SeekOrigin.Begin);
        var raw = br.ReadBytes(Math.Min(32, e.Comp));
        string rawHex = BitConverter.ToString(raw).Replace("-", " ");

        string decompInfo = "";
        try
        {
            fs.Seek(e.Off, SeekOrigin.Begin);
            byte[] cmp = br.ReadBytes(e.Comp);
            byte[] decompressed;
            if (e.Flag == 1)
            {
                using var ms = new MemoryStream(cmp);
                // Skip zlib header (2 bytes) and use DeflateStream
                ms.ReadByte(); ms.ReadByte();
                using var ds = new DeflateStream(ms, CompressionMode.Decompress);
                using var outMs = new MemoryStream();
                ds.CopyTo(outMs);
                decompressed = outMs.ToArray();
            }
            else
            {
                decompressed = cmp;
            }
            int take = Math.Min(32, decompressed.Length);
            string dhex = BitConverter.ToString(decompressed, 0, take).Replace("-", " ");
            string asAscii = "";
            for (int j = 0; j < Math.Min(8, decompressed.Length); j++)
            {
                char c = (char)decompressed[j];
                asAscii += (c >= 32 && c < 127) ? c : '.';
            }
            decompInfo = $" decomp[{decompressed.Length}]={dhex} '{asAscii}'";
        }
        catch (Exception ex) { decompInfo = " (decompress failed: " + ex.Message + ")"; }

        Console.WriteLine($"  [{i}] off={e.Off} comp={e.Comp} decomp={e.Decomp} flag={e.Flag} hash=0x{e.Hash:X16} raw={rawHex}{decompInfo}");
    }
}

static ulong UopHash(string s)
{
    uint eax = 0, ecx = 0, edx = 0;
    uint ebx, esi, edi;
    ebx = edi = esi = (uint)(s.Length + 0xDEADBEEF);
    int i = 0;
    unchecked
    {
        for (i = 0; i + 12 < s.Length; i += 12)
        {
            edi = (uint)((s[i + 7] << 24) | (s[i + 6] << 16) | (s[i + 5] << 8) | s[i + 4]) + edi;
            esi = (uint)((s[i + 11] << 24) | (s[i + 10] << 16) | (s[i + 9] << 8) | s[i + 8]) + esi;
            edx = (uint)((s[i + 3] << 24) | (s[i + 2] << 16) | (s[i + 1] << 8) | s[i]) - esi;
            edx = (edx + ebx) ^ (esi >> 28) ^ (esi << 4);
            esi += edi;
            edi = (edi - edx) ^ (edx >> 26) ^ (edx << 6);
            edx += esi;
            esi = (esi - edi) ^ (edi >> 24) ^ (edi << 8);
            edi += edx;
            ebx = (edx - esi) ^ (esi >> 16) ^ (esi << 16);
            esi += edi;
            edi = (edi - ebx) ^ (ebx >> 13) ^ (ebx << 19);
            ebx += esi;
            esi = (esi - edi) ^ (edi >> 28) ^ (edi << 4);
            edi += ebx;
        }
        if (s.Length - i > 0)
        {
            switch (s.Length - i)
            {
                case 12: esi += (uint)s[i + 11] << 24; goto case 11;
                case 11: esi += (uint)s[i + 10] << 16; goto case 10;
                case 10: esi += (uint)s[i + 9] << 8; goto case 9;
                case 9:  esi += s[i + 8]; goto case 8;
                case 8:  edi += (uint)s[i + 7] << 24; goto case 7;
                case 7:  edi += (uint)s[i + 6] << 16; goto case 6;
                case 6:  edi += (uint)s[i + 5] << 8; goto case 5;
                case 5:  edi += s[i + 4]; goto case 4;
                case 4:  ebx += (uint)s[i + 3] << 24; goto case 3;
                case 3:  ebx += (uint)s[i + 2] << 16; goto case 2;
                case 2:  ebx += (uint)s[i + 1] << 8; goto case 1;
                case 1:  ebx += s[i]; break;
            }
            esi = (esi ^ edi) - ((edi >> 18) ^ (edi << 14));
            ecx = (esi ^ ebx) - ((esi >> 21) ^ (esi << 11));
            edi = (edi ^ ecx) - ((ecx >> 7) ^ (ecx << 25));
            esi = (esi ^ edi) - ((edi >> 16) ^ (edi << 16));
            edx = (esi ^ ecx) - ((esi >> 28) ^ (esi << 4));
            edi = (edi ^ edx) - ((edx >> 18) ^ (edx << 14));
            eax = (esi ^ edi) - ((edi >> 8) ^ (edi << 24));
            return ((ulong)edi << 32) | eax;
        }
    }
    return ((ulong)esi << 32) | eax;
}
