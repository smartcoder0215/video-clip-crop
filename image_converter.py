from PIL import Image
import os

def convert_image(input_path, output_path, output_format):
    """
    Convert an image from one format to another.
    
    Args:
        input_path (str): Path to the input image file
        output_path (str): Path where the converted image will be saved
        output_format (str): Desired output format ('PNG', 'JPEG', or 'JFIF')
    """
    try:
        # Validate input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGB if needed (for JPEG/JFIF)
            if output_format in ('JPEG', 'JFIF'):
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Convert P mode (palette) to RGB
                    if img.mode == 'P':
                        img = img.convert('RGB')
                    else:
                        # Create white background for transparent images
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                elif img.mode not in ('RGB', 'L'):
                    img = img.convert('RGB')
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Save the image in the new format
            save_format = 'JPEG' if output_format in ('JPEG', 'JFIF') else output_format
            save_params = {'format': save_format}
            
            # Add quality parameter for JPEG/JFIF
            if save_format == 'JPEG':
                save_params['quality'] = 95
                save_params['optimize'] = True
            
            img.save(output_path, **save_params)
            
        print(f"Image successfully converted and saved to: {output_path}")
        return True
        
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        raise
    except Exception as e:
        print(f"An error occurred during conversion: {str(e)}")
        raise

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
    print("3. Convert to JFIF")
    choice = input("Enter your choice (1, 2, or 3): ")
    
    input_image = input("Enter the path to your input image: ")
    output_image = input("Enter the path for the output image: ")
    
    # Set the output format based on choice
    output_format = {
        "1": "PNG",
        "2": "JPEG",
        "3": "JFIF"
    }.get(choice, "PNG")
    
    # Ensure the output path is valid
    output_image = ensure_output_path(output_image, output_format)
    
    try:
        convert_image(input_image, output_image, output_format)
        print("Conversion completed successfully!")
    except Exception as e:
        print(f"Conversion failed: {str(e)}")

if __name__ == "__main__":
    main() 