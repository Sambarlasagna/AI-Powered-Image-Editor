import streamlit as st
from process import process_prompt, initialize  # Importing the necessary functions from the 'process' module
from edit import process_img  # Importing image processing function from the 'edit' module
import io
from PIL import Image  # Importing the Python Imaging Library to handle image manipulation
import time

# Set up the Streamlit app's title
st.title("AI Image Editor")

#To get typing animation
def typing_animation(text, speed=0.01):
    """
    Displays a typing animation in Streamlit.
    
    Parameters:
        text (str): The text to display with typing effect.
        speed (float): The delay (in seconds) between each character.
    """
    placeholder = st.empty()  # Create a placeholder for the text
    typed_text = ""
    for char in text:
        typed_text += char
        placeholder.text(typed_text)  # Update the placeholder with new text
        time.sleep(speed)  # Delay to simulate typing effect

# Initialize the AI model and get a welcome message
intro = initialize()
typing_animation(intro)

# Text input field where the user can specify the image edits they want
command = st.text_input("", placeholder="e.g. resize to 100x100")

try:
    # Allow the user to upload an image (with validation for accepted types)
    uploaded_img = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])
except:
    # Display a warning if file upload fails
    st.warning("Upload files of type: jpg, png or jpeg")

try:
    if uploaded_img:
        # Open the uploaded image and display it
        image = Image.open(uploaded_img)
        st.image(image, caption="Uploaded Image")

        # Process the user's command to extract editing instructions
        reply, edits = process_prompt(command)
        

        # Process the image with the extracted edits
        edited_img = process_img(image, edits)

        if edits:
            # Display the edited image after modifications
            st.image(edited_img, caption="Edited image")

            # Convert the edited image to a byte stream for downloading
            img_byte_arr = io.BytesIO()
            edited_img.save(img_byte_arr, format="PNG")
            img_byte_arr.seek(0)

            # Allow the user to download the edited image
            st.download_button(
                label="Download Image",
                data=img_byte_arr,
                file_name="downloaded_image.jpg",
                mime="image/jpeg"
            )

            # Display the reply text to inform the user about the edits
            typing_animation(reply)
        else:
            # If no edits were applied, show the reply message
            typing_animation(reply)
except:
    # Display a warning if an error occurs during image processing
    st.warning("Error occurred. Please try again")