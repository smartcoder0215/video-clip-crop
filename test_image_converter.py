import os
from image_converter import convert_image, ensure_output_path
from PIL import Image
import tempfile

def test_image_conversion():
    # Create a temporary directory for test files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test image
        test_image_path = os.path.join(temp_dir, "test.png")
        test_image = Image.new('RGB', (100, 100), color='red')
        test_image.save(test_image_path)
        
        # Test cases
        test_cases = [
            ("PNG", "test_output.png"),
            ("JPEG", "test_output.jpg"),
            ("JFIF", "test_output.jfif")
        ]
        
        print("Starting image conversion tests...")
        
        for format, output_name in test_cases:
            try:
                output_path = os.path.join(temp_dir, output_name)
                print(f"\nTesting conversion to {format}...")
                
                # Convert the image
                result = convert_image(test_image_path, output_path, format)
                
                # Verify the output file exists
                if os.path.exists(output_path):
                    # Try to open the converted image
                    with Image.open(output_path) as img:
                        print(f"✓ Successfully converted to {format}")
                        print(f"  - Output size: {img.size}")
                        print(f"  - Mode: {img.mode}")
                else:
                    print(f"✗ Failed: Output file not created for {format}")
                    
            except Exception as e:
                print(f"✗ Error during {format} conversion: {str(e)}")
        
        print("\nAll tests completed!")

if __name__ == "__main__":
    test_image_conversion() 