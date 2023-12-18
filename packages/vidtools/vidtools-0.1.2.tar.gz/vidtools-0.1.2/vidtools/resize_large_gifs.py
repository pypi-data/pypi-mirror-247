import os
from PIL import Image

def resize_large_gifs(input_folder, output_folder, target_size_mb):
    # Ensure the output folder exists, create it if necessary
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all files in the input folder
    files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    for file in files:
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)

        # Check the size of the source GIF
        source_size_bytes = os.path.getsize(input_path)
        if source_size_bytes > target_size_mb * 1024 * 1024:
            # Open the input GIF
            with Image.open(input_path) as img:
                # Calculate the target width to achieve the target size
                target_width = int(img.width * (target_size_mb / (source_size_bytes / (1024 * 1024))) ** 0.5)

                # Resize the GIF while maintaining the aspect ratio
                resized_img = img.resize((target_width, int(img.height * (target_width / img.width))), Image.ANTIALIAS)

                # Save the resized GIF
                resized_img.save(output_path, optimize=True, quality=95)

# if __name__ == "__main__":
#     input_folder_path = "path/to/input/folder"
#     output_folder_path = "path/to/output/folder"
#     target_size_mb = 100

#     resize_large_gifs(input_folder_path, output_folder_path, target_size_mb)
