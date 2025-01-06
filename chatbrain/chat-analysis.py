import json
import tkinter as tk
from tkinter import filedialog, simpledialog
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load model directly
tokenizer = AutoTokenizer.from_pretrained("gradientai/Llama-3-8B-Instruct-Gradient-4194k")
model = AutoModelForCausalLM.from_pretrained("gradientai/Llama-3-8B-Instruct-Gradient-4194k")

# Create a text generation pipeline
text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def analyze_chat(file_path, user1_name, user2_name, user1_nickname, user2_nickname):
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

    Conversation:
    {conversation_text}
    """

    response = text_generator(prompt, max_length=16384, num_return_sequences=1)
    text = response[0]["generated_text"]
    try:
        analysis = json.loads(text)
    except json.JSONDecodeError:
        analysis = {"error": "Invalid JSON output from model."}
    return analysis

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
    file_path = "joey-norma-31-12-2024_shrinked.txt"
    user1_name = "Joey"
    user1_nickname = "J"
    user2_name = "Norma"
    user2_nickname = "N"
    # file_path = get_file_path()
    # user1_name = get_user_input("Enter the first user's name:")
    # user1_nickname = get_user_input("Enter the first user's nickname:")
    # user2_name = get_user_input("Enter the second user's name:")
    # user2_nickname = get_user_input("Enter the second user's nickname:")
    result = analyze_chat(file_path, user1_name, user2_name, user1_nickname, user2_nickname)
    print(json.dumps(result, indent=2))