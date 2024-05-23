import pandas
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load the CSV data into DataFrames
df_gaussian_blur = pandas.read_csv('panda_graphs/0. All CSV Files for Graphs/image_processing_times_GaussianBlur_all_res.csv')
df_sobel_filter = pandas.read_csv('panda_graphs/0. All CSV Files for Graphs/image_processing_times_SobelFilter_all_res.csv')
df_sepia_tone = pandas.read_csv('panda_graphs/0. All CSV Files for Graphs/image_processing_times_SepiaTone_all_res.csv')

# Convert 'Time Taken (ms)' to seconds for all DataFrames
df_gaussian_blur['Time Taken (ms)'] = df_gaussian_blur['Time Taken (ms)'] / 1000
df_sobel_filter['Time Taken (ms)'] = df_sobel_filter['Time Taken (ms)'] / 1000
df_sepia_tone['Time Taken (ms)'] = df_sepia_tone['Time Taken (ms)'] / 1000

# Group the data by 'Resolution Category' and 'Method', and calculate the mean 'Time Taken (ms)' for all DataFrames
grouped_gaussian_blur = df_gaussian_blur.groupby(['Resolution Category', 'Method'])['Time Taken (ms)'].mean().reset_index()
grouped_sobel_filter = df_sobel_filter.groupby(['Resolution Category', 'Method'])['Time Taken (ms)'].mean().reset_index()
grouped_sepia_tone = df_sepia_tone.groupby(['Resolution Category', 'Method'])['Time Taken (ms)'].mean().reset_index()

# Create a helper function to map resolution categories to a numerical value
resolution_map = {'720p': 1, '1080p': 2, '2K': 3, '4K': 4, '8K': 5}
grouped_gaussian_blur['Resolution_Rank'] = grouped_gaussian_blur['Resolution Category'].map(resolution_map)
grouped_sobel_filter['Resolution_Rank'] = grouped_sobel_filter['Resolution Category'].map(resolution_map)
grouped_sepia_tone['Resolution_Rank'] = grouped_sepia_tone['Resolution Category'].map(resolution_map)

# Sort the data by 'Resolution_Rank' for all DataFrames
grouped_gaussian_blur = grouped_gaussian_blur.sort_values('Resolution_Rank')
grouped_sobel_filter = grouped_sobel_filter.sort_values('Resolution_Rank')
grouped_sepia_tone = grouped_sepia_tone.sort_values('Resolution_Rank')

# Create a line plot with separate lines for JS and WASM for each filter
plt.figure(figsize=(10, 6))
plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)  # Adjust plot margins

colors = ['darkorange', 'dodgerblue']
line_styles = ['-', '--', ':']
labels = ['Gaussian Blur', 'Sobel Filter', 'Sepia Tone']

for i, (grouped, label) in enumerate(zip([grouped_gaussian_blur, grouped_sobel_filter, grouped_sepia_tone], labels)):
    for j, (method, color) in enumerate(zip(['JS', 'WASM'], colors)):
        subset = grouped[grouped['Method'] == method]
        plt.plot(subset['Resolution_Rank'], subset['Time Taken (ms)'], marker='o', label=f'{label} - {method}',
                 color=color, linestyle=line_styles[i])

# Set labels and title with increased font size
plt.xlabel('Resolution (Ascending Order)', fontsize=14)
plt.ylabel('Average Time Taken (s)', fontsize=14)  # Change label to 's' for seconds
plt.title('Image Processing - Average Time Taken by Resolution for JS and WASM', fontsize=16)
plt.xticks(ticks=range(1, 6), labels=['720p', '1080p', '2K', '4K', '8K'])
plt.legend(fontsize=10)

# Format y-axis to show one decimal place
formatter = FuncFormatter(lambda y, _: '{:.1f}'.format(y))
plt.gca().yaxis.set_major_formatter(formatter)

plt.grid(True)
plt.show()