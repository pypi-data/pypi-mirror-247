# from moviepy.video.io.VideoFileClip import VideoFileClip
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# from moviepy.editor import concatenate_videoclips
# from moviepy.video.io.VideoFileClip import VideoFileClip
# from moviepy.editor import concatenate_videoclips
# from moviepy.video.io.VideoFileClip import VideoFileClip
# from moviepy.editor import concatenate_videoclips
# from moviepy.editor import VideoClip
# from moviepy.editor import clips_array
# from moviepy.video.io.VideoFileClip import VideoFileClip
# from moviepy.editor import concatenate_videoclips
from .vid2gif import vid_2_gf_main
# def reverse_clip(clip):
#     # Reverse the playback direction of the clip
#     return clip.fx(vfx.speedx, factor=-1)


# def cut_and_concatenate(input_file, output_folder, segment_duration=3):
#     # Load the video clip
#     video_clip = VideoFileClip(input_file)

#     # Get the duration of the original video
#     original_duration = video_clip.duration

#     # Create a list to store the clips
#     clips = []

#     # Cut the video into segments of 'segment_duration' seconds
#     for start_time in range(0, int(original_duration), segment_duration):
#         end_time = min(start_time + segment_duration, original_duration)
        
#         # Cut the original segment
#         output_segment = f"{output_folder}/segment_{start_time}_{end_time}.mp4"
#         ffmpeg_extract_subclip(input_file, start_time, end_time, targetname=output_segment)

#         # Revert the segment
#         reversed_clip = reverse_clip(VideoFileClip(output_segment))
#         reversed_segment = f"{output_folder}/reversed_segment_{start_time}_{end_time}.mp4"
#         reversed_clip.write_videofile(reversed_segment, codec="libx264", audio_codec="aac")

#         # Add the original and reverted segments to the list
#         clips.extend([VideoFileClip(output_segment), VideoFileClip(reversed_segment)])
#         # clips.append(clip)

#         # Concatenate all the clips
#         final_clip = concatenate_videoclips(clips, method="compose")

#         # Save the final concatenated video with the same codec settings as the original video
#         final_output = f"{output_folder}/final_concatenated_{start_time}_{end_time}_video.mp4"
#         final_clip.write_videofile(final_output)

#         # Close the video clips
#         video_clip.close()
#         final_clip.close()



# Example usage:



def function_handler(body):
    # Extract parameters from the body
    method = body.get('method')
    file_system = body.get("file_system")
    input_url = body.get("input_url")
    output_url = body.get("output_url")
    max_length_seconds= body.get("max_length_seconds")
   

    # Validate required parameters
    if method == 'vid2gif' and file_system and input_url and output_url:
        # Call the vid_2_gf_main function with extracted parameters
        return vid_2_gf_main(input_dir=input_url, output_dir=output_url, file_system=file_system, mode="new")
    if method == 'crop_vid' and max_length_seconds and file_system and input_url and output_url:
        return  create_infinite_loop_gif(input_path=input_url, output_path=output_url, segment_length=3)

        
    else:
        return {'statusCode': 400, 'body': 'Invalid or missing parameters for the vid2gif method'}
