from PIL import Image
from moviepy.editor import VideoFileClip
import os
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename

print("Hello World, this is my videotoASCII_converter. Please select a video file preferably with mp4, avi, mov, mkv. Thank you for using this software for my Extended Project Qualification. By Karan Dahyea.")

ASCII_CHARACTERS = [
    " ", ".", ",", "-", "~", ":", ";", "o", "l", "I", "i", "1", "r", "t", "f", "j", "y", "n", "u", "v", "c", "x", "k",
    "d", "b", "p", "q", "g", "z", "s", "a", "h", "m", "w", "M", "W", "8", "B", "%", "#", "@",
]

def get_terminal_size():
    try:
        width, height = os.get_terminal_size()
        return width, height
    except OSError:
        return 80, 24  # Default if can't detect

def resize_image(image, max_width, max_height):
    width, height = image.size
    aspect_ratio = height / width
    # Adjust because characters are taller than wide (~2:1 height to width)
    adjusted_ratio = aspect_ratio * 0.5

    # Estimate new dimensions
    new_width = max_width
    new_height = int(new_width * adjusted_ratio)

    # If height too big, adjust width down
    if new_height > max_height:
        new_height = max_height
        new_width = int(new_height / adjusted_ratio)

    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def pixel_to_ascii(image, reverse=False):
    pixels = image.getdata()
    ascii_str = ""
    characters = ASCII_CHARACTERS[::-1] if reverse else ASCII_CHARACTERS
    for pixel in pixels:
        index = int(pixel / 255 * (len(characters) - 1))
        ascii_str += characters[index]
    return ascii_str

def frame_to_ascii(frame, max_width, max_height, reverse=False):
    image = Image.fromarray(frame)
    image = resize_image(image, max_width, max_height)
    image = grayify(image)
    ascii_image = pixel_to_ascii(image, reverse)

    width, height = image.size
    pixel_count = len(ascii_image)
    ascii_lines = [ascii_image[index:(index + width)] for index in range(0, pixel_count, width)]
    return ascii_lines  # return as list of lines instead of joined string

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

def animate_ascii_frames(video_path, reverse=False):
    try:
        clip = VideoFileClip(video_path)
    except Exception as e:
        print(f"Failed to load video: {e}")
        return 

    frame_rate = clip.fps
    frame_duration = 0.675925925 / frame_rate
    video_duration = clip.duration

    try:
        for i, frame in enumerate(clip.iter_frames()):
            start_time = time.time()

            terminal_width, terminal_height = get_terminal_size()
            max_height = terminal_height - 3  # leave space for timer and buffer
            max_width = terminal_width

            ascii_lines = frame_to_ascii(frame, max_width, max_height, reverse)

            clear_screen()

            # Print ascii art lines
            for line in ascii_lines:
                print(line)

            # Calculate current video time
            current_time = i * frame_duration
            time_str = f"Time: {format_time(current_time)} / {format_time(video_duration)}"

            # Print empty lines to fill up terminal height minus timer lines
            empty_lines_count = max(0, terminal_height - len(ascii_lines) - 2)
            for _ in range(empty_lines_count):
                print("")

            # Print timer centered
            padding = (terminal_width - len(time_str)) // 2
            print(" " * max(0, padding) + time_str)
            print("")  # extra blank line after timer for spacing

            elapsed_time = time.time() - start_time
            sleep_time = max(0, frame_duration - elapsed_time)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nAnimation interrupted by user.")
    except Exception as e:
        print(f"Error during animation: {e}")
    finally:
        clip.close()

    print("Animation finished. Please restart the code again <3. Made by Karan Dahyea")

def select_video_file():
    Tk().withdraw()
    video_file = askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
    return video_file

if __name__ == "__main__":
    video_path = select_video_file()
    if video_path:
        reverse_contrast = input("Type '1' for reverse contrast or anything else for normal: ")
        reverse = True if reverse_contrast == '1' else False
        animate_ascii_frames(video_path, reverse)
    else:
        print("No video file selected. :(")
