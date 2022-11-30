from gpiozero import LED
from gpiozero import Button
from threading import Thread
from picamera import PiCamera
import subprocess
import os
from datetime import datetime
from dataclasses import dataclass
from pyngrok import ngrok
import data_base
import mms

@dataclass
class Helper:
    # error message
    ERROR = "Error running commmand"
    
    # constants
    GPIO_PIN = 17
    start_stream = "./start.sh"
    stop_stream  = "./stop.sh"
    stream_dir = "/home/little_one/Desktop/DaRing/RPi_Cam_Web_Interface"
    push_to_server = "./ngrok http 80"
    desktop_dir = "/home/little_one/Desktop/DaRing"
    photos_dir = "Photos"
    shortclips_dir = "ShortClips"
    stop_ngrok  = "killall ngrok"
    
    # return a jpg filename based on current time and date
    def create_filename_name(is_photo):
        file_extension = ".jpg" if is_photo else ".h264"
        now = datetime.now()
        current_date = now.strftime("%m_%d_%Y")
        current_time = now.strftime("%I_%M_%S_%p")
        formatted_date = now.strftime("%b %d, %Y %I:%M:%S %p")
        return f"{current_date}_{current_time}{file_extension}", formatted_date


def wait_for_doorbell(firebase_database):
    print("Waiting for door bell to be pressed...")
    # button connected to GPIO pin 17
    button = Button(Helper.GPIO_PIN)

    # wait until button is pressed to continue
    button.wait_for_press()
    
    # stop stream
    stop_stream()
    
    # take a photo
    photo_path, photo_filename, formatted_date = take_photo()
    # upload photo data to firebase
    firebase_database.add_media_data(photo_filename, formatted_date, True)
    # upload photo to firebase storage
    firebase_database.upload_file(photo_filename, photo_path, True)
    
    # take a 3 second video
    shortclip_path, shortclip_filename, formatted_date = take_shortclip()
    # upload shortclip data to firebase
    firebase_database.add_media_data(shortclip_filename, formatted_date, False)
    # upload photo to firebase storage
    firebase_database.upload_file(shortclip_filename, shortclip_path, False)
    
    # send the owner a text message that doorbell was pressed
    mms.send_text_message()
    print("DoorBell pressed")
    
# start streaming camera to server
def start_stream():
    # change directory
    change_directory(Helper.stream_dir)
    # start stream
    stream_output = run_shell_command(Helper.start_stream)
    print("Streaming...")
    
    return push_camera_to_server()
    
# stop stream camera to server
def stop_stream():
    # change directory
    change_directory(Helper.stream_dir)
    # stop stream
    output = run_shell_command(Helper.stop_stream)
    print("Stopped streaming")
    
# change current working directory
def change_directory(new_dir):
    os.chdir(new_dir)

# connect camera feed to online server
# return public url link to camera feed
def push_camera_to_server():
    # change directory
    change_directory(Helper.desktop_dir)
    # kill all ngrok processes, there should not be any running
    run_shell_command(Helper.stop_ngrok)
    # start ngrok server
    print("Starting server...")
    start_server_result = ngrok.connect(bind_tls=True)
    return f"{start_server_result.public_url}/html"
    
# runs a command in shell
def run_shell_command(command):
    try:
        output = subprocess.Popen(command, shell=True)
        result = output.communicate()[0]
        # if out is not None, then return it
        if result is not None:
            return result
    except:
        return Helper.ERROR
    
# creates a folder in a desired directory
# returns new path
def create_folder(current_dir, folder_name):
    folder_path = os.path.join(current_dir, folder_name)
    if os.path.exists(folder_path) == False:
        os.path.join(folder_path, folder_name)
        os.makedirs(folder_path)
    return folder_path

# take a photo
# return photo path, photo filename, and its date (formatted)
def take_photo():
    # change directory
    change_directory(Helper.desktop_dir)
    # if Photos folder does not exist, create it
    photos_dir = create_folder(os.getcwd(), Helper.photos_dir)            
    # open camera
    camera = PiCamera()
    # take photo
    photo_filename, formatted_date = Helper.create_filename_name(True)
    photo_path = f"{photos_dir}/{photo_filename}"
    # take image and save to path
    camera.capture(photo_path)
    # close camera after using
    camera.close()
    return photo_path, photo_filename, formatted_date

# take a short video (3 seconds long called "shortclip")
# return video path, video filename, and its date (formatted)
def take_shortclip():
    # change directory
    change_directory(Helper.desktop_dir)
    # if ShortCLips folder does not exist, create it
    shortclips_dir = create_folder(os.getcwd(), Helper.shortclips_dir)            
    # open camera
    camera = PiCamera()
    
    # camera preferences
    camera.vflip = False
    camera.framerate = 15
    camera.resolution = (720, 440)
    
    shortclip_filename, formatted_date = Helper.create_filename_name(False)
    shortclip_path = f"{shortclips_dir}/{shortclip_filename}"
    # start recording 3 second video
    camera.start_recording(shortclip_path)
    print("Recording started...")
    # record 3 second video, 
    camera.wait_recording(6)
    camera.stop_recording()
    print("Recording stopped...")
    # close camera after using
    camera.close()
    
    # convert .h264 file to .mp4 and delete .h264 file
    new_shortclip_path = shortclip_path.replace(".h264", ".mp4")
    # convert .h264 file to mp4, redirect output so that no results show
    run_shell_command(f"MP4Box -add {shortclip_path} {new_shortclip_path} >/dev/null 2>&1")
    # remove .h264 file since a new .mp4 file was created
    run_shell_command(f"rm {shortclip_path}")
    # update path
    shortclip_path = new_shortclip_path 
    shortclip_filename = shortclip_filename.replace(".h264", ".mp4") 
    
    return shortclip_path, shortclip_filename, formatted_date
    
def main():
    # init database
    firebase_database = data_base.firebase()
    
    # start streaming
    server_link = start_stream()
    # upload public url link to firebase
    firebase_database.add_link_to_live_feed(server_link)
    
    # run doorbell again after it is pressed
    # and photo & video is taken
    while True:
        wait_for_doorbell(firebase_database)
    
    
if __name__ == '__main__':
    main()
    