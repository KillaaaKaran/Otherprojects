from PIL import Image
from moviepy.editor import VideoFileClip
import os
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename

print("Hello World, this is my videotoASCII_converter. Please select a video file preferably with mp4, avi, mov, mkv. Thank you for using this software for my Extended Project Qualification. By Karan Dahyea.")

# Enhanced ASCII characters ordered from less intensity to more intensity
ASCII_CHARACTERS = [
    " ", ".", ",", "-", "~", ":", ";", "o", "l", "I", "i", "1", "r", "t", "f", "j", "y", "n", "u", "v", "c", "x", "k",
    "d", "b", "p", "q", "g", "z", "s", "a", "h", "m", "w", "M", "W", "8", "B", "%", "#", "@", "░", "░", "░", "▒", "▒", "▒", "▓", "▓", "█"
]

REVERSE_ASCII_CHARACTERS = [
    "█", "▓", "▓", "▒", "▒", "▒", "░", "░", "░", "@", "#", "%", "B", "8", "W", "M", "w",
    "m", "h", "a", "s", "z", "g", "q", "p", "b", "d", "k", "x", "c", "v", "u", "n", "y",
    "j", "f", "t", "r", "i", "I", "l", "o", ";", ":", "~", "-", ",", ".", " "
]

def resize_image(image, new_width):
    width, height = image.size
    ratio = width / height
    new_height = int(new_width / ratio)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def pixel_to_ascii(image, reverse=False):
    pixels = image.getdata()
    ascii_str = ""
    characters = REVERSE_ASCII_CHARACTERS if reverse else ASCII_CHARACTERS

    for pixel in pixels:
        index = int(pixel / 255 * (len(characters) - 1))
        ascii_str += characters[index]
    return ascii_str

def frame_to_ascii(frame, new_width, reverse=False):
    image = Image.fromarray(frame)
    image = resize_image(image, new_width)
    image = grayify(image)
    ascii_image = pixel_to_ascii(image, reverse)
    pixel_count = len(ascii_image)
    ascii_lines = [ascii_image[index:(index + new_width)] for index in range(0, pixel_count, new_width)]
    return "\n".join(ascii_lines)

def clear_screen():
    os.system('cls')  # Clears the screen in Windows Command Prompt

def get_terminal_size():
    try:
        # Try to get terminal size in a Windows Command Prompt environment
        width, height = os.get_terminal_size()
        return width, height
    except OSError:
        # Default size for the command prompt if there's an issue retrieving size
        return 80, 24

def animate_ascii_frames(video_path, reverse=False):
    try:
        clip = VideoFileClip(video_path)
    except Exception as e:
        print(f"Failed to load video: {e}")
        return 

    frame_rate = clip.fps

    terminal_width, terminal_height = get_terminal_size()
    new_width = int(terminal_width - 0.01)  # Ensure width is an integer

    try:
        for frame in clip.iter_frames():
            ascii_art = frame_to_ascii(frame, new_width, reverse)
            clear_screen()
            print(ascii_art)
            time.sleep(1 / frame_rate)  # Delay between frames to match the video frame rate
    except KeyboardInterrupt:
        print("\nAnimation interrupted by user.")
    except Exception as e:
        print(f"Error during animation: {e}")
    finally:
        clip.close()

    print("Animation finished. Please restart the code again <3. Made by Karan Dahyea")

def select_video_file():
    Tk().withdraw()  # Hide the root window
    video_file = askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
    return video_file

if __name__ == "__main__":
    video_path = select_video_file()
    if video_path:
        reverse_contrast = input("Reverse contrast? Type 1 for Yes, 2 for No (Be warned that reverse contrast is a bit laggy.): ")
        reverse = True if reverse_contrast == '1' else False
        animate_ascii_frames(video_path, reverse)
    else:
        print("No video file selected.")

