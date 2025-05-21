# Video Clipper

A user-friendly desktop application for video and image processing, built with Python and CustomTkinter.

## Features

### Video Tools
- **Video Cutting**: Trim videos by specifying start and end times
- **Video Cropping**: Crop videos to remove unwanted portions
- **Video Rotation**: Rotate videos by 90°, 180°, or 270°
- **Speed Adjustment**: Adjust video playback speed
- **Preview Support**: View video thumbnails before processing

### Image Tools
- **Format Conversion**: Convert images between multiple formats:
  - PNG (supports transparency)
  - JPEG (with quality optimization)
  - JFIF (JPEG File Interchange Format)
- **Preview Support**: View image thumbnails before conversion
- **Quality Control**: Maintain image quality during conversion
- **Transparency Handling**: Properly handle transparent images

### Audio Tools
- **Audio Extraction**: Extract audio from video files
- **Format Support**: Save audio in MP3 or WAV format
- **Volume Control**: Adjust audio volume during extraction

### User Interface
- **Modern Dark Theme**: Sleek, eye-friendly interface
- **Drag and Drop**: Easy file handling with drag-and-drop support
- **Progress Tracking**: Visual progress bars for all operations
- **Toast Notifications**: User-friendly status updates
- **Settings Management**: Save and load user preferences

## Installation

### Windows
1. Download the latest `VideoClipper.exe` from the releases
2. Double-click to run (no installation required)

### From Source
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/video-clipper.git
   cd video-clipper
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python gui.py
   ```

## Usage

### Video Processing
1. Select the "Video Tools" tab
2. Choose your input video file
3. Set the desired parameters (time range, crop height, etc.)
4. Select output location
5. Click the appropriate action button

### Image Conversion
1. Select the "Image Tools" tab
2. Choose your input image file
3. Select the desired output format (PNG, JPEG, or JFIF)
4. Choose output location
5. Click "Convert Image"

### Audio Extraction
1. Select the "Audio Tools" tab
2. Choose your input video file
3. Select output format (MP3 or WAV)
4. Adjust volume if needed
5. Click "Extract Audio"

## Requirements

- Windows 10 or later
- For source installation:
  - Python 3.8 or later
  - Required Python packages (see requirements.txt)

## Dependencies

- customtkinter
- pillow
- opencv-python
- moviepy
- numpy
- tkinterdnd2 (optional, for drag-and-drop support)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- CustomTkinter for the modern UI components
- MoviePy for video processing capabilities
- Pillow for image processing features