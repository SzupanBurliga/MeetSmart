import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

def process_with_groq(markdown_file, mode, model="llama-3.3-70b-versatile"):
    """
    Reads a Markdown file and sends its content as a user message to the Groq API.

    Args:
        markdown_file (str): Path to the Markdown file.
        mode (str): Mode to use for generating chat completions.
        model (str): Model to use for generating chat completions (default is 'llama-3.3-70b-versatile').

    Returns:
        str: The response content from the Groq API.
    """
    
    # Define system messages for different modes
    mode_system_messages = {
        "cleanup": (
            "You will receive a markdown file containing OCR of an online meeting. "
            "You have to remove irrelevant content and leave only things important to the presentation. "
            "Cut out things like usernames, UI elements, etc. If a line repeats itself, leave only one of them. "
            "Do not write any additional info, return just the original content."
        ),
        "merge": (
            "You will receive a markdown file containing OCR of an online meeting followed up by audio transcription of that meeting"
            "Ypur task is to corelate the audio transcription with the OCR and put it in correct order"
            "Do not write any additional info, return just the original content."
        ),
        "summarize": (
            "You will receive a markdown file summarize the content of the meeting."
            "Maintain the original formatting as much as possible."
        )
    }

    # Get the appropriate system message based on the mode
    system_message = mode_system_messages.get(mode)
    if not system_message:
        raise ValueError(f"Invalid mode '{mode}'. Supported modes: {', '.join(mode_system_messages.keys())}.")

    # Get API key from environment variables
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables.")

    # Check if the file exists and read its content
    if not os.path.exists(markdown_file):
        raise FileNotFoundError(f"The file '{markdown_file}' does not exist.")
    
    with open(markdown_file, "r", encoding="utf-8") as file:
        user_message_content = file.read()

    # Initialize Groq client
    client = Groq(api_key=api_key)

    # Send the message and get the response
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": user_message_content,
            }
        ],
        model=model,
    )

    # Return the assistant's response
    return chat_completion.choices[0].message.content


# Example usage
# if __name__ == "__main__":
#     try:
#         # Specify the Markdown file and mode
#         markdown_file = "result.md"
#         mode = "cleanup"  # Choose from 'cleanup', 'summarize', 'translate'
        
#         # Process the file and print the result
#         response = process_with_groq(markdown_file, mode)
#         print("Response:")
#         print(response)
#     except Exception as e:
#         print(f"An error occurred: {e}")
