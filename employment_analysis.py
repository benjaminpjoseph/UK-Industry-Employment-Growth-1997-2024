import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned CSV file
df = pd.read_csv('emp13feb2025-CLEANED-DATES.csv')

# Clean and prepare the data
# Convert 'Date' to datetime with proper format
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')

# Extract year and quarter
df['Year'] = df['Date'].dt.year
df['Quarter'] = df['Date'].dt.quarter

# Filter for industries of interest
industries = ['Education', 'Human health & social work activities', 'Information & communication']
df_filtered = df[['Date', 'Year', 'Quarter'] + industries]

# Reshape the data and calculate year-on-year growth
df_long = df_filtered.melt(id_vars=['Date', 'Year', 'Quarter'], value_vars=industries, 
                           var_name='Industry', value_name='Employment')
df_long['YoY_Growth'] = df_long.groupby(['Industry', 'Quarter'])['Employment'].pct_change() * 100
df_long = df_long.dropna()

# Visualize year-on-year growth with improved styling
# Create the figure with improved dimensions and DPI
plt.figure(figsize=(14, 8), dpi=100)

# Define a more appealing color palette
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, orange, green

# Plot with improved styling
for i, industry in enumerate(industries):
    industry_data = df_long[df_long['Industry'] == industry]
    plt.plot(industry_data['Date'], industry_data['YoY_Growth'], 
             label=industry, 
             color=colors[i], 
             linewidth=2.5,
             marker='o',  # Add markers at data points
             markersize=4,
             alpha=0.85)  # Slight transparency

# Enhance the chart appearance
plt.title('Year-on-Year Employment Growth by Industry in the UK (1997-2024)', 
          fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Date', fontsize=12, labelpad=10)
plt.ylabel('Year-on-Year Growth (%)', fontsize=12, labelpad=10)

# Move the legend to the top left
plt.legend(fontsize=12, frameon=True, facecolor='white', edgecolor='lightgray', 
           loc='upper left')

# Add a horizontal line at y=0
plt.axhline(y=0, color='gray', linestyle='--', alpha=0.7, linewidth=1)

# Refine the axes
plt.gca().spines['top'].set_visible(False)  # Remove top border
plt.gca().spines['right'].set_visible(False)  # Remove right border
plt.tick_params(axis='both', which='major', labelsize=10)

# Set grid with light gray lines
plt.grid(True, alpha=0.3, linestyle='-', color='gray')

# Adjust y-axis limits to give some padding
y_min = df_long['YoY_Growth'].min() - 1
y_max = df_long['YoY_Growth'].max() + 1
plt.ylim([y_min, y_max])

# Format x-axis for better readability
plt.gcf().autofmt_xdate()  # Angle the date labels for better fit

# Adjust layout to fit everything nicely
plt.tight_layout()

# Save the chart with higher quality
plt.savefig('yoy_growth_by_industry.png', dpi=300, bbox_inches='tight')

# Display the chart
plt.show()