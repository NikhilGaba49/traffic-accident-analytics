import re

# A function defining the boundaries for each time of day
def categorise_time_of_day(time):
    time_pattern = r"(\d{1,2}):\d\d:\d\d"
    string_match = re.search(time_pattern, time)
    if not string_match:
        return "Invalid"
    hour = int(string_match.group(1))
    if hour < 6:
        return "Late Night"
    elif hour < 12:
        return "Morning"
    elif hour < 18:
        return "Afternoon"
    return "Evening"