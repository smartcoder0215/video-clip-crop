import subprocess
import sys
import os

def run_command(command):
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("Setting up Media Tools environment...")
    
    # Upgrade pip and install build tools
    print("\n1. Upgrading pip and installing build tools...")
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "setuptools", "wheel"])
    
    # Install dependencies one by one
    print("\n2. Installing dependencies...")
    
    # Install Pillow
    print("\nInstalling Pillow...")
    if not run_command([sys.executable, "-m", "pip", "install", "Pillow>=9.5.0"]):
        print("Failed to install Pillow. Trying alternative method...")
        run_command([sys.executable, "-m", "pip", "install", "--upgrade", "Pillow"])
    
    # Install moviepy
    print("\nInstalling moviepy...")
    run_command([sys.executable, "-m", "pip", "install", "moviepy>=1.0.3"])
    
    # Install opencv-python
    print("\nInstalling opencv-python...")
    if not run_command([sys.executable, "-m", "pip", "install", "opencv-python>=4.8.0"]):
        print("Failed to install opencv-python. Trying headless version...")
        run_command([sys.executable, "-m", "pip", "install", "opencv-python-headless"])
    
    # Install customtkinter
    print("\nInstalling customtkinter...")
    if not run_command([sys.executable, "-m", "pip", "install", "customtkinter>=5.2.0"]):
        print("Failed to install customtkinter. Trying without dependencies...")
        run_command([sys.executable, "-m", "pip", "install", "customtkinter", "--no-deps"])
    
    # Install tkinterdnd2
    print("\nInstalling tkinterdnd2...")
    if not run_command([sys.executable, "-m", "pip", "install", "tkinterdnd2>=0.3.0"]):
        print("Failed to install tkinterdnd2. Trying alternative methods...")
        # Try installing from source
        if not run_command([sys.executable, "-m", "pip", "install", "git+https://github.com/pmgagne/tkinterdnd2.git"]):
            print("Failed to install tkinterdnd2 from source. Trying alternative package...")
            run_command([sys.executable, "-m", "pip", "install", "tkinterdnd2-tk"])
    
    print("\nSetup completed!")
    print("\nIf you encountered any errors, please try the following:")
    print("1. Make sure you have Python 3.8 or later installed")
    print("2. Try running the commands manually from requirements.txt")
    print("3. If issues persist, try installing the packages one by one")
    print("\nNote: If tkinterdnd2 installation fails, the program will still work")
    print("but drag and drop functionality will be disabled.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 