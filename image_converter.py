from PIL import Image
import os

def convert_image(input_path, output_path, output_format):
    """
    Convert an image from one format to another.
    
    Args:
        input_path (str): Path to the input image file
        output_path (str): Path where the converted image will be saved
        output_format (str): Desired output format ('PNG' or 'JPEG')
    """
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGB if needed (for JPEG)
            if output_format == 'JPEG' and img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            
            # Save the image in the new format
            img.save(output_path, format=output_format)
            
        print(f"Image successfully converted and saved to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def ensure_output_path(output_path, output_format):
    """
    Ensure the output path has a valid filename and extension.
    """
    # If output_path is a directory, create a default filename
    if os.path.isdir(output_path) or not output_path:
        output_path = os.path.join(output_path, f"converted_image.{output_format.lower()}")
    
    # If no extension is provided, add the correct one
    if not os.path.splitext(output_path)[1]:
        output_path += f".{output_format.lower()}"
    
    return output_path

def main():
    print("Image Conversion Tool")
    print("1. Convert to PNG")
    print("2. Convert to JPEG")
    choice = input("Enter your choice (1 or 2): ")
    
    input_image = input("Enter the path to your input image: ")
    output_image = input("Enter the path for the output image: ")
    
    # Set the output format based on choice
    output_format = 'PNG' if choice == "1" else 'JPEG'
    
    # Ensure the output path is valid
    output_image = ensure_output_path(output_image, output_format)
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_image)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    convert_image(input_image, output_image, output_format)

if __name__ == "__main__":
    main() 