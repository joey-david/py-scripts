import re
import tkinter as tk
from tkinter import filedialog, simpledialog
from datetime import datetime

def shrink_chat(input_file, user1_name, user2_name, user1_nickname, user2_nickname, start_date, end_date=None, start_time=None, end_time=None):
    
    last_date = None
    last_hour = None
    output_file = input_file.replace(".txt", "_shrinked.txt")
    
    start_datetime = datetime.strptime(start_date, "%m/%d/%Y")
    end_datetime = datetime.strptime(end_date, "%m/%d/%Y") if end_date else None
    start_time = datetime.strptime(start_time, "%I:%M %p").time() if start_time else None
    end_time = datetime.strptime(end_time, "%I:%M %p").time() if end_time else None
    
    with open(input_file, "r", encoding="utf-8") as fin, open(output_file, "w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            
            # Expected format: "M/D/YY, H:MM AM/PM - Name: Message"
            pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}),?\s*(\d{1,2}:\d{1,2}(?:\s?(?:AM|PM))?)?\s*-\s*(.*?):\s*(.*)$'
            match = re.match(pattern, line)
            if not match:
                # Just write out lines that don't match the pattern
                fout.write(line + "\n")
                continue
            
            date_str, hour_str, user, message = match.groups()
            message_datetime = datetime.strptime(date_str, "%m/%d/%Y")
            
            if hour_str:
                message_time = datetime.strptime(hour_str, "%I:%M %p").time()
            else:
                message_time = None
            
            # Check if the message is within the date and time range
            if message_datetime < start_datetime or (end_datetime and message_datetime > end_datetime):
                continue
            if start_time and message_time and message_time < start_time:
                continue
            if end_time and message_time and message_time > end_time:
                continue
            
            # Remove "<This message was edited>"
            message = message.replace("<This message was edited>", "")
            
            # Replace user names
            user = user.replace(user1_name, user1_nickname).replace(user2_name, user2_nickname)
            
            # Print the date only if new
            date_out = date_str if date_str != last_date else ""
            # Print the hour only if new hour
            hour_out = ""
            if hour_str:
                hour_key = hour_str.split(":")[0] + hour_str[-2:].upper()  # e.g. "10AM"
                if hour_key != last_hour:
                    hour_out = hour_str
                    last_hour = hour_key
            
            line_out = ((date_out + " " + hour_out).strip() + " - " if (date_out or hour_out) else "") + f"{user}: {message}"
            fout.write(line_out + "\n")
            
            last_date = date_str

if __name__ == "__main__":
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

    input_file = get_file_path()
    user1_name = get_user_input("Enter the first user's name:")
    user2_name = get_user_input("Enter the second user's name:")
    user1_nickname = get_user_input("Enter the first user's nickname:")
    user2_nickname = get_user_input("Enter the second user's nickname:")
    start_date = get_user_input("Enter the start date (MM/DD/YYYY):")
    end_date = get_user_input("Enter the end date (MM/DD/YYYY) (optional):")
    start_time = get_user_input("Enter the start time (HH:MM AM/PM) (optional):")
    end_time = get_user_input("Enter the end time (HH:MM AM/PM) (optional):")

    shrink_chat(input_file, user1_name, user2_name, user1_nickname, user2_nickname, start_date, end_date, start_time, end_time)