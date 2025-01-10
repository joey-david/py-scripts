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

def shrink_chat(input_file, start_date=None, end_date=None, start_time=None, end_time=None, output_file=None):
    """
    Compacts a chat log file by removing messages outside a specified date and time range.
    Detects all user names from the chat and assigns unique nicknames automatically.
    """
    def create_nickname(name, used):
        i = 1
        while i <= len(name):
            candidate = name[:i]
            if candidate not in used:
                return candidate
            i += 1
        # fallback if entire name is taken
        idx = 2
        candidate = name
        while candidate in used:
            candidate = f"{name}{idx}"
            idx += 1
        return candidate

    last_datetime = None
    result = []
    name_to_nickname = {}
    used_nicknames = set()

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
            result.append(" " + line.replace("<This message was edited>", ""))
            continue
        if end_datetime and message_datetime > end_datetime:
            break
        msgCount += 1
        if msgCount > 1000:
            raise Exception("Timeframe too wide, too many messages")
        pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}),?\s*(\d{1,2}:\d{1,2}(?:\s?(?:AM|PM))?)?\s*-\s*(.*?):\s*(.*)$'
        match = re.match(pattern, line)
        if not match:
            result.append(line)
            continue

        date_str, hour_str, user, message = match.groups()
        message = message.replace("<This message was edited>", "")

        if user not in name_to_nickname:
            nickname = create_nickname(user, used_nicknames)
            name_to_nickname[user] = nickname
            used_nicknames.add(nickname)
        else:
            nickname = name_to_nickname[user]

        if last_datetime is None or (message_datetime - last_datetime) > timedelta(hours=1):
            date_out = date_str
            hour_out = hour_str
            last_datetime = message_datetime
        else:
            date_out = ""
            hour_out = ""

        line_out = ((date_out + " " + hour_out).strip() + " - " if (date_out or hour_out) else "") + f"{nickname}: {message}"
        result.append(line_out)

    result_str = "\n".join(result)
    if output_file is not None:
        with open(output_file, "w", encoding="utf-8") as fout:
            fout.write(result_str)

    n_users = len(name_to_nickname)
    names = list(name_to_nickname.keys())
    usernames = list(name_to_nickname.values())
    return result_str, msgCount, n_users, names, usernames

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

    output_file = "./data/shrink_test_output.txt"
    start_date = "12/28/2024"
    end_date = "12/29/2024"
    start_time = "12:00 AM"
    end_time = "11:59 PM"
    string_test, msgCount, n_users, user_list, nickname_list = shrink_chat(
        input_file, start_date, end_date, start_time, end_time, output_file)
    print(f"Messsages: {msgCount}")
    print(f"Number of users: {n_users}")
    print(f"Users: {user_list}")
    print(f"Nicknames: {nickname_list}")