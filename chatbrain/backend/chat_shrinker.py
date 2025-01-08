import re
import tkinter as tk
from tkinter import filedialog, simpledialog
from datetime import datetime, timedelta

def search_start(messages, start_datetime):
    for i in range(len(messages) - 1, -1, -1):
        message_datetime = extract_datetime(messages[i])
        if message_datetime and message_datetime < start_datetime:
            print(message_datetime)
            print(f"found start at {i}")
            return i + 1
    return 0

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
        try:
            message_time = datetime.strptime(hour_str, "%I:%M %p").time()
        except ValueError:
            message_time = datetime.strptime(hour_str, "%I:%M").time()
        message_datetime = datetime.combine(message_datetime, message_time)
    return message_datetime

def parse_datetime(date_str, time_str):
    if date_str:
        try:
            dt = datetime.strptime(date_str, "%m/%d/%Y")
        except ValueError:
            dt = datetime.strptime(date_str, "%m/%d/%y")
        if time_str:
            try:
                dt = datetime.combine(dt, datetime.strptime(time_str, "%I:%M %p").time())
            except ValueError:
                dt = datetime.combine(dt, datetime.strptime(time_str, "%I:%M").time())
        return dt
    return None

def shrink_chat(input_file, user1_name, user2_name, user1_nickname, user2_nickname,
                 start_date=None, end_date=None, start_time=None, end_time=None, output_file=None):
    """
    Compacts a chat log file by removing messages outside a specified date and time range.
    Simplifies names to nicknames and removes "This message was edited" tags.
    
    Parameters:
    - input_file (str): Path to the input chat log file.
    - user1_name (str): Full name of the first user.
    - user2_name (str): Full name of the second user.
    - user1_nickname (str): Nickname for the first user.
    - user2_nickname (str): Nickname for the second user.
    - start_date (str, optional): Start date in MM/DD/YYYY format.
    - end_date (str, optional): End date in MM/DD/YYYY format.
    - start_time (str, optional): Start time in HH:MM AM/PM format.
    - end_time (str, optional): End time in HH:MM AM/PM format.
    - output_file (str, optional): Path to the output file to save the compacted chat log.
    
    Returns:
    - tuple: A string of the compacted chat log and the number of messages included.
    """
    last_datetime = None
    result = []

    start_datetime = parse_datetime(start_date, start_time)
    end_datetime = parse_datetime(end_date, end_time)
    
    with open(input_file, "r", encoding="utf-8") as fin:
        messages = fin.readlines()
    
    start_index = search_start(messages, start_datetime) if start_datetime else 0
    msgCount = 0
    
    for line in messages[start_index:]:
        line = line.strip()
        message_datetime = extract_datetime(line)
        if not message_datetime:
            line = line.replace(user1_name, user1_nickname).replace(user2_name, user2_nickname).replace("<This message was edited>", "")
            result.append(" " + line)
            continue
        if end_datetime and message_datetime > end_datetime:
            break
        msgCount += 1
        # TODO: Implement a nicer way to handle the message count limit
        if msgCount > 1000:
            raise Exception("Timeframe too wide, too many messages")
        pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}),?\s*(\d{1,2}:\d{1,2}(?:\s?(?:AM|PM))?)?\s*-\s*(.*?):\s*(.*)$'
        match = re.match(pattern, line)
        if not match:
            result.append(line)
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
        result.append(line_out)
    
    result_str = "\n".join(result)
    
    if output_file is not None:
        with open(output_file, "w", encoding="utf-8") as fout:
            fout.write(result_str)
    
    return result_str, msgCount

if __name__ == "__main__":
    def get_file_path():
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename(title="Select the chat file")

    def get_user_input(prompt):
        root = tk.Tk()
        root.withdraw()
        return simpledialog.askstring("Input", prompt)

    input_file = get_file_path()
    # user1_name = get_user_input("Enter the first user's name:")
    # user2_name = get_user_input("Enter the second user's name:")
    # user1_nickname = get_user_input("Enter the first user's nickname:")
    # user2_nickname = get_user_input("Enter the second user's nickname:")
    # start_date = get_user_input("Enter the start date (MM/DD/YYYY) (optional):")
    # end_date = get_user_input("Enter the end date (MM/DD/YYYY) (optional):")
    # start_time = get_user_input("Enter the start time (HH:MM AM/PM) (optional):")
    # end_time = get_user_input("Enter the end time (HH:MM AM/PM) (optional):")

    output_file = "../data/shrink_test_output.txt"
    start_date = "12/28/2024"
    end_date = "12/29/2024"
    start_time = "12:00 AM"
    end_time = "11:59 PM"
    string_test, msgCount = shrink_chat(input_file, "Joey", "Norma Saganeiti", "J", "N", start_date, end_date, start_time, end_time, output_file)
    print(msgCount)