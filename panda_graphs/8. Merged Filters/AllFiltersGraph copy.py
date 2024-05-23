import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load the CSV data into DataFrames
gaussian_blur_df = pd.read_csv('panda_graphs/1. Gaussian Blur/GaussianBlur.csv')
sobel_filter_df = pd.read_csv('panda_graphs/2. Sobel Filter/SobelFilter.csv')
sepia_tone_df = pd.read_csv('panda_graphs/3. Sepia Tone/SepiaTone.csv')

# Create a helper function to map resolution categories to a numerical value
resolution_map = {'720p': 1, '1080p': 2, '2K': 3, '4K': 4, '8K': 5}

# Add 'Resolution_Rank' column to each DataFrame
gaussian_blur_df['Resolution_Rank'] = gaussian_blur_df['Resolution Category'].map(resolution_map)
sobel_filter_df['Resolution_Rank'] = sobel_filter_df['Resolution Category'].map(resolution_map)
sepia_tone_df['Resolution_Rank'] = sepia_tone_df['Resolution Category'].map(resolution_map)

# Combine the DataFrames into a single DataFrame
df = pd.concat([gaussian_blur_df, sobel_filter_df, sepia_tone_df])

# Convert 'Time Taken (ms)' to seconds
df['Time Taken (ms)'] = df['Time Taken (ms)'] / 1000

# Create a line plot with two separate lines for JS and WASM
plt.figure(figsize=(10, 6))
colors = ['darkorange', 'dodgerblue']
labels = ['JS', 'WASM']

for i, (filter_data, filter_label) in enumerate([(gaussian_blur_df, 'Gaussian Blur'), 
                                                 (sobel_filter_df, 'Sobel Filter'), 
                                                 (sepia_tone_df, 'Sepia Tone')]):
    for method, color, label in zip(['JS', 'WASM'], colors, labels):
        subset = filter_data[filter_data['Method'] == method]
        grouped = subset.groupby(['Resolution_Rank'])['Time Taken (ms)'].mean().reset_index()
        plt.plot(grouped['Resolution_Rank'], grouped['Time Taken (ms)'], marker='o', 
                 color=color, alpha=0.3 + i*0.2, label=f'{filter_label} - {label}')

# Set labels and title
plt.xlabel('Resolution (Ascending Order)')
plt.ylabel('Average Time Taken (s)')  # Change label to 's' for seconds
plt.title('All Filters - Average Time Taken by Resolution for JS and WASM')
plt.xticks(ticks=range(1, 6), labels=['720p', '1080p', '2K', '4K', '8K'])
plt.legend()

# Format y-axis to show one decimal place
formatter = FuncFormatter(lambda y, _: '{:.1f}'.format(y))
plt.gca().yaxis.set_major_formatter(formatter)

plt.grid(True)
plt.show()