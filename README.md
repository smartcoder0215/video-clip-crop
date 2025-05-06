# Video and Image Tools

A simple tool to help you edit your videos and convert images. You can:
- Cut a portion of your video
- Remove the bottom part of your video
- Convert WebP images to PNG or JPEG format
- Extract audio from videos
- Adjust video and image properties

## What You Need Before Starting

1. Python 3.8 or later installed on your computer (Download from [python.org](https://www.python.org/downloads/))
2. The video or image file you want to edit

## How to Set Up

### Easy Installation (Recommended)
1. Download all the files from this project to a folder on your computer
2. Open Command Prompt (Windows) or Terminal (Mac/Linux)
3. Navigate to the folder where you saved the files
4. Run the setup script:
   ```
   python setup.py
   ```
   This will automatically install all required dependencies.

### Manual Installation
If the automatic setup doesn't work, you can try installing dependencies manually:

1. First, upgrade pip and install build tools:
   ```
   python -m pip install --upgrade pip setuptools wheel
   ```

2. Then install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. If you encounter errors, try installing packages one by one:
   ```
   pip install moviepy>=1.0.3
   pip install Pillow>=9.5.0
   pip install customtkinter>=5.2.0
   pip install opencv-python>=4.8.0
   pip install tkinterdnd2>=0.3.0
   ```

### Troubleshooting Installation
If you encounter issues during installation:

1. For Pillow installation errors:
   ```
   python -m pip install --upgrade Pillow
   ```

2. For OpenCV installation errors:
   ```
   pip install opencv-python-headless
   ```

3. For CustomTkinter installation errors:
   ```
   pip install customtkinter --no-deps
   ```

## How to Use

### Using the Graphical Interface (Recommended)
1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Navigate to the folder where you saved the files
3. Run the program by typing:
   ```
   python gui.py
   ```
4. The program will open a window with three tabs:
   - Video Tools: For cutting, cropping, and adjusting videos
   - Image Tools: For converting and editing images
   - Audio Tools: For extracting and processing audio

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

3. Additional video features:
   - Rotate video (90°, 180°, 270°)
   - Adjust video speed
   - Preview video before processing

### Image Tools Tab
1. To convert an image:
   - Click "Select Input Image" to choose your image file
   - Click "Select Output Location" to choose where to save the result
   - Choose PNG or JPEG format using the radio buttons
   - Click "Convert Image"

2. The image preview and progress bar will help you track the conversion process.

### Audio Tools Tab
1. To extract audio from video:
   - Click "Select Video" to choose your video file
   - Click "Select Output Location" to choose where to save the audio
   - Choose MP3 or WAV format
   - Adjust volume if needed
   - Click "Extract Audio"

### Settings Tab
1. Theme selection:
   - Choose between Dark and Light themes
2. Default output directory:
   - Set a default location for saved files

## Tips
- Make sure you have enough disk space for the new files
- The process might take a few minutes depending on your file size
- Keep the original files safe until you're happy with the result
- For images, PNG format is better for images with transparency, while JPEG is better for photographs
- The GUI will show success or error messages to help you understand what's happening
- You can drag and drop files directly into the program

## Need Help?
If you encounter any problems:
1. Make sure Python is installed correctly
2. Check that you entered the correct file paths
3. Ensure you have enough disk space
4. Make sure the files aren't being used by another program
5. Try running the setup script again if you encounter dependency issues

If you need any other help, feel free to reach out to me. pavelnefir85@gmail.com