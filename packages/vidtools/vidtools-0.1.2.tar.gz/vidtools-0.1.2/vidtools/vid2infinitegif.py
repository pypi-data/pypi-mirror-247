import os
import json
from datetime import datetime

import time
import requests
import importlib

import importlib  
import os
import importlib
from .video_to_jpeg_frames import video_to_jpeg_frames  


from .main import function_handler
from .pic2vid import pic_2_vid_main
from .cut_video_into_pieces import cut_video_into_pieces

def download_content(url, save_path):
    response = requests.get(url, stream=True)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')
        if 'image' in content_type:
            save_path += ".jpg"
        elif 'video' in content_type:
            save_path += ".mp4"
        else:
            print(f"Unsupported content type: {content_type}")
            return

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Download successful. Content saved at {save_path}")
    else:
        print(f"Failed to download content. Status code: {response.status_code}")

# Provide the URL and the path where you want to save the content

import random
import string
import uuid

def generate_random_string(length=10):
    # Generate a random UUID
    random_uuid = uuid.uuid4()
    print("Random UUID:", random_uuid)
    return str(random_uuid)

     
def sleep_random_time():
    delay_seconds = random.uniform(1, 5)
    print(f"Sleeping for {delay_seconds:.2f} seconds before the next download.")

    # Introduce the random delay
    time.sleep(delay_seconds)    


from pathlib import Path

from pathlib import Path

def get_all_content_paths(directories):
    all_video_paths = []
    all_photo_paths = []
    all_gif_paths = []
    print("getting all directories")

    # Create a Path object for the specified directory
    base_dir = Path(directories)

    # Iterate over all files in the directory and its subdirectories
    for file_path in base_dir.rglob("*"):
        print(file_path)
        file_dir=os.path.dirname(file_path)

        # Check if the file is a regular file and has a video extension
        if file_path.is_file() and file_path.suffix.lower() in {'.mp4', '.avi', '.mkv', '.mov'}:
            all_video_paths.append({"full_path": file_path, "directory_path": file_dir, "type": "video"})
        # Check if the file is a regular file and has an image extension
        elif file_path.is_file() and file_path.suffix.lower() in {'.png', '.jpg', '.JPG', '.PNG'}:
            all_photo_paths.append({"full_path": file_path, "directory_path": file_dir, "type": "photo"})
        # Check if the file is a regular file and has a gif extension
        elif file_path.is_file() and file_path.suffix.lower() == '.gif':
            all_gif_paths.append({"full_path": file_path, "directory_path": file_dir, "type": "gif"})

    return {
        "video_paths": all_video_paths,
        "photo_paths": all_photo_paths,
        "gif_paths": all_gif_paths
    }

# Example usage:

import os
import shutil

def copy_and_continue_numbering(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    
    # Filter only the image files (assuming the format is input_xxx.jpg)
    image_files = [file for file in files if file.endswith('.jpg')]

    # Find the highest existing numbering
    existing_numbers = [int(file.split('_')[1].split('.')[0]) for file in image_files]
    max_existing_number = max(existing_numbers, default=0)

    # Sort the image files based on their current numbering
    image_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    # Reverse the order of the sorted files
    reversed_files = reversed(image_files)

    # Continue numbering and create copies
    for idx, file in enumerate(reversed_files, start=max_existing_number + 1):
        new_name = f"input_{str(idx).zfill(3)}.jpg"
        old_path = os.path.join(folder_path, file)
        new_path = os.path.join(folder_path, new_name)
        shutil.copy2(old_path, new_path)

def batch_content_create_infinte_gifs(directory_path, amount_of_vids_to_process, offset):

    # Get all content paths for the specified directory
    all_paths = get_all_content_paths(directory_path)
    
    processing_ammount_at_once=amount_of_vids_to_process
    
    count=offset
    # Print the list of content paths for each type
    for content_type, paths in all_paths.items():
        print(f"{content_type.capitalize()} Paths:")
        for path_info in paths:
            
            if path_info['type']=="video":
                if count<processing_ammount_at_once:
                    
                    count=count+1
                
                    print(f"  Full Path: {path_info['full_path']}, directory_path: {path_info['directory_path']} Type: {path_info['type']}")
                    # Example payload/body
                    base_path=f"./{path_info['directory_path']}"
                    
                    # Example usage:
                    input_video_path =f"./{path_info['full_path']}" 
                    output_folder_cuts = f"{base_path}/cuts_{uuid.uuid4()}"
                    print("input_video_path ", input_video_path)
                    print("output_folder_path ", output_folder_cuts)
                    output_paths=cut_video_into_pieces(input_video_path, output_folder_cuts)
                    output_path_gif_dir=f"{base_path}/gifs"
                    
                    
   
                        
                    for i in range(0,len(output_paths)):
                        try:
                            output_path_frames = f"{base_path}/frames_{i}_{uuid.uuid4()}"
                            if not os.path.exists(output_path_frames):
                                os.makedirs(output_path_frames)
                            video_to_jpeg_frames(path_video=output_paths[i], output_folder=output_path_frames) 
                            copy_and_continue_numbering(folder_path=output_path_frames)
                            # Use os.path.basename() to get the filename
                            filename_with_extension = os.path.basename(input_video_path)

                            # Use os.path.splitext() to split the filename and extension
                            filename_without_extension = os.path.splitext(filename_with_extension)[0]


                            filename = filename_without_extension

                            ourput_path_mp4=f"{base_path}/gif_{i}_{filename}"
                            
                            if not os.path.exists(ourput_path_mp4):
                                os.makedirs(ourput_path_mp4)
                            ourput_path_mp4=f"{ourput_path_mp4}/gif_{i}_{filename}"
                            pic_2_vid_main(input_path=output_path_frames,output_path=ourput_path_mp4)
                            payload = {
                                                "method": "vid2gif",
                                                "file_system": "local",
                                                "input_url":  f"./{ourput_path_mp4}.mp4",
                                                "output_url":  f"{output_path_gif_dir}",
                                            }

                            function_handler(payload)
                        # cleanup temp files
                            shutil.rmtree(output_path_frames)
                            shutil.rmtree(f"{base_path}/gif_{i}_{filename}")

                        except Exception as e:
                            print("an error occured with a video")
                            print(e)
                            exit()
                    shutil.rmtree(output_folder_cuts)

                        
                else:
                  
                    print("done creating gifs")
                    return
 