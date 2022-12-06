import threading
import functools
from datetime import datetime
from secrets_firebase import API_KEY, AUTH_DOMAIN, DATABASE_URL, STORAGE_BUCKET

'''
This is a helper class that contains constants 
and methods used throughout multiple files.
'''

# firebase config credentials
config = {
    "apiKey": API_KEY,
    "authDomain": AUTH_DOMAIN,
    "databaseURL": DATABASE_URL,
    "storageBucket": STORAGE_BUCKET
}

# constants
EMPTY = ""

# database_base.py constants
LINK_KEY = "link"
MP4_EXT = ".mp4"
JPG_EXT = ".jpg"
MEDIA_PHOTOS = "photos"
MEDIA_SHORTCLIPS = "shortclips"
# error message
ERROR = "Error running commmand"

# doorbell.py constants
GPIO_PIN = 17
H264_EXT = ".h264"
VIDEO_DURATION = 3 << 1
# commands
START_STREAM = "./start.sh"
STOP_STREAM  = "./stop.sh"
PUSH_TO_SERVER = "./ngrok http 80"
STOP_NGROK  = "killall ngrok"
# directories
STREAM_DIR = "/home/littleone/Desktop/Da-Bell/RPi_Cam_Web_Interface"
DESKTOP_DIR = "/home/littleone/Desktop/Da-Bell"
# folder names
PHOTOS_FOLDER = "Photos"
SHORTCLIPS_FOLDER = "ShortClips"

# see if credentials exist in secrets_firebase.py
def is_credentials_added():
    return EMPTY not in [API_KEY, AUTH_DOMAIN, DATABASE_URL, STORAGE_BUCKET]

# exceptions
class NoCredentialsAdded(Exception):
    def __str__(self):
        return "Credentials missing from secrets_firebase.py file!"

# create a curl command to start/stop motion detection
def get_motion_detection_command(is_starting):
    # 201 to start motion detection, 200 to stop
    command = 201 if is_starting else 200
    # adding curl to open link, therefore running command
    return f"curl localhost:80/html/cmd_pipe.php?cmd=md%{command}"

# create a filename based on current time and date
def create_filename_name(is_photo):
    file_extension = JPG_EXT if is_photo else H264_EXT
    now = datetime.now()
    current_date = now.strftime("%m_%d_%Y")
    current_time = now.strftime("%I_%M_%S_%p")
    formatted_date = now.strftime("%b %d, %Y %I:%M:%S %p")
    return f"{current_date}_{current_time}{file_extension}", formatted_date

# decorator to automatically launch a function in a thread
def threaded(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper
