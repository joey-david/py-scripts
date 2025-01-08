import re
import tkinter as tk
from tkinter import filedialog, simpledialog
from datetime import datetime, timedelta

def binary_search(messages, start_datetime):
    low, high = 0, len(messages) - 1
    while low <= high:
        mid = (low + high) // 2
        message_datetime = extract_datetime(messages[mid])
        if message_datetime < start_datetime:
            low = mid + 1
        elif message_datetime > start_datetime:
            high = mid - 1
        else:
            return mid
    return low

def extract_datetime(line):
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}),?\s*(\d{1,2}:\d{1,2}(?:\s?(?:AM|PM))?)?\s*-\s*(.*?):\s*(.*)$'
    match = re.match(pattern, line)
    if not match:
        return None
    date_str, hour_str, _, _ = match.groups()
    try:
        message_datetime = datetime.strptime(date_str, "%m/%d/%Y")
    except ValueError:
        message_datetime = datetime.strptime(date_str, "%m/%d/%y")
    if hour_str:
        message_time = datetime.strptime(hour_str, "%I:%M %p").time()
        message_datetime = datetime.combine(message_datetime, message_time)
    return message_datetime

def parse_datetime(date_str, time_str):
    if date_str:
        dt = datetime.strptime(date_str, "%m/%d/%Y")
        if time_str:
            dt = datetime.combine(dt, datetime.strptime(time_str, "%I:%M %p").time())
        return dt
    return None

def shrink_chat(input_file, user1_name, user2_name, user1_nickname, user2_nickname, start_date=None, end_date=None, start_time=None, end_time=None):
    last_datetime = None
    output_file = input_file.replace(".txt", "_shrinked.txt")
    
    start_datetime = parse_datetime(start_date, start_time)
    end_datetime = parse_datetime(end_date, end_time)
    
    with open(input_file, "r", encoding="utf-8") as fin:
        messages = fin.readlines()
    
    start_index = binary_search(messages, start_datetime) if start_datetime else 0
    
    with open(output_file, "w", encoding="utf-8") as fout:
        for line in messages[start_index:]:
            line = line.strip()
            message_datetime = extract_datetime(line)
            if not message_datetime:
                line = line.replace(user1_name, user1_nickname).replace(user2_name, user2_nickname).replace("<This message was edited>", "")
                fout.write(" " + line)
                continue
            if end_datetime and message_datetime > end_datetime:
                break
            
            pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}),?\s*(\d{1,2}:\d{1,2}(?:\s?(?:AM|PM))?)?\s*-\s*(.*?):\s*(.*)$'
            match = re.match(pattern, line)
            if not match:
                fout.write(line + "\n")
                continue
            
            date_str, hour_str, user, message = match.groups()
            message = message.replace("<This message was edited>", "")
            user = user.replace(user1_name, user1_nickname).replace(user2_name, user2_nickname)
            
            if last_datetime is None or (message_datetime - last_datetime) > timedelta(hours=1):
                date_out = date_str
                hour_out = hour_str
                last_datetime = message_datetime
            else:
                date_out = ""
                hour_out = ""
            
            line_out = ((date_out + " " + hour_out).strip() + " - " if (date_out or hour_out) else "") + f"{user}: {message}"
            fout.write("\n" + line_out)

if __name__ == "__main__":
    def get_file_path():
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename(title="Select the chat file")

    def get_user_input(prompt):
        root = tk.Tk()
        root.withdraw()
        return simpledialog.askstring("Input", prompt)

    # input_file = get_file_path()
    # user1_name = get_user_input("Enter the first user's name:")
    # user2_name = get_user_input("Enter the second user's name:")
    # user1_nickname = get_user_input("Enter the first user's nickname:")
    # user2_nickname = get_user_input("Enter the second user's nickname:")
    # start_date = get_user_input("Enter the start date (MM/DD/YYYY) (optional):")
    # end_date = get_user_input("Enter the end date (MM/DD/YYYY) (optional):")
    # start_time = get_user_input("Enter the start time (HH:MM AM/PM) (optional):")
    # end_time = get_user_input("Enter the end time (HH:MM AM/PM) (optional):")

    # shrink_chat(input_file, user1_name, user2_name, user1_nickname, user2_nickname, start_date, end_date, start_time, end_time)
    shrink_chat("./joey-norma-31-12-2024.txt", "Joey", "Norma Saganeiti", "J", "N")
