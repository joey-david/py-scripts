import json
import re
import tkinter as tk
from tkinter import filedialog, simpledialog
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from time import time
from tqdm import tqdm
import logging
from typing import Optional, Dict, Any


def llm_analysis(file_path: str, user1_name: str, user2_name: str, 
                user1_nickname: str, user2_nickname: str) -> Dict[str, Any]:
    """Perform LLM analysis with integrated progress tracking."""
    
    with open(file_path, "r", encoding="utf-8") as f:
        conversation_text = f.read()

    prompt = f"""
      You are an advanced conversation analyst. Analyze the following chat between:
      1) {user1_name} (nickname: {user1_nickname})
      2) {user2_name} (nickname: {user2_nickname})

      Your task is to provide a detailed analysis with the following metrics:

      1) **Conversation-level metrics:**
        - **Stability Score (out of 100):** Reflects the emotional consistency and lack of dramatic fluctuations in the conversation.
        - **Health Score (out of 100):** Indicates the overall positive or negative tone and supportiveness of the conversation.
        - **Intensity Score (out of 100):** Measures the engagement level, such as message frequency and response speed.

      2) **User-level metrics (for each user by name):**
        - **Assertiveness (out of 100):** The extent to which the user expresses their opinions and stands firm on their views.
        - **Positiveness (out of 100):** The level of positive emotions and optimism expressed by the user.
        - **Affection Towards the Other (out of 100):** Signs of warmth, care, or fondness directed at the other person.
        - **Romantic Attraction Towards the Other (out of 100):** Indicators of romantic interest or desire towards the other person.
        - **Rationality (out of 100):** The degree to which the user thinks logically and objectively.
        - **Emotiveness (out of 100):** The overall expression of emotions by the user.
        - **IQ Estimate (integer):** A rough estimate of the user's intelligence based on language use and reasoning in the conversation.

      3) **Insights:**
        - An array of at least three insights offering deeper interpretation of the conversation. These should be analysis or inferences that the participants may not be aware of or may find valuable.

      Ensure that the output is strictly in JSON format with the following structure:

      {{
        "conversation_metrics": {{
        "stability_score_out_of_100": int,
        "health_score_out_of_100": int,
        "intensity_score_out_of_100": int
        }},
        "users": {{
        "{user1_name}": {{
          "assertiveness": int,
          "positiveness": int,
          "affection_towards_other": int,
          "romantic_attraction_towards_other": int,
          "rationality": int,
          "emotiveness": int,
          "IQ_estimate": int
        }},
        "{user2_name}": {{
          "assertiveness": int,
          "positiveness": int,
          "affection_towards_other": int,
          "romantic_attraction_towards_other": int,
          "rationality": int,
          "emotiveness": int,
          "IQ_estimate": int
        }}
        }},
        "insights": ["Insight 1", "Insight 2", "Insight 3"]
      }}
    """

    response = text_generator(
        prompt,
        max_new_tokens=4096,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.7
    )

    try:
        analysis = json.loads(response[0]['generated_text'])
    except json.JSONDecodeError:
        analysis = {"error": "Invalid JSON output from model"}
    
    return analysis


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load model directly with fp16 precision
logging.info("Loading tokenizer and model...")
tokenizer = AutoTokenizer.from_pretrained("gradientai/Llama-3-8B-Instruct-Gradient-4194k")
model = AutoModelForCausalLM.from_pretrained("gradientai/Llama-3-8B-Instruct-Gradient-4194k", torch_dtype="auto")

# Create a text generation pipeline
text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def metadata_analysis(filepath, user1_name, user2_name, user1_nickname, user2_nickname):
  with open(filepath, "r", encoding="utf-8") as f:
    messages = f.readlines()

  user1_count = user2_count = user1_chars = user2_chars = 0
  total_messages = len(messages)
  total_characters = 0

  for msg in tqdm(messages, desc="Analyzing messages"):
    try:
      if re.match(r"\d{1,2}/\d{1,2}/\d{2,4} \d{1,2}:\d{2} [APM]{2} - ", msg) or re.match(r"\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2} - ", msg):
        datetime_str, rest = msg.split(" - ", 1)
        user, message = rest.split(": ", 1)
      else:
        user, message = msg.split(": ", 1)
    except ValueError:
      logging.warning(f"Skipping invalid message: {msg}")
      continue

    message_length = len(message)
    total_characters += message_length

    if user == user1_nickname:
      user1_count += 1
      user1_chars += message_length
    elif user == user2_nickname:
      user2_count += 1
      user2_chars += message_length

  user1_percentage_messages = round((user1_count / total_messages) * 100, 2) if total_messages else 0
  user2_percentage_messages = round((user2_count / total_messages) * 100, 2) if total_messages else 0
  user1_percentage_characters = round((user1_chars / total_characters) * 100, 2) if total_characters else 0
  user2_percentage_characters = round((user2_chars / total_characters) * 100, 2) if total_characters else 0
  user1_average_msg_len = round(user1_chars / user1_count, 2) if user1_count else 0
  user2_average_msg_len = round(user2_chars / user2_count, 2) if user2_count else 0

  return {
    "total_messages": total_messages,
    "total_characters": total_characters,
    user1_name: {
      "percentage_messages": user1_percentage_messages,
      "percentage_characters": user1_percentage_characters,
      "average_message_length": user1_average_msg_len
    },
    user2_name: {
      "percentage_messages": user2_percentage_messages,
      "percentage_characters": user2_percentage_characters,
      "average_message_length": user2_average_msg_len
    }
  }

def combine_results(metadata, llm):
  return {
    "metadata": metadata,
    "llm": llm
  }

def get_file_path():
  root = tk.Tk()
  root.withdraw()  # Hide the root window
  file_path = filedialog.askopenfilename(title="Select the chat file")
  return file_path

def get_user_input(prompt):
  root = tk.Tk()
  root.withdraw()  # Hide the root window
  user_input = simpledialog.askstring("Input", prompt)
  return user_input

if __name__ == "__main__":
    # Configure logging with more detailed format
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )

    # Initialize model and tokenizer with progress monitoring
    logging.info("🔧 Initializing model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("gradientai/Llama-3-8B-Instruct-Gradient-4194k")
    model = AutoModelForCausalLM.from_pretrained(
        "gradientai/Llama-3-8B-Instruct-Gradient-4194k",
        torch_dtype="auto"
    )
    
    # Create monitored pipeline
    text_generator, progress_tracker = create_monitored_pipeline(model, tokenizer)
    
    # Your existing main code continues...
    file_path = "joey-norma-31-12-2024_shrinked.txt"
    user1_name = "Joey"
    user1_nickname = "J"
    user2_name = "Norma"
    user2_nickname = "N"
    
    logging.info("📊 Starting analysis pipeline...")
    metadata = metadata_analysis(file_path, user1_name, user2_name, user1_nickname, user2_nickname)
    print("\nMetadata Analysis Results:")
    print(json.dumps(metadata, indent=2))
    
    logging.info("🤖 Starting LLM analysis...")
    result = llm_analysis(file_path, user1_name, user2_name, user1_nickname, user2_nickname)
    print("\nLLM Analysis Results:")
    print(json.dumps(result, indent=2))
    