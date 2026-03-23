using UnityEngine;

namespace UOResources {

	public static class UOConsole {

		public static void Init(){
			UnityEngine.Debug.Log("[UOConsole] Initialized");
		}

		public static void Release() {
		}

		public static void Debug(string format, params object[] arg) {
			UnityEngine.Debug.Log(string.Format(format, arg));
		}

		public static void Fatal(string format, params object[] arg) {
			UnityEngine.Debug.LogError(string.Format(format, arg));
		}
	}
}
