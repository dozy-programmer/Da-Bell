# Da Bell
This is a project made for CS578 (Wireless Networks) class at San Diego State.

Da Bell is a custom-made Ring Doorbell alternative that is low-lost and provides the same basic functionality, but without the audio and speaking capability. It runs on Raspberry Pi devices and hence, uses dependencies that are not available on Windows. Follow the [installation](#installation) section to get your Raspberry Pi device up and running.

### Table of Contents
- [Installation](#installation)
- [iOS App](#ios-app)
- [Improvements](#improvements)

## Installation:

#### Hardware Requirements:
- Camera
  - RPi Cam Web Interface requires a PiCamera. 
- Button
  - Connect Raspberry Pi GPIO Pin 17 to button.

##### 1. Download dependencies
```shell
# make sure are in Da-Bell directory
# create virtual environment to hold all dependencies
python -m venv cs578
# activate virtual environment
. cs578/Scripts/activate
# install dependencies
pip install -r requirements.txt
```

##### 2. Download [RPi-Cam-Web-Interface](https://elinux.org/RPi-Cam-Web-Interface#Installation_Instructions) by following Installation Instructions
- Set settings to default during set-up.
- After set-up, it will ask to start camera, select <yes>.

##### 3. Install Ngrok
1. Create an [account](https://ngrok.com/) to get an auth token.
2. Go to [Ngrok](https://ngrok.com/download) and Download for Linux.
3. Extract/Unzip the file.
4. Required: place ngrok file inside Da Bell folder
5. Run the following in your command line:
```shell
./ngrok authtoken <your-auth-token>
# then to start tunnel on port 80 for localhost
./ngrok http 80
# copy the link you see after running this command 
# and insert in you browser to see your camera feed
```

##### 4. Run
```shell
# make sure you are Da-Bell directory
# to check your current directory
pwd
# run door bell program
python doorbell.py
# program should be waiting for button input, press button
# the Raspberry Pi will take a photo and a 3 second video
# then it will send the user a message + photo that someone is at the door
# user can see the photo and 3 second video taken on the app
```
##

## iOS App:

Da Bell also has an [iOS app](https://github.com/CollinLTT/CS578-Da-Bell) where you can do the following:
- view live feed
- see all photos taken when doorbell was pressed 
  - saved on firebase storage
- see all 3-second videos taken when doorbell was pressed 
  - saved on firebase storage
- see videos of all motion detected activites
  - saved on the Raspberry Pi
  
## Improvements:

Audio and speaker capabilities can be added to Da Bell, but was not included to keep costs to a minimum. In addition, this prototype was created to only show video because there isn't many low-cost options that did not include extra hardware (like a speaker and microphone, thus higher price). In essense, we wanted to make a modular door bell camera that can be improved by just plugging in hardware and enabling the respective feature. These features can be added without any issues to existing project. In conclusion, Da bell is a base prototype and anyone can improve Da Bell!
