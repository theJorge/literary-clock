import os
import sys
from PIL import Image # Import the Pillow library

# --- Path Setup ---
# Assuming 'merrychristmas.png' is in the same directory as this script.
# Adjust the 'picdir' if your image is in a different location (e.g., in a 'pic' folder)
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic') 
# If your image is in the same folder as the script, use:
# imagedir = os.path.dirname(os.path.realpath(__file__)) 
imagedir = os.path.dirname(os.path.realpath(__file__))

libdir = "./lib/e-Paper/RaspberryPi_JetsonNano/python/lib"
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in5_V2 as epd7in5
# --------------------

def main():
    try:
        epd = epd7in5.EPD()
        
        # 1. Initialize and clear the display
        print("Initializing and clearing display...")
        epd.init()
        # epd.Clear() # Optional: You can skip the clear to speed up refresh

        # 2. Define Display Dimensions
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: white background
        
        # 3. Open and Process the PNG image
        print("Loading and preparing image...")
        
        # Construct the full path to the image
        image_path = os.path.join(imagedir, 'merrychristmas.png')
        
        # Open the image file
        img = Image.open(image_path)
        
        # E-Ink displays typically require specific preparation:
        # a) Resize: Match the display resolution (800x480 for 7.5inch V2)
        # b) Convert: Use Dithering and convert to '1' bit mode (1-bit black/white)
        #            This is necessary for the black/white e-ink panel.
        
        Limage = img.resize((epd.width, epd.height))
        # Use Image.Dither.FLOYDSTEINBERG for better quality conversion to 1-bit
        Himage = Limage.convert('1', dither=Image.Dither.FLOYDSTEINBERG)

        # 4. Display the image
        print("Displaying image...")
        epd.display(epd.getbuffer(Himage))
        
        print("Entering sleep mode...")
        epd.sleep()
        
    except IOError as e:
        print(f"I/O Error: {e}")
        
    except KeyboardInterrupt:
        print("Exiting...")
        epd.sleep()
        sys.exit()

if __name__ == '__main__':
    main()
