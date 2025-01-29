import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

def process_with_groq(markdown_file, mode, output_file, model="llama-3.3-70b-versatile"):
    """
    Reads a Markdown file and sends its content as a user message to the Groq API.
    The response is saved to the specified output file.

    Args:
        markdown_file (str): Path to the Markdown file.
        mode (str): Mode to use for generating chat completions.
        output_file (str): Path to the output Markdown file.
        model (str): Model to use for generating chat completions (default is 'llama-3.3-70b-versatile').

    Returns:
        None: The response is saved to the specified output file.
    """
    
    # Define system messages for different modes
    mode_system_messages = {
        "cleanup": (
            "You will receive a markdown file containing OCR and transcryption of an online meeting. "
            "Cut out things like usernames, UI elements, etc."
            "Do not change the wording, just remove parts irrelevant to the topic of the meeting."
            "Lines begining with 'Timestamp' must stay"
            "Do not write any additional information, keep the markdown formatting."
        ),
        "merge": (
            "You will receive a markdown file containing OCR of an online meeting followed up by audio transcription of that meeting. "
            "Your task is to merge the audio transcription with the OCR and put it in correct order considering topics of OCR and transcription. "
            "Keep all of the original information and just rearrange it in a logical order. "
            "Do not add any of your own information."
        ),
        "summarize": (
            "You will receive a markdown file. Summarize the content of the meeting. "
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

    # Get the assistant's response
    response_content = chat_completion.choices[0].message.content

    # Write the response to the output file
    with open(output_file, "w", encoding="utf-8") as output:
        output.write(response_content)

# Example usage in a different file:
# from your_module import process_with_groq
process_with_groq("outputs/OCR_result.md", "cleanup", "outputs/cleaned_result.md")
