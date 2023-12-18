import cv2

def video_to_jpeg_frames(path_video, output_folder):
    # Open the video file
    video_capture = cv2.VideoCapture(path_video)

    # Read and save frames as JPEG images
    success, image = video_capture.read()
    count = 0

    while success:
        cv2.imwrite(f'{output_folder}/input_{count:03d}.jpg', image)  # Save frame as JPEG
        success, image = video_capture.read()
        count += 1

    # Release the video capture object
    video_capture.release()
