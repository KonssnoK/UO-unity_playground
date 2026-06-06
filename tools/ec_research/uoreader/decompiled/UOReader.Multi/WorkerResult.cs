using System.Drawing;

namespace UOReader.Multi;

public class WorkerResult
{
	public string command;

	public Bitmap image;

	public string description;

	public WorkerResult(Bitmap img, string desc)
	{
		image = img;
		description = desc;
	}
}
