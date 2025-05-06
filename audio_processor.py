from moviepy.editor import VideoFileClip, AudioFileClip
import os

def extract_audio(video_path, output_path, output_format='mp3', volume=1.0):
    """
    Extract audio from a video file and save it in the specified format.
    
    Args:
        video_path (str): Path to the input video file
        output_path (str): Path where the audio will be saved
        output_format (str): Output format ('mp3' or 'wav')
        volume (float): Volume multiplier (0.0 to 2.0)
    """
    try:
        # Load the video
        video = VideoFileClip(video_path)
        
        # Extract audio
        audio = video.audio
        
        # Adjust volume if needed
        if volume != 1.0:
            audio = audio.volumex(volume)
        
        # Write the audio to the output path
        audio.write_audiofile(output_path, codec='libmp3lame' if output_format == 'mp3' else 'pcm_s16le')
        
        # Close the video and audio to free up resources
        video.close()
        audio.close()
        
        print(f"Audio successfully extracted and saved to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def ensure_output_path(output_path, output_format):
    """
    Ensure the output path has a valid filename and extension.
    """
    # If output_path is a directory, create a default filename
    if os.path.isdir(output_path) or not output_path:
        output_path = os.path.join(output_path, f"extracted_audio.{output_format}")
    
    # If no extension is provided, add the correct one
    if not os.path.splitext(output_path)[1]:
        output_path += f".{output_format}"
    
    return output_path 