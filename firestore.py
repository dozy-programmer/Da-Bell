import firebase_admin
from firebase_admin import credentials, firestore, storage
from dataclasses import dataclass
import datetime
from secrets_firebase_private import FIREBASE_CRED, STORAGE_BUCKET

@dataclass
class firestore: 
    COLLECTION_PHOTOS = "Photos"
    
    # init firestore
    cred = credentials.Certificate(FIREBASE_CRED)
    # initialize firestore and storage
    firebase_admin.initialize_app(cred,{'storageBucket': STORAGE_BUCKET})
    db = firestore.client()
    photos_ref = db.collection(COLLECTION_PHOTOS)
        
    def add_media_data(self, path, is_photo):
        photos_ref = self.photos_ref.document()
        photos_ref.set({
            'path': path,
            'date_created': datetime.datetime.now(),
            'date_created_formatted': u'Nov 12, 2022',
            'is_photo': is_photo
        })
        
    def upload_file(self, filename):
        bucket = storage.bucket()
        blob = bucket.blob(filename)
        blob.upload_from_filename(filename)
            
def main():
    firestore_database = firestore()
    #firestore_database.add_media_data()
    #firestore_database.upload_file("project_info.txt")
    
if __name__ == "__main__":
    main()