from moviepy.editor import VideoFileClip
import os

def clip_video(input_path, output_path, start_time, end_time):
    """
    Clip a video from start_time to end_time.
    
    Args:
        input_path (str): Path to the input video file
        output_path (str): Path where the clipped video will be saved
        start_time (float): Start time in seconds
        end_time (float): End time in seconds
    """
    try:
        # Load the video
        video = VideoFileClip(input_path)
        
        # Clip the video
        clipped_video = video.subclip(start_time, end_time)
        
        # Write the clipped video to the output path
        clipped_video.write_videofile(output_path, codec='libx264')
        
        # Close the video to free up resources
        video.close()
        clipped_video.close()
        
        print(f"Video successfully clipped and saved to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def crop_video_bottom(input_path, output_path, crop_height):
    """
    Crop the bottom portion of a video.
    
    Args:
        input_path (str): Path to the input video file
        output_path (str): Path where the cropped video will be saved
        crop_height (int): Height in pixels to keep from the top
    """
    try:
        # Load the video
        video = VideoFileClip(input_path)
        
        # Get original dimensions
        original_height = video.h
        
        # Crop the video
        cropped_video = video.crop(y1=0, y2=crop_height)
        
        # Write the cropped video to the output path
        cropped_video.write_videofile(output_path, codec='libx264')
        
        # Close the video to free up resources
        video.close()
        cropped_video.close()
        
        print(f"Video successfully cropped and saved to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def ensure_output_path(output_path):
    """
    Ensure the output path has a valid filename and extension.
    """
    # If output_path is a directory, create a default filename
    if os.path.isdir(output_path) or not output_path:
        output_path = os.path.join(output_path, "output_video.mp4")
    
    # If no extension is provided, add .mp4
    if not os.path.splitext(output_path)[1]:
        output_path += ".mp4"
    
    return output_path

def main():
    print("Video Processing Tool")
    print("1. Clip video (time-based)")
    print("2. Crop bottom of video")
    choice = input("Enter your choice (1 or 2): ")
    
    input_video = input("Enter the path to your input video: ")
    output_video = input("Enter the path for the output video: ")
    
    # Ensure the output path is valid
    output_video = ensure_output_path(output_video)
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_video)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if choice == "1":
        # Get start and end times
        start_time = float(input("Enter start time (in seconds): "))
        end_time = float(input("Enter end time (in seconds): "))
        clip_video(input_video, output_video, start_time, end_time)
    elif choice == "2":
        # Get crop height
        crop_height = int(input("Enter the height in pixels to keep from the top: "))
        crop_video_bottom(input_video, output_video, crop_height)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main() 