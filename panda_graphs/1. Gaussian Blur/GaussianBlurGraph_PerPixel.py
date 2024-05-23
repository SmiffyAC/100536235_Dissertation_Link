import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load the CSV data into a DataFrame
df = pd.read_csv('panda_graphs/0. All CSV Files for Graphs/image_processing_times_GaussianBlur_all_res.csv')

# Convert 'Time Taken (ms)' to nanoseconds (ns)
df['Time Taken (ns)'] = df['Time Taken (ms)'] * 1e6

# Create a helper function to map resolution categories to the number of pixels
resolution_map = {'720p': 1280 * 720, '1080p': 1920 * 1080, '2K': 2560 * 1440, '4K': 3840 * 2160, '8K': 7680 * 4320}

# Group the data by 'Resolution Category' and 'Method', and calculate the mean 'Time Taken (ns)'
grouped = df.groupby(['Resolution Category', 'Method'])['Time Taken (ns)'].mean().reset_index()

# Calculate the average time taken per pixel for each resolution category and method
grouped['Time per Pixel (ns)'] = grouped.apply(lambda row: row['Time Taken (ns)'] / resolution_map[row['Resolution Category']], axis=1)

# Add the 'Number of Pixels' column to the grouped DataFrame
grouped['Number of Pixels'] = grouped['Resolution Category'].map(resolution_map)

# Sort the data by 'Number of Pixels'
grouped = grouped.sort_values('Number of Pixels')

print(grouped)

# Create a scatter plot with lines and two separate colors for JS and WASM
plt.figure(figsize=(10, 6))
plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)  # Adjust plot margins

for method, color in [('JS', 'darkorange'), ('WASM', 'dodgerblue')]:
    subset = grouped[grouped['Method'] == method]
    plt.plot(subset['Number of Pixels'], subset['Time Taken (ns)'], marker='o', label=method, color=color)
    
    # Add labels to the points
    for x, y, label in zip(subset['Number of Pixels'], subset['Time Taken (ns)'], subset['Resolution Category']):
        plt.text(x, y, label, fontsize=10, ha='center', va='bottom')

# Set labels and title with increased font size
plt.xlabel('Number of Pixels', fontsize=14)
plt.ylabel('Time Taken (ns)', fontsize=14)
plt.title('Gaussian Blur - Time Taken to Apply Filter to a Single Pixel for JS and WASM', fontsize=16)

# Format x-axis labels to display the number of pixels in millions
def format_pixels(x, pos):
    return f'{x / 1e6:.1f}M'

plt.gca().xaxis.set_major_formatter(FuncFormatter(format_pixels))

plt.legend(fontsize=12)

plt.grid(True)
plt.show()