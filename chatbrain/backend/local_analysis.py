import json
import re
import tkinter as tk
from tkinter import filedialog, simpledialog
from time import time
from tqdm import tqdm
import logging
from typing import Optional, Dict, Any


def metadata_analysis(compressed_string, n_users, usersnames, nicknames):
  messages = compressed_string.split("\n")
  # Prepare stats dict
  stats = {}
  for i in range(n_users):
    stats[usersnames[i]] = {
      "messages": 0,
      "characters": 0
    }

  total_messages = len(messages)
  total_characters = 0

  for msg in tqdm(messages, desc="Analyzing messages"):
    try:
      if re.match(r"\d{1,2}/\d{1,2}/\d{2,4} \d{1,2}:\d{2} [APM]{2} - ", msg) or \
         re.match(r"\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2} - ", msg):
        _, rest = msg.split(" - ", 1)
        user, message = rest.split(": ", 1)
      else:
        user, message = msg.split(": ", 1)
    except ValueError:
      logging.warning(f"Skipping invalid message: {msg}")
      continue

    length = len(message)
    total_characters += length

    if user in stats:
      stats[user]["messages"] += 1
      stats[user]["characters"] += length

  # Calculate final metrics
  results = {
    "total_messages": total_messages,
    "total_characters": total_characters
  }
  for nick, data in stats.items():
    msg_count = data["messages"]
    char_count = data["characters"]
    name = data["display_name"]

    results[name] = {
      "messages": msg_count,
      "percentage_messages": round((msg_count / total_messages) * 100, 2) if total_messages else 0,
      "percentage_characters": round((char_count / total_characters) * 100, 2) if total_characters else 0,
      "average_message_length": round(char_count / msg_count, 2) if msg_count else 0
    }

  return results


if __name__ == "__main__":

    # Your existing main code continues...
    with open(".data/martin_shrinked.txt", "r", encoding="utf-8") as fin:
      compressed_string = fin.read()
    
    logging.info("📊 Starting metadata analysis...")
    metadata = metadata_analysis(compressed_string, 2, ["Martin", "Tortoised"], ["M", "N"])
    print("\nMetadata Analysis Results:")
    print(json.dumps(metadata, indent=2))