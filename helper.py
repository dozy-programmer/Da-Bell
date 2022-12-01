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
start_stream = "./start.sh"
stop_stream  = "./stop.sh"
stream_dir = "/home/little_one/Desktop/DaRing/RPi_Cam_Web_Interface"
push_to_server = "./ngrok http 80"
desktop_dir = "/home/little_one/Desktop/DaRing"
photos_dir = "Photos"
shortclips_dir = "ShortClips"
stop_ngrok  = "killall ngrok"

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
