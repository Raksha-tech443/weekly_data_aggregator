from datetime import datetime, timedelta

def _fill_missing_days(data):
    """
    Fills in missing days in a week-long date range by calculating the
    mean of the previous and next available day's values.
    """
    if not data:
        return {}

    sorted_dates_str = sorted(data.keys())
    # Determine the week's Monday
    first_date_obj = datetime.strptime(sorted_dates_str[0], "%Y-%m-%d").date()
    monday_of_week = first_date_obj - timedelta(days=first_date_obj.weekday())

    # Create a full week's date range
    full_week_dates = {}
    for i in range(7):
        date_obj = monday_of_week + timedelta(days=i)
        date_str = date_obj.strftime("%Y-%m-%d")
        full_week_dates[date_str] = data.get(date_str)

    # Interpolate missing values
    dates_with_values = sorted([d for d, v in full_week_dates.items() if v is not None])
    
    for date_str, value in full_week_dates.items():
        if value is None:
            current_date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Find the nearest previous and next available dates
            prev_date_str = None
            next_date_str = None
            
            # Find previous
            for d in reversed(dates_with_values):
                if d < date_str:
                    prev_date_str = d
                    break
            
            # Find next
            for d in dates_with_values:
                if d > date_str:
                    next_date_str = d
                    break
            
            # Calculate the mean
            if prev_date_str and next_date_str:
                prev_val = full_week_dates[prev_date_str]
                next_val = full_week_dates[next_date_str]
                full_week_dates[date_str] = (prev_val + next_val) // 2
            elif prev_date_str: # Handle case of missing days at the start of the week
                full_week_dates[date_str] = full_week_dates[prev_date_str]
            elif next_date_str: # Handle case of missing days at the end of the week
                full_week_dates[date_str] = full_week_dates[next_date_str]

    return full_week_dates

def process_daily_data(data):
    """
    Fills in missing daily data and formats the output by day of the week.
    """
    filled_data = _fill_missing_days(data)

    # Sort the filled data by date
    sorted_filled_data = sorted(filled_data.items())

    # Map dates to day-of-week names
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    output = {}
    for date_str, value in sorted_filled_data:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        day_of_week = day_names[date_obj.weekday()]
        output[day_of_week] = value
    
    return output

if __name__ == "__main__":
    # Example from the first image
    input_data_1 = {
        '2020-01-01': 6,
        '2020-01-04': 12,
        '2020-01-05': 14,
        '2020-01-06': 2,
        '2020-01-07': 4
    }
    print("Example 1:")
    print(f"Input: {input_data_1}")
    output_1 = process_daily_data(input_data_1)
    print(f"Output: {output_1}")
    
    print("\n" + "-"*30 + "\n")

    # Example from the second image
    input_data_2 = {
        '2020-01-01': 4,
        '2020-01-02': 4,
        '2020-01-03': 6,
        '2020-01-04': 8,
        '2020-01-05': 2,
        '2020-01-06': -6,
        '2020-01-07': 2,
        '2020-01-08': -2
    }
    print("Example 2:")
    print(f"Input: {input_data_2}")
    output_2 = process_daily_data(input_data_2)
    print(f"Output: {output_2}")
