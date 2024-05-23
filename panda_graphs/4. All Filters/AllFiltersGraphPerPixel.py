import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load the CSV data into DataFrames
df_gaussian_blur = pd.read_csv('panda_graphs/0. All CSV Files for Graphs/image_processing_times_GaussianBlur_all_res.csv')
df_sobel_filter = pd.read_csv('panda_graphs/0. All CSV Files for Graphs/image_processing_times_SobelFilter_all_res.csv')
df_sepia_tone = pd.read_csv('panda_graphs/0. All CSV Files for Graphs/image_processing_times_SepiaTone_all_res.csv')

# Convert 'Time Taken (ms)' to nanoseconds (ns) for all DataFrames
df_gaussian_blur['Time Taken (ns)'] = df_gaussian_blur['Time Taken (ms)'] * 1e6
df_sobel_filter['Time Taken (ns)'] = df_sobel_filter['Time Taken (ms)'] * 1e6
df_sepia_tone['Time Taken (ns)'] = df_sepia_tone['Time Taken (ms)'] * 1e6

# Create a helper function to map resolution categories to the number of pixels
resolution_map = {'720p': 1280 * 720, '1080p': 1920 * 1080, '2K': 2560 * 1440, '4K': 3840 * 2160, '8K': 7680 * 4320}

# Group the data by 'Resolution Category' and 'Method', and calculate the mean 'Time Taken (ns)' for all DataFrames
grouped_gaussian_blur = df_gaussian_blur.groupby(['Resolution Category', 'Method'])['Time Taken (ns)'].mean().reset_index()
grouped_sobel_filter = df_sobel_filter.groupby(['Resolution Category', 'Method'])['Time Taken (ns)'].mean().reset_index()
grouped_sepia_tone = df_sepia_tone.groupby(['Resolution Category', 'Method'])['Time Taken (ns)'].mean().reset_index()

# Calculate the average time taken per pixel for each resolution category and method for all DataFrames
grouped_gaussian_blur['Time per Pixel (ns)'] = grouped_gaussian_blur.apply(lambda row: row['Time Taken (ns)'] / resolution_map[row['Resolution Category']], axis=1)
grouped_sobel_filter['Time per Pixel (ns)'] = grouped_sobel_filter.apply(lambda row: row['Time Taken (ns)'] / resolution_map[row['Resolution Category']], axis=1)
grouped_sepia_tone['Time per Pixel (ns)'] = grouped_sepia_tone.apply(lambda row: row['Time Taken (ns)'] / resolution_map[row['Resolution Category']], axis=1)

# Add the 'Number of Pixels' column to the grouped DataFrames
grouped_gaussian_blur['Number of Pixels'] = grouped_gaussian_blur['Resolution Category'].map(resolution_map)
grouped_sobel_filter['Number of Pixels'] = grouped_sobel_filter['Resolution Category'].map(resolution_map)
grouped_sepia_tone['Number of Pixels'] = grouped_sepia_tone['Resolution Category'].map(resolution_map)

# Sort the data by 'Number of Pixels' for all DataFrames
grouped_gaussian_blur = grouped_gaussian_blur.sort_values('Number of Pixels')
grouped_sobel_filter = grouped_sobel_filter.sort_values('Number of Pixels')
grouped_sepia_tone = grouped_sepia_tone.sort_values('Number of Pixels')

# Create subplots for each filter
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

# Plot Gaussian Blur
for method, color in [('JS', 'darkorange'), ('WASM', 'dodgerblue')]:
    subset = grouped_gaussian_blur[grouped_gaussian_blur['Method'] == method]
    ax1.plot(subset['Number of Pixels'], subset['Time per Pixel (ns)'], marker='o', label=method, color=color)
    for x, y, label in zip(subset['Number of Pixels'], subset['Time per Pixel (ns)'], subset['Resolution Category']):
        ax1.text(x, y, label, fontsize=8, ha='center', va='bottom')

ax1.set_xlabel('Number of Pixels', fontsize=12)
ax1.set_ylabel('Time per Pixel (ns)', fontsize=12)
ax1.set_title('Gaussian Blur', fontsize=14)
ax1.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x / 1e6:.1f}M'))
ax1.legend(fontsize=10)
ax1.grid(True)

# Plot Sobel Filter
for method, color in [('JS', 'darkorange'), ('WASM', 'dodgerblue')]:
    subset = grouped_sobel_filter[grouped_sobel_filter['Method'] == method]
    ax2.plot(subset['Number of Pixels'], subset['Time per Pixel (ns)'], marker='o', label=method, color=color)
    for x, y, label in zip(subset['Number of Pixels'], subset['Time per Pixel (ns)'], subset['Resolution Category']):
        ax2.text(x, y, label, fontsize=8, ha='center', va='bottom')

ax2.set_xlabel('Number of Pixels', fontsize=12)
ax2.set_title('Sobel Filter', fontsize=14)
ax2.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x / 1e6:.1f}M'))
ax2.legend(fontsize=10)
ax2.grid(True)

# Plot Sepia Tone
for method, color in [('JS', 'darkorange'), ('WASM', 'dodgerblue')]:
    subset = grouped_sepia_tone[grouped_sepia_tone['Method'] == method]
    ax3.plot(subset['Number of Pixels'], subset['Time per Pixel (ns)'], marker='o', label=method, color=color)
    for x, y, label in zip(subset['Number of Pixels'], subset['Time per Pixel (ns)'], subset['Resolution Category']):
        ax3.text(x, y, label, fontsize=8, ha='center', va='bottom')

ax3.set_xlabel('Number of Pixels', fontsize=12)
ax3.set_title('Sepia Tone', fontsize=14)
ax3.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x / 1e6:.1f}M'))
ax3.legend(fontsize=10)
ax3.grid(True)

plt.tight_layout()
plt.show()