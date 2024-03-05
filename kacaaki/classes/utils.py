from datetime import datetime, timedelta

def find_next_weekday_date(weekday):
    # Map weekday names to their corresponding index (0 for Monday, 1 for Tuesday, ..., 6 for Sunday)
    weekday_map = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }

    # Get the current date
    today = datetime.now().date()

    # Calculate the difference in days between the target weekday and the current weekday
    current_weekday_index = today.weekday()
    target_weekday_index = weekday_map[weekday]
    days_until_next_weekday = (target_weekday_index - current_weekday_index) % 7

    # Calculate the date of the next occurrence of the target weekday
    next_weekday_date = today + timedelta(days=days_until_next_weekday)

    return next_weekday_date

# Example usage:

