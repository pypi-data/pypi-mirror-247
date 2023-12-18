from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def cut_video_into_pieces(input_path, output_folder):
    output_paths=[]
    # Ensure the output folder exists, create it if necessary
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    

    # Load the video clip
    video_clip = VideoFileClip(input_path)

    # Calculate the duration of each piece (3 seconds)
    piece_duration = 3
    
    if video_clip.size[0] > video_clip.size[1]:
        piece_duration = 3

    # Get the total duration of the video
    total_duration = video_clip.duration
    
        # If the video is shorter than the piece duration, copy the entire video
    if total_duration <= piece_duration:
        output_path = os.path.join(output_folder, "piece_1.mp4")
        video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        output_paths.append(output_path)

    else:

        # Calculate the number of pieces
        num_pieces = int(total_duration // piece_duration)

        for i in range(num_pieces):
            # Define the start and end times for each piece
            start_time = i * piece_duration
            end_time = (i + 1) * piece_duration

            # Create a subclip for each piece
            subclip = video_clip.subclip(start_time, end_time)

            # Define the output file path for each piece
            output_path = os.path.join(output_folder, f"piece_{i + 1}.mp4")

            # Write the subclip to the output file
            subclip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            output_paths.append(output_path)

        # Close the video clip
        video_clip.close()
    return output_paths


