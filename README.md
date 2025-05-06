# Video and Image Tools

A simple tool to help you edit your videos and convert images. You can:
- Cut a portion of your video
- Remove the bottom part of your video
- Convert WebP images to PNG or JPEG format

## What You Need Before Starting

1. Python installed on your computer (Download from [python.org](https://www.python.org/downloads/))
2. The video or image file you want to edit

## How to Set Up

1. Download all the files from this project to a folder on your computer
2. Open Command Prompt (Windows) or Terminal (Mac/Linux)
3. Navigate to the folder where you saved the files
4. Run this command to install required software:
   ```
   pip install -r requirements.txt
   ```

## How to Use

### Using the Graphical Interface (Recommended)
1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Navigate to the folder where you saved the files
3. Run the program by typing:
   ```
   python gui.py
   ```
4. The program will open a window with two tabs:
   - Video Tools: For cutting and cropping videos
   - Image Tools: For converting images

### Video Tools Tab
1. To cut a video:
   - Click "Select Input Video" to choose your video file
   - Click "Select Output Location" to choose where to save the result
   - Enter the start and end times in seconds
   - Click "Cut Video"

2. To crop a video:
   - Click "Select Input Video" to choose your video file
   - Click "Select Output Location" to choose where to save the result
   - Enter the height in pixels to keep from the top
   - Click "Crop Video"

### Image Tools Tab
1. To convert an image:
   - Click "Select Input Image" to choose your image file
   - Click "Select Output Location" to choose where to save the result
   - Choose PNG or JPEG format using the radio buttons
   - Click "Convert Image"

### Using Command Line (Alternative Method)
If you prefer using the command line, you can still use the original scripts:

1. For video editing:
   ```
   python video_clipper.py
   ```

2. For image conversion:
   ```
   python image_converter.py
   ```

## Tips
- Make sure you have enough disk space for the new files
- The process might take a few minutes depending on your file size
- Keep the original files safe until you're happy with the result
- For images, PNG format is better for images with transparency, while JPEG is better for photographs
- The GUI will show success or error messages to help you understand what's happening

## Need Help?
If you encounter any problems:
1. Make sure Python is installed correctly
2. Check that you entered the correct file paths
3. Ensure you have enough disk space
4. Make sure the files aren't being used by another program

If you need any other help, feel free to reach out to me. pavelnefir85@gmail.com