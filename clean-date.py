import pandas as pd

# Load the CSV file
df = pd.read_csv('emp13feb2025-CLEANED.csv')

# Function to convert "Jan-Mar YYYY" to datetime
def parse_quarterly_date(date_str):
    # Remove any trailing annotations like "[r]"
    date_str = date_str.split('[')[0].strip()
    
    # Split the string into month range and year
    month_range, year = date_str.split()
    
    # Map the start month of the quarter to a month number
    month_map = {
        'Jan': 1, 'Apr': 4, 'Jul': 7, 'Oct': 10
    }
    start_month = month_range.split('-')[0]  # Extract the start month
    month = month_map[start_month]  # Get the corresponding month number
    
    # Create a datetime object for the first day of the quarter
    return pd.to_datetime(f'{year}-{month:02d}-01')

# Apply the function to the 'Date' column
df['Date'] = df['Date'].apply(parse_quarterly_date)

# Save the cleaned data to a new CSV file (optional)
df.to_csv('emp13feb2025-CLEANED-DATES.csv', index=False)

# Inspect the cleaned data
print(df.head())