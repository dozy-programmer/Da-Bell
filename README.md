# Da Bell
This is a project made for CS578 (Wireless Networks) class at San Diego State.

Da Bell is a custom-made Ring Doorbell alternative that is low-lost and provides the same basic functionality, but without the audio and speaking capability. 

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

```shell
# make sure are in Da-Ring directory
# create virtual environment to hold all dependencies
python -m venv cs578
# activate virtual environment
. cs578/Scripts/activate
```
