# Video Clipper Tool

A simple tool to help you edit your videos. You can either cut a portion of your video or remove the bottom part of it.

## What You Need Before Starting

1. Python installed on your computer (Download from [python.org](https://www.python.org/downloads/))
2. The video file you want to edit

## How to Set Up

1. Download all the files from this project to a folder on your computer
2. Open Command Prompt (Windows) or Terminal (Mac/Linux)
3. Navigate to the folder where you saved the files
4. Run this command to install required software:
   ```
   pip install -r requirements.txt
   ```

## How to Use

1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Navigate to the folder where you saved the files
3. Run the program by typing:
   ```
   python video_clipper.py
   ```
4. The program will show you two options:
   - Option 1: Cut a portion of your video
   - Option 2: Remove the bottom part of your video

### Option 1: Cutting a Video
1. Choose option 1
2. Enter the full path to your video file (e.g., `C:\Videos\myvideo.mp4`)
3. Enter where you want to save the new video (e.g., `C:\Videos\cut_video.mp4`)
4. Enter the start time in seconds (e.g., 10 for 10 seconds)
5. Enter the end time in seconds (e.g., 30 for 30 seconds)
6. Wait for the program to finish

### Option 2: Removing Bottom of Video to Erase the WaterMark or Logo
1. Choose option 2
2. Enter the full path to your video file
3. Enter where you want to save the new video
4. Enter the height in pixels you want to keep from the top (e.g., 720 for HD quality)
5. Wait for the program to finish

## Tips
- Make sure you have enough disk space for the new video
- The process might take a few minutes depending on your video size
- Keep the original video file safe until you're happy with the result

## Need Help?
If you encounter any problems:
1. Make sure Python is installed correctly
2. Check that you entered the correct file paths
3. Ensure you have enough disk space
4. Make sure the video file isn't being used by another program 

If you need any other help, feel free to reach out to me. pavelnefir85@gmail.com