# Image editing logic: defining the transformations to apply based on the user's request
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageFilter
import re


def process_img(image, edits):
        # Iterate through all the edits specified by the user
        for edit in edits:
            if edit.lower() in ['grayscale']:
                # Convert the image to grayscale
                image = image.convert("L")

            elif edit.lower() in ['resize', 'changesize', 'change size', 'size']:
                # Resize the image based on the given dimensions
                x, y = [int(num) for num in re.findall(r'-?\d+', edits[edit])]
                image = image.resize((x, y))

            elif edit.lower() in ['rotate', 'turn', 'flip', 'angle']:
                # Rotate or flip the image based on the user's input
                for edit in edits:
                    if isinstance(edits[edit], str):
                        # If the value is a string, extract the number using regex
                        numbers = re.findall(r'\d+', edits[edit])  # Extract all numbers
                        if numbers:  # If there's a number found
                            angle = int(numbers[0])  # Take the first number and convert to int
                    elif isinstance(edits[edit], int):
                        # If the value is already an integer, use it directly
                        angle = edits[edit]
                        
                image = image.rotate(angle)

            elif edit.lower() in ['blur', 'blurred']:
                # Apply a blur filter to the image
                image = image.filter(ImageFilter.GaussianBlur(radius=10))  

            elif edit.lower() in ['text', 'write']:
                # Add text to the image at a specified position
                draw = ImageDraw.Draw(image)
                draw.text((10, 10), edits[edit], fill="white")

            elif edit.lower() in ['flip']:
                # Flip the image either horizontally or vertically
                if edits[edit].lower() in ["horizontal", "horizontally"]:
                    image = image.transpose(Image.FLIP_LEFT_RIGHT)
                else:
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)

            elif edit.lower() == 'brightness':
                # Adjust the brightness of the image
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(1.5)
            
            elif edit.lower() == 'contrast':
                # Adjust the contrast of the image
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(2)

            elif edit.lower() in ['sharpen', 'sharpness']:
                # Sharpen the image
                enhancer = ImageEnhance.Sharpness(image)
                image = enhancer.enhance(2) 
                
        # For more options visit https://pillow.readthedocs.io/en/stable/index.html

        return image
# except:
#     Display a warning if an error occurs during image processing
#     st.warning("Error occurred. Please try again")
