# import pandas as pd
# import matplotlib.pyplot as plt
# import os

# # Display current directory
# print("Current Directory:", os.getcwd())


# # Load CSV file into DataFrame
# df = pd.read_csv('image_processing_times (41).csv')

# # Display the first few rows of the DataFrame
# print(df.head())

# # Check the data types and non-null counts
# print(df.info())

# # Get some basic statistics for numerical columns
# print(df.describe())


# # Assuming you want to plot 'Time Taken (ms)' against 'TrialNum' for each 'Method'
# plt.figure(figsize=(10, 5))
# for method in df['Method'].unique():
#     subset = df[df['Method'] == method]
#     plt.plot(subset['TrialNum'], subset['Time Taken (ms)'], marker='o', label=method)

# plt.title('Time Taken by Trial Number for Each Method')
# plt.xlabel('Trial Number')
# plt.ylabel('Time Taken (ms)')
# plt.legend()
# plt.grid(True)
# plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV data into a DataFrame
df = pd.read_csv('image_processing_times (53).csv')

# This is all filters on all images - ran on PC so spead is faster
# df = pd.read_csv('image_processing_times - 2024-05-02T231746.480.csv')

# Group the data by 'Resolution Category' and 'Method', and calculate the mean 'Time Taken (ms)'
grouped = df.groupby(['Resolution Category', 'Method'])['Time Taken (ms)'].mean().reset_index()

# Create a helper function to map resolution categories to a numerical value
resolution_map = {'720p': 1, '1080p': 2, '2K': 3, '4K': 4, '8K': 5}
grouped['Resolution_Rank'] = grouped['Resolution Category'].map(resolution_map)

# Sort the data by 'Resolution_Rank'
grouped = grouped.sort_values('Resolution_Rank')

print(grouped)

# Create a line plot with two separate lines for JS and WASM
plt.figure(figsize=(10, 6))
for method in ['JS', 'WASM']:
    subset = grouped[grouped['Method'] == method]
    plt.plot(subset['Resolution_Rank'], subset['Time Taken (ms)'], marker='o', label=method)

# Set labels and title
plt.xlabel('Resolution (Ascending Order)')
plt.ylabel('Average Time Taken (ms)')
plt.title('Average Time Taken by Resolution for JS and WASM')
plt.xticks(ticks=range(1, 6), labels=['720p', '1080p', '2K', '4K', '8K'])
plt.legend()

# Create a linear gradient for the background (optional)
# gradient_colors = plt.cm.Blues(np.linspace(0, 1, 256))
# gradient = np.tile(gradient_colors, (16, 1))
# plt.imshow(gradient, extent=[0, 5, 0, 12000], aspect='auto', origin='lower')

plt.grid(True)
plt.show()

# # Define the size ranges
# size_ranges = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000]

# # Create a new column 'Size Range' based on the 'Size (KB)' column
# df['Size Range'] = pd.cut(df['Size (KB)'], bins=size_ranges, include_lowest=True, right=False)

# # Group the data by 'Size Range' and 'Method', and calculate the mean 'Time Taken (ms)'
# grouped = df.groupby(['Size Range', 'Method'])['Time Taken (ms)'].mean().reset_index()

# # Sort the data by 'Size Range'
# grouped['Size Range'] = pd.Categorical(grouped['Size Range'], ordered=True, categories=grouped['Size Range'].unique())
# grouped = grouped.sort_values('Size Range')

# print(grouped)

# # Create a line plot with two separate lines for JS and WASM
# plt.figure(figsize=(12, 6))
# for method in ['JS', 'WASM']:
#     subset = grouped[grouped['Method'] == method]
#     plt.plot(subset['Size Range'].astype(str), subset['Time Taken (ms)'], marker='o', label=method)

# # Set labels and title
# plt.xlabel('Size Range (KB)')
# plt.ylabel('Average Time Taken (ms)')
# plt.title('Average Time Taken by Image Size Range for JS and WASM')
# plt.xticks(rotation=45)
# plt.legend()

# plt.grid(True)
# plt.show()