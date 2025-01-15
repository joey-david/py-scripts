import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../backend'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../backend/llm'))

from backend import chat_shrinker
from backend.llm import llm_analysis

def getTextAnalysis(input_files, start_date, end_date, start_time, end_time):
    file = input_files.pop()
    start_date = "12/28/2024"
    end_date = "12/29/2024"
    start_time = "12:00 AM"
    end_time = "11:59 PM"
    compressed_string, msgCount, n_users, user_list, nickname_list = chat_shrinker.shrink_chat(
        file, start_date, end_date, start_time, end_time)
    json, response = llm_analysis.promptToJSON(prompt=compressed_string, users=user_list, nicknames=nickname_list, maxOutputTokens=2000)
    print(json)
    return json, response

def getTextMetadata(input_files):
    file = input_files.pop()
    platform = chat_shrinker.detect_platform(file)
    if (platform == "discord"):
        compressed_string, msgCount, n_users, user_list, nickname_list = chat_shrinker.shrink_discord_chat(file)
    elif (platform == "whatsapp"):
        compressed_string, msgCount, n_users, user_list, nickname_list = chat_shrinker.shrink_whatsapp_chat(file)
    else:
        raise Exception("Unsupported platform")
    metadata = chat_shrinker.metadata_analysis(compressed_string, n_users, user_list, nickname_list)
    return metadata