# Da Bell
This is a project made for CS578 (Wireless Networks) class at San Diego State.

Da Bell is a custom-made Ring Doorbell alternative that is low-lost and provides the same basic functionality, but without the audio and speaking capability. It runs on Raspberry Pi devices and hence, uses dependencies that are not available on Windows. Follow the [How to Use](#how-to-use)  section to get your Raspberry Pi device up and running.

#### Git

###### Basic Git Commands :
```shell
# CLONING AN EXISTING REPO 
# note: make sure you are in your desired directory
git clone https://github.com/Amark18/Da-Ring.git
# go inside project directory
cd Da-Ring
# set the remote url so when you push/pull, it goes to GitHub
git remote set-url origin https://github.com/Amark18/Da-Ring.git

# TO COMMIT CHANGES
# add files so that you can push to repo
git add .
# commit/confirm your changes
git commit -m "explain what you did, but keep it short and concise"
# push your changes to Github
git push

#### NICE TO KNOW COMMANDS ####
# see the status of the project files since last commit
git status

# pull and merge project files from Github Repo
git pull

# create and switch to new branch
git checkout -b <branch-name>

# to switch between branches
git checkout <branch-name>

```

For more git commands, see my [git cheat-sheet repo](https://github.com/Amark18/Git-Cheat-Sheet).


#### How to use:

Requirements:
- Camera
- Button

##### 1. Download dependencies
```shell
# make sure are in Da-Ring directory
# create virtual environment to hold all dependencies
python -m venv cs578
# activate virtual environment
. cs578/Scripts/activate
# install dependencies
pip install -r requirements.txt
```

##### 2. Download [RPi-Cam-Web-Interface](https://elinux.org/RPi-Cam-Web-Interface#Installation_Instructions) by following Installation Instructions

##### 3. Install Ngrok
1. Create an [account](https://ngrok.com/) to get an auth token.
2. Go to [Ngrok](https://ngrok.com/download) and download for Linux
3. Extract the file
4. Run
```shell
./ngrok authtoken <your-auth-token>
# then to start tunnel on port 80 for localhost
./ngrok http 80
# copy the link you see after running this command 
# and insert in you browser to see your camera feed
```

##### 4. Install [Camera](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)
- this part is optional as you may have enabled it already

##### 5. Run
```shell
# run door bell program
python doorbell.py
# program should be waiting for button input, press button
# the Raspberry Pi will take a photo and a 3 second video
# then it will send the user a message + photo that someone is at the door
# user can see the 3 second video taken on the app
```

##
