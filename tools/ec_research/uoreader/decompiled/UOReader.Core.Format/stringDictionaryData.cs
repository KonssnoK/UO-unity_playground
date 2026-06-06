using System.Collections.Generic;
using System.IO;
using System.Text;
using Mythic.Package;

namespace UOReader.Core.Format;

public class stringDictionaryData
{
	public long unk64;

	public uint StringCount;

	public short unk16;

	public List<string> stringList = new List<string>();

	public static void LoadUOP(string path)
	{
		MythicPackage mythicPackage = new MythicPackage(path);
		stringDictionaryData stringDictionaryData2 = new stringDictionaryData();
		byte[] buffer = mythicPackage.Blocks[0].Files[0].Unpack(mythicPackage.FileInfo.FullName);
		using (MemoryStream input = new MemoryStream(buffer))
		{
			using BinaryReader binaryReader = new BinaryReader(input);
			stringDictionaryData2.unk64 = binaryReader.ReadInt64();
			stringDictionaryData2.StringCount = binaryReader.ReadUInt32();
			stringDictionaryData2.unk16 = binaryReader.ReadInt16();
			for (int i = 0; i < stringDictionaryData2.StringCount; i++)
			{
				ushort count = binaryReader.ReadUInt16();
				byte[] bytes = binaryReader.ReadBytes(count);
				stringDictionaryData2.stringList.Add(Encoding.ASCII.GetString(bytes));
			}
		}
		FilePointers.stringDictionary = stringDictionaryData2;
	}
}
