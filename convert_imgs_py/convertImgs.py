from PIL import Image
import os

def process_images(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over the images in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Open the image
            image_path = os.path.join(input_folder, filename)
            image = Image.open(image_path)

            # Get the original image dimensions
            width, height = image.size

            # Calculate the aspect ratio
            aspect_ratio = width / height

            # Resize the image to 4K resolution
            new_width = 3840
            new_height = int(new_width / aspect_ratio)
            resized_image_4k = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Save the 4K image
            output_filename_4k = os.path.splitext(filename)[0] + "_4K" + os.path.splitext(filename)[1]
            output_path_4k = os.path.join(output_folder, output_filename_4k)
            resized_image_4k.save(output_path_4k)

            # Resize the image to 2K resolution
            new_width = 2560
            new_height = int(new_width / aspect_ratio)
            resized_image_2k = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Save the 2K image
            output_filename_2k = os.path.splitext(filename)[0] + "_2K" + os.path.splitext(filename)[1]
            output_path_2k = os.path.join(output_folder, output_filename_2k)
            resized_image_2k.save(output_path_2k)

            # Resize the image to 1080p resolution
            new_width = 1920
            new_height = int(new_width / aspect_ratio)
            resized_image_1080p = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Save the 1080p image
            output_filename_1080p = os.path.splitext(filename)[0] + "_1080p" + os.path.splitext(filename)[1]
            output_path_1080p = os.path.join(output_folder, output_filename_1080p)
            resized_image_1080p.save(output_path_1080p)

            # Resize the image to 720p resolution
            new_width = 1280
            new_height = int(new_width / aspect_ratio)
            resized_image_720p = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Save the 720p image
            output_filename_720p = os.path.splitext(filename)[0] + "_720p" + os.path.splitext(filename)[1]
            output_path_720p = os.path.join(output_folder, output_filename_720p)
            resized_image_720p.save(output_path_720p)

            print(f"Processed: {filename}")

    print("Image processing completed.")

# Example usage
input_folder = "All_Images/TEST8K"
output_folder = "All_Images/ConvertedImgs"
process_images(input_folder, output_folder)