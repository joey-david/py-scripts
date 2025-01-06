import json
import re
import tkinter as tk
from tkinter import filedialog, simpledialog
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from datetime import datetime, timedelta
from time import time
from tqdm import tqdm
import logging
import threading
import queue
from typing import Optional, Dict, Any
import sys

class ProgressTracker:
    """A sophisticated progress tracking system compatible with the Transformers pipeline."""
    
    def __init__(self):
        self.stages = {
            'preprocessing': 0,
            'inference': 0,
            'postprocessing': 0
        }
        self._lock = threading.Lock()
        self.start_times: Dict[str, float] = {}
        self.end_times: Dict[str, float] = {}
        self.current_stage = None
        self.total_tokens = 0
        self.processed_tokens = 0
        self._stop_event = threading.Event()

    def start_stage(self, stage_name: str) -> None:
        """Initialize a processing stage with timing."""
        with self._lock:
            self.current_stage = stage_name
            self.start_times[stage_name] = time()
            self.stages[stage_name] = 0
            logging.info(f"▶️ Starting {stage_name} stage")

    def update_stage(self, stage_name: str, progress: float) -> None:
        """Update progress for a specific stage."""
        with self._lock:
            self.stages[stage_name] = min(100, max(0, progress))
            elapsed = time() - self.start_times.get(stage_name, time())
            logging.info(f"📊 {stage_name}: {progress:.1f}% complete ({elapsed:.1f}s elapsed)")

    def end_stage(self, stage_name: str) -> None:
        """Mark a stage as complete and record timing."""
        with self._lock:
            self.end_times[stage_name] = time()
            self.stages[stage_name] = 100
            duration = self.end_times[stage_name] - self.start_times.get(stage_name, self.end_times[stage_name])
            logging.info(f"✅ Completed {stage_name} in {duration:.2f} seconds")

    def get_status(self) -> Dict[str, Any]:
        """Retrieve current progress status across all stages."""
        with self._lock:
            return {
                'current_stage': self.current_stage,
                'stages': self.stages.copy(),
                'timings': {
                    stage: {
                        'start': self.start_times.get(stage),
                        'end': self.end_times.get(stage),
                        'duration': self.end_times.get(stage, time()) - self.start_times.get(stage, time()) 
                        if stage in self.start_times else 0
                    }
                    for stage in self.stages
                }
            }

    def stop(self) -> None:
        """Signal monitoring to stop."""
        self._stop_event.set()

    @property
    def should_stop(self) -> bool:
        """Check if monitoring should stop."""
        return self._stop_event.is_set()

class ProgressBar:
    """A custom progress bar for terminal output."""
    
    def __init__(self, total: int = 100, prefix: str = '', suffix: str = '', length: int = 50):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.current = 0
        self._lock = threading.Lock()

    def update(self, current: int) -> None:
        """Update and display the progress bar."""
        with self._lock:
            self.current = current
            percentage = (self.current / self.total) * 100
            filled_length = int(self.length * self.current // self.total)
            bar = '█' * filled_length + '-' * (self.length - filled_length)
            sys.stdout.write(f'\r{self.prefix} |{bar}| {percentage:.1f}% {self.suffix}')
            sys.stdout.flush()

    def finish(self) -> None:
        """Complete the progress bar."""
        self.update(self.total)
        sys.stdout.write('\n')
        sys.stdout.flush()

def create_monitored_pipeline(model, tokenizer) -> tuple:
    """Create a text generation pipeline with integrated progress monitoring."""
    progress_tracker = ProgressTracker()
    
    # Create standard pipeline
    text_generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer
    )
    
    # Enhance pipeline with progress tracking
    original_call = text_generator.__call__

    def monitored_call(*args, **kwargs):
        progress_tracker.start_stage('preprocessing')
        
        # Token counting for progress estimation
        input_text = args[0] if args else kwargs.get('text_inputs', '')
        input_tokens = tokenizer(input_text, return_length=True)['length']
        expected_output_tokens = kwargs.get('max_new_tokens', 4096)
        total_tokens = input_tokens + expected_output_tokens
        progress_tracker.total_tokens = total_tokens
        
        progress_tracker.end_stage('preprocessing')
        progress_tracker.start_stage('inference')
        
        # Create progress bar for inference
        progress_bar = ProgressBar(prefix='Generating:', suffix='Complete')
        
        def progress_callback():
            while not progress_tracker.should_stop:
                # Estimate progress based on known model characteristics
                progress = min(100, (progress_tracker.processed_tokens / total_tokens) * 100)
                progress_tracker.update_stage('inference', progress)
                progress_bar.update(int(progress))
                time.sleep(0.1)
            progress_bar.finish()

        # Start progress monitoring thread
        monitor_thread = threading.Thread(target=progress_callback)
        monitor_thread.daemon = True
        monitor_thread.start()

        try:
            result = original_call(*args, **kwargs)
        finally:
            progress_tracker.stop()
            progress_tracker.end_stage('inference')
            
        progress_tracker.start_stage('postprocessing')
        progress_tracker.end_stage('postprocessing')
        
        return result

    text_generator.__call__ = monitored_call
    return text_generator, progress_tracker

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

      Conversation:
      {conversation_text}
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
    