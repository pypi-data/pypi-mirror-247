from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import keyboard
import pyautogui
import pkg_resources
import moviepy.editor as mp

def block_keys():
    for i in range(150):
        keyboard.block_key(i)
        
def unblock_keys():
    for i in range(150):
        keyboard.unblock_key(i)

def path_converter(path):
    return pkg_resources.resource_filename('lasssi', path)

def play_video():
    video_path = path_converter('assets/lasssi_video.mp4')
    audio_path = path_converter('assets/lasssi_audio.mp3')
    
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = mp.AudioFileClip(audio_path)

    video_clip = video_clip.set_audio(audio_clip)

    screen_width, screen_height = pyautogui.size()

    video_clip = video_clip.resize((screen_width, screen_height))
    video_clip.preview(fps=25, fullscreen=True)

def main():
    block_keys()
    play_video()
    
if __name__ == "__main__":
    main()