import pyrebase
from dataclasses import dataclass
import threading
import functools
from secrets_firebase import API_KEY, AUTH_DOMAIN, DATABASE_URL, STORAGE_BUCKET

@dataclass
class firebase: 
    # firebase config credentials
    config = {
      "apiKey": API_KEY,
      "authDomain": AUTH_DOMAIN,
      "databaseURL": DATABASE_URL,
      "storageBucket": STORAGE_BUCKET
    }
    
    # constants
    MP4_EXT = ".mp4"
    JPG_EXT = ".jpg"
    
    # initialize firebase using config credentials
    firebase = pyrebase.initialize_app(config)
    
    # get a reference to the database service
    db = firebase.database()
    # get a reference to the storage service
    storage = firebase.storage()
    
    # constants
    media_photos = "photos"
    media_shortclips = "shortclips"

    # decorator to automatically launch a function in a thread
    def threaded(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.start()
            return thread
        return wrapper

    @threaded
    def add_media_data(self, path, formatted_date, is_photo):
        # get rid of the file extention in path, because it contains the date
        date_created = path.replace(self.MP4_EXT, "").replace(self.JPG_EXT, "")
    
        media_data = {
            'path': path,
            'date_created': date_created,
            'date_created_formatted': formatted_date,
            'is_photo': is_photo
        }
        
        # determine if current file is a photo or a video
        media_type = self.media_photos if is_photo else self.media_shortclips
        # upload photo/video data to firebase
        self.db.child(media_type).push(media_data)
        
    # link to live camera feed changes everytime app starts
    # uploading to database for iOS app to get the link
    @threaded
    def add_link_to_live_feed(self, link):
        link_data = {
            'link': link,
        }
        
        self.db.child("link").update(link_data)
    
    @threaded
    # uploads a photo/video to firebase storage
    def upload_file(self, filename, file_path, is_photo):
        # determines if file is a photo or video
        # so it knows what folder to put it in in firebase storage
        media_type = self.media_photos if is_photo else self.media_shortclips
        # uploading media to firebase storage
        self.storage.child(f"{media_type}/{filename}").put(file_path)
        print(f"{media_type.upper()} file uploaded")
