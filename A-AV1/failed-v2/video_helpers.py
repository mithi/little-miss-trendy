from moviepy.editor import VideoFileClip
from moviepy.editor import ImageSequenceClip
from IPython.display import HTML
import numpy as np
import io
import base64

# IMPORTANT: 
# using the function make_video_from_image_directory() 
# please make sure the directory contains ONLY JPG files and no other files and hidden files (like .DS_STORE)
def make_video_from_image_directory(image_path, video_filename, my_fps):
    
    print()
    print("Creating video from images in:", image_path)
    print("which can be found in:", video_filename)
    print("with fps:", my_fps, "...")
    print()
    
    clip = ImageSequenceClip(image_path, fps=my_fps)
    clip.write_videofile(video_filename)
    
    print()
    print("...Video created.")
    print()

    
def prepare_video_for_showing(video_file_path):

    video = io.open(video_file_path, 'r+b').read()
    encoded_video = base64.b64encode(video)
    
    specs = '''<video alt="test" controls>
                <source src="data:video/mp4;base64,{0}" type="video/mp4" />
             </video>'''.format(encoded_video.decode('ascii'))

    return specs