using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;

namespace UOResources {

#pragma warning disable 618
	public static class UOConsole {
		[DllImport("kernel32.dll",
			EntryPoint = "GetStdHandle",
			SetLastError = true,
			CharSet = CharSet.Auto,
			CallingConvention = CallingConvention.StdCall)]
		private static extern IntPtr GetStdHandle(int nStdHandle);

		[DllImport("kernel32.dll",
			EntryPoint = "AllocConsole",
			SetLastError = true,
			CharSet = CharSet.Auto,
			CallingConvention = CallingConvention.StdCall)]
		private static extern int AllocConsole();

		[DllImport("kernel32.dll", 
			EntryPoint = "FreeConsole", 
			SetLastError = true, 
			CharSet = CharSet.Auto, 
			CallingConvention = CallingConvention.StdCall)]
		private static extern int FreeConsole();

		//private const int MY_CODE_PAGE = 437;
		private const int STD_OUTPUT_HANDLE = -11;

		private static TextReader unityStreamIn;
		private static TextWriter unityStreamOut;
		private static TextWriter unityStreamError;
		private static Encoding unityEncodingOut;

		public static void Init(){
			unityStreamIn = Console.In;
			unityStreamOut = Console.Out;
			unityStreamError = Console.Error;
			unityEncodingOut = Console.OutputEncoding;
			AllocConsole();
			IntPtr stdHandle = GetStdHandle(STD_OUTPUT_HANDLE);
			
			FileStream fileStream = new FileStream(stdHandle, FileAccess.Write);
			//Encoding encoding = System.Text.Encoding.GetEncoding(MY_CODE_PAGE);
			Encoding encoding = System.Text.Encoding.ASCII;
			StreamWriter standardOutput = new StreamWriter(fileStream, encoding);
			standardOutput.AutoFlush = true;
			Console.SetOut(standardOutput);
		}

		public static void Release() {
			FreeConsole();
			Console.SetOut(unityStreamOut);
			Console.SetError(unityStreamError);
			Console.SetIn(unityStreamIn);
			Console.OutputEncoding = unityEncodingOut;
		}

		public static void Debug(string format, params object[] arg) {
			Console.WriteLine(format, arg);
		}

		public static void Fatal(string format, params object[] arg) {
			//Console.ForegroundColor = ConsoleColor.Red;
			Console.WriteLine(format, arg);
			//Console.ResetColor();
		}


	}
}
