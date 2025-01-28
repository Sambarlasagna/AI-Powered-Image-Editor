# Function to initialize the AI model and generate a response to ask the user for help
import ollama
import ast
import re

def initialize():
    # Ask the AI to give a message with a request for help
    init = ollama.generate(model="llama3", prompt="You are an image editor, ask how can you be of help to the user in minimum 10 words.")
    return init['response'].strip('"')

# Function to process the user's input and generate a dictionary of image edits
def process_prompt(task):
    # Define the prompt for the AI to extract image editing instructions
    prompt = f'''Extract image editing terms from: {task}.
        If there are no image editing terminologies explicitly mentioned, return an empty dictionary: {{}}.
        Do not infer or guess image editing terms.
        Return them in dictionary form with ONLY the image editing terminologies as keys
        (e.g. "grayscale", "brightness", "contrast", "text", "resize", "blur", "rotate", "enhance", "contrast","sharpen")
        and their corresponding values. (e.g., +20%, -20%, 120x150 or None to the corresponding key if no values are provided)
        Ensure that the proper image editing terminology is used (e.g., "grayscale" instead of "black and white").
        and their corresponding values. (e.g., +20%, -20%, 120x150 or None to the corresponding key if no values are provided)
        Every key MUST contain a value. 
        Enclose it in curly braces.
        Return the dictionary with no extra text, explanation, or formatting.
        Now, after the dictionary, add a reply text of about 20-50 words, human-like, acknowledge the action taken. Keep it short and relevant to the image edits.'''

    
    # Get the response from the Ollama model
    response = ollama.generate(model="llama3", prompt=prompt)

    # Extract the dictionary part from the response
    match = re.search(r'\{.*\}', response['response'])

    if match:
        # If a dictionary is found, process it
        dict_part = match.group(0)
        d = ast.literal_eval(dict_part)
        if d:
            # If there are editing terms, clean up the response
            text = response['response'].replace(dict_part, '').strip()
            text = re.sub(r'\s+', ' ', text).strip()
        else:
            # If no editing terms are found, ask the user for more clarity
            response2 = ollama.generate(model="llama3", prompt="You are an image editor and the user hasn't been clear about their requests. Reply with 1-50 words asking the user to be more clear.")
            return response2['response'].strip('"'),{}
    else:
        print("Error")

    return text, d
