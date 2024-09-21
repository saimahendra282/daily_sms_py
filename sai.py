import json
import os
from datetime import datetime, timedelta
from pushbullet import Pushbullet

# Get the API key from environment variables
api_key = os.getenv('PUSHBULLET_API_KEY')
if not api_key:
    raise ValueError("Pushbullet API key not found. Ensure it's set as an environment variable.")

pb = Pushbullet(api_key)

# Load the timetable data from a JSON file
with open('tt.json', 'r') as file:
    data = json.load(file)

# Mapping course codes to course names
course_mapping = {
    "22PH4102": "Applied Physics",
    "22CS2228F": "Cross PlatForm",
    "22CEC3101A": "CIS advanced",
    "22CEC3204": "Cloud Devops",
    "22SDCS03A": "JFSD advanced",
    # Add more mappings as needed
}

# Function to parse the time from the JSON format
def parse_time(time_str):
    return datetime.strptime(time_str, "%I:%M %p")

# Function to send a notification
def send_notification(title, message):
    pb.push_note(title, message)
    print(f"Notification sent: {title}")

# Check the timetable and send notifications
now = datetime.now()
current_day = now.strftime("%A").upper()

for entry in data:
    class_day = entry['day']
    class_start_time = parse_time(entry['startTime'])
    class_end_time = parse_time(entry['endTime'])
    time_before_class = class_start_time - timedelta(minutes=5)

    # Get the course name based on the course code
    course_code = entry['course']
    
    # Skip the SMS notification if the course field is null or empty
    if not course_code:
        print(f"Skipping entry: {entry['timeSlot']} due to missing course.")
        continue

    course_name = course_mapping.get(course_code, "No Course")  # Defaults to "No Course" if no match

    # Send upcoming class notification 5 minutes before class starts
    if current_day == class_day and time_before_class.time() <= now.time() < class_start_time.time():
        title = f"Upcoming Class: {course_name}"
        message = f"Room: {entry['room']}\nTime: {entry['timeSlot']}"
        send_notification(title, message)

    # Send current class notification when the class starts
    if current_day == class_day and class_start_time.time() <= now.time() < class_end_time.time():
        title = f"Current Class: {course_name} has started"
        message = f"Room: {entry['room']}\nTime: {entry['timeSlot']}"
        send_notification(title, message)
