from gpiozero import LED
from gpiozero import Button
from picamera import PiCamera
from pyngrok import ngrok
import helper
import data_base
import mms
import subprocess
import os

# waits until a button ("doorbell") is pressed
# and takes a photo + video, then uploads to firebase
def wait_for_doorbell(firebase_database):
    print("Waiting for door bell to be pressed...")
    # button connected to GPIO PIN 17 
    button = Button(helper.GPIO_PIN)

    # wait until button is pressed to continue
    button.wait_for_press()
    print("DoorBell pressed")
    
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
    
    # resume steaming to online server
    resume_stream()
    
# start streaming camera to server
def start_stream():
    # change directory
    change_directory(helper.stream_dir)
    # start stream
    run_shell_command(helper.start_stream)
    print("Streaming...")
    return push_camera_to_server()

# start streaming camera to server
def resume_stream():
    # change directory
    change_directory(helper.stream_dir)
    # resume stream
    run_shell_command(helper.start_stream)
    print("Resuming Streaming...")
    
# stop streaming camera feed to server
def stop_stream():
    # change directory
    change_directory(helper.stream_dir)
    # stop stream
    run_shell_command(helper.stop_stream)
    print("Stopped streaming")

# enable motion detection    
def start_motion_detection():
    start_motion_command = "http://path.to.camera/html/cmd_pipe.php?cmd=md%200"

# disable motion detection
def stop_motion_detection():
    stop_motion_detection = "http://path.to.camera/html/cmd_pipe.php?cmd=md%201"
    
# change current working directory
def change_directory(new_dir):
    os.chdir(new_dir)

# connect camera feed to online server
# return public url link to camera feed
def push_camera_to_server():
    # change directory
    change_directory(helper.desktop_dir)
    # kill ngrok process, it should not be running
    run_shell_command(helper.stop_ngrok)
    # start ngrok server
    print("Starting server...")
    start_server_result = ngrok.connect(bind_tls=True)
    return f"{start_server_result.public_url}/html"
    
# runs a command in shell
# return result (if there is any)
def run_shell_command(command):
    try:
        output = subprocess.Popen(command, shell=True)
        result = output.communicate()[0]
        # if result is not None, then return the string
        if result is not None:
            return result
    except:
        return helper.ERROR
    
# creates a folder in a desired directory
# returns path of new folder created
def create_folder(current_dir, folder_name):
    folder_path = os.path.join(current_dir, folder_name)
    if os.path.exists(folder_path) == False:
        os.path.join(folder_path, folder_name)
        os.makedirs(folder_path)
    return folder_path

# take a photo
# return photo path, photo filename, and date (formatted)
def take_photo():
    # change directory
    change_directory(helper.desktop_dir)
    # if Photos folder does not exist, create it
    photos_dir = create_folder(os.getcwd(), helper.photos_dir)            
    # open camera
    camera = PiCamera()
    # create path to save photo to
    photo_filename, formatted_date = helper.create_filename_name(True)
    photo_path = f"{photos_dir}/{photo_filename}"
    # take photo and save to path
    camera.capture(photo_path)
    # close camera after using
    camera.close()
    return photo_path, photo_filename, formatted_date

# take a short video (3 seconds long called "shortclip")
# return video path, video filename, and its date (formatted)
def take_shortclip():
    # change directory
    change_directory(helper.desktop_dir)
    # if ShortCLips folder does not exist, create it
    shortclips_dir = create_folder(os.getcwd(), helper.shortclips_dir)      
          
    # open camera
    camera = PiCamera()
    # camera preferences
    camera.vflip = False
    camera.framerate = 15
    camera.resolution = (720, 440)
    # will need to add this as frame rate is off, currently too fast
    # camera.framerate = 25
    
    shortclip_filename, formatted_date = helper.create_filename_name(False)
    shortclip_path = f"{shortclips_dir}/{shortclip_filename}"
    # start recording 3 second video
    camera.start_recording(shortclip_path)
    print("Recording started...")
    # record 3 second video
    camera.wait_recording(helper.VIDEO_DURATION)
    camera.stop_recording()
    print("Recording stopped...")
    # close camera after using
    camera.close()
    
    # convert .h264 file to .mp4 and delete .h264 file
    new_shortclip_path = shortclip_path.replace(helper.H264_EXT, helper.MP4_EXT)
    # convert .h264 file to mp4, redirect output so that no results show in terminal
    run_shell_command(f"MP4Box -add {shortclip_path} {new_shortclip_path} >/dev/null 2>&1")
    # delete .h264 file since a new .mp4 file was created
    run_shell_command(f"rm {shortclip_path}")
    # update file name to be .mp4 since .h264 file no longer exists
    shortclip_filename = shortclip_filename.replace(helper.H264_EXT, helper.MP4_EXT) 
    return new_shortclip_path, shortclip_filename, formatted_date
    
def main():
    # init database
    firebase_database = data_base.firebase()
    
    # start streaming
    server_link = start_stream()
    # upload public url link to firebase
    firebase_database.add_link_to_live_feed(server_link)
    
    # run doorbell again after it is pressed
    # and photo-video are taken
    while True:
        wait_for_doorbell(firebase_database)
    
    
if __name__ == '__main__':
    main()
    