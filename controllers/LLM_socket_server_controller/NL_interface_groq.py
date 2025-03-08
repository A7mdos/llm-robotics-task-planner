import os
import socket
from groq import Groq

# Instantiate the client using your Groq API key.
api_key = "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"
client = Groq(api_key=api_key)

def load_prompt_template():
    """Load the system prompt from a file."""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    prompt_path = os.path.join(current_dir, "prompt.txt")
    with open(prompt_path, "r") as f:
        return f.read()

# Load the prompt template
prompt_template = load_prompt_template()

def translate_nl_to_commands(nl_command: str) -> str:
    """Translate natural language commands into robot commands using the Groq API."""
    
    full_prompt = prompt_template + "\n" + nl_command
    
    # Use Groq API for LLM processing
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Using Groq Llama-3 model
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.0
    )

    # Extract the generated response
    return response.choices[0].message.content.strip()

def send_commands_to_controller(commands: str):
    """Send translated commands to the robot controller via a socket connection."""
    for line in commands.splitlines():
        line = line.strip()
        if not line:
            continue
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 5000))
            s.sendall(line.encode())
            s.close()

if __name__ == "__main__":
    while True:
        nl_command = input("Enter your natural language command (type 'exit' to quit): ")
        if nl_command.lower().strip() == "exit":
            break
        terminal_commands = translate_nl_to_commands(nl_command)
        print("Generated terminal commands:")
        print(terminal_commands)
        send_commands_to_controller(terminal_commands)
