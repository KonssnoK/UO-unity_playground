using System.Collections.Generic;
using System.Threading;

namespace UOResources {
	public class SectorsLoader {
		public const int SECTORS_COUNT = 7138;
		private static Queue<int> _sectorsQueue = new Queue<int>();
		private static Semaphore sem = new Semaphore(0, 1);
		private static Thread _thread;
		private static bool[] alreadyKnown = new bool[SECTORS_COUNT];
		private static bool isClosing = false;
		public static void Enqueue(int sector) {
			//UOConsole.Debug("sector {0}", sector);
			if (alreadyKnown[sector])
				return;//TODO: Change after resource managing has been considered

			alreadyKnown[sector] = true;
			if (!_sectorsQueue.Contains(sector)) {
				_sectorsQueue.Enqueue(sector);
				UOConsole.Debug("UPDATE: Queuing {0} ..", sector);
				if (_sectorsQueue.Count == 1) {
					sem.Release();
				}
			}
		}

		public static void Dismiss(int sector) {
			if(alreadyKnown[sector])
				alreadyKnown[sector] = false;
		}

		public int Count { get { return _sectorsQueue.Count; } }

		public static void startLoader() {
			_thread = new Thread(new ThreadStart(loaderThread));
			_thread.Start();
		}

		public static void endLoader() {
			isClosing = true;
		}

		public static void loaderThread() {
			while (!isClosing) {
				if (_sectorsQueue.Count == 0) {
					UOConsole.Debug("LOADER: thread: waiting..");
					sem.WaitOne();//Halt the loader thread
					UOConsole.Debug("LOADER: thread: resuming..");
				}

				int sector = _sectorsQueue.Dequeue();
				UOConsole.Debug("LOADER: Loading  {0}", sector);
				UOResources.UOFacetManager.loadSprites(sector);
				UOConsole.Debug("LOADER: Finished {0} - {1} left", sector, _sectorsQueue.Count);
			}
		}
	}
}
