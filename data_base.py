import pyrebase
from dataclasses import dataclass
import helper

'''
This program upload data to firebase 
database and media to firebase storage. 
'''

@dataclass
class firebase:
    # check if credentials was added
    if not helper.is_credentials_added():
        raise helper.NoCredentialsAdded
    
    # initialize firebase using config credentials
    firebase = pyrebase.initialize_app(helper.config)
    # get a reference to the database service
    db = firebase.database()
    # get a reference to the storage service
    storage = firebase.storage()

    # add photo/video data to database
    @helper.threaded
    def add_media_data(self, path, formatted_date, is_photo):
        # get rid of the file extention in path, because it contains the date
        date_created = path.replace(helper.MP4_EXT, "").replace(helper.JPG_EXT, "")
        # create json with the media data
        media_data = {
            'path': path,
            'date_created': date_created,
            'date_created_formatted': formatted_date,
            'is_photo': is_photo
        }
        # determine if current file is a photo or a video
        media_type = helper.MEDIA_PHOTOS if is_photo else helper.MEDIA_SHORTCLIPS
        # upload photo/video data to firebase
        self.db.child(media_type).push(media_data)
        
    # link to live camera feed changes everytime app starts
    # uploading to database for iOS app to retrieve the link
    @helper.threaded
    def add_link_to_live_feed(self, link):
        # convert link string to JSON
        link_data = {
            helper.LINK_KEY: link,
        }
        # upload link to firebase
        self.db.child(helper.LINK_KEY).update(link_data)
    
    @helper.threaded
    # uploads a photo/video to firebase storage
    def upload_file(self, filename, file_path, is_photo):
        # determines if file is a photo or video
        # so it knows what folder to put it in in firebase storage
        media_type = helper.MEDIA_PHOTOS if is_photo else helper.MEDIA_SHORTCLIPS
        # uploading media to firebase storage
        self.storage.child(f"{media_type}/{filename}").put(file_path)
        print(f"{media_type} file uploaded")
