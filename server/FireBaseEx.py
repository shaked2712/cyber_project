import pyrebase
import face_recognition
import os
import threading
import Search_img

config={
    "apiKey": "AIzaSyDz5UR-f0h0WJ9RO9i8cxcj23x2OIwid78",
    "authDomain": "cyberproject-22962.firebaseapp.com",
    "projectId": "cyberproject-22962",
    "storageBucket": "cyberproject-22962.appspot.com",
    "databaseURL":"https://cyberproject-22962-default-rtdb.firebaseio.com/",
   "serviceAccount":{
        "type": "service_account",
        "project_id": "cyberproject-22962",
        "private_key_id": "cf9f9f9b9bc9a0046b8b5f59e030d59f4be1d479",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC2Y2YCIohY5ws+\ncnS8mh2BZAWAisk3gig4/zjU2H5k8+K+2epjVPCxC24ZMe2PZnXrE6EdSWe4ijCu\nS32nQdm3z6y9aGe7cv6tvmMJZ0eoKGzy2YmQvg9ujM7MmRBFUIy7s2B/wl8a0NnE\nwa2DOYkE6NeWvFqSi4wSa03Ni8y4QqGEpINsq+EW51Wj6Oixlq+n3Z6uigC9NlEt\nMNXN/kpgg4oX0FTSRFODJNwzJdVHdMGKEUQmQ+bhe+Py6yibijGsn2vC0A9cBdwX\nMRMOviXtusOeqhWiY+MQrEnIbeZdMWOtkq8qTvVD0DLx+uadxrAFTd4scFkJ2iI1\nkwboz3MlAgMBAAECggEAHueu5FO3qODVjepVD5RJxaAOMp7Rw78hU68jkSVyHWca\nF97TEavV8RoPuOM17uOcvY2g8lZ65dE8uHwAObQ10Si2i43CbgfpUcV+AJzojnzz\nIR9taQJbmQ7xB8gz8prYjgGyK1PjS6byD54F6cN5DUTrKxaVfll5DbHzCA5VTS9r\n4aLOJwySMBQn5aTizpAkhANHOH25L3wkYVtJt/+11FZC0qXQnZdBjUUFstqYfEDQ\nkvQkTYa9H/XW4r6GQtg2puNUJfNqBnrDUu3rw4rVK4dTK9ZTwKjmMbtRyRyxOUvC\nslOcVp6EUbdqrQCVzsV+P/QENBfsCSo0BkD3V4TtIQKBgQDidYdntrG1Wgg7sC+a\nTvXzKRUX9jM+J1eYg7IGhqZysSTYbtjL/hw7WRXPRvFMAOsBqFUCw4ZXxlrLCKZM\n4vYpnrMgg8GkhEjn0pb+NOc1aIqPI0K3N02L2kB3up7oiGbp8UY3wfKHtYQFvs43\nHLBC6I5UmzfB3HTESwuSGpsF2QKBgQDOLiZbdHHgwWeqfzh6OJqgIwnUQGWo2pUe\nA2KpHrD9vnG7WCEpW7WWpGi/ypCIGnRWa83uT759OVooAExCEP9UinQ8GCFj6ASn\nDHCd43BWtFe5ZmoTUB+oRjk1PVrvxPQ/RZ3N06yy5Jb/G6G6eBcSOnT7PMyb2uKJ\n3fczsYtMLQKBgQCfcqEkJT56simZ3TOnMnF6BDMV7AOof4rtl8yBS81mc9O9kE6V\nUxYNs2vnxcuf+AV/5UX17DVrF/5VdoGhISyxoUv+WMa/T2UF1QD7e8RPlov4vJr8\n5bN0BPffVUcN8vyDO551I9ngM64BXZdUtp5kfdm5OJDJrq+Ihk5fUNxWAQKBgQCb\nI6ynCjKZ/M1lRD8Z8DehIVxHAoG8EWU85S06tiZVeBSZ9FFXjnNPu7w5/FDOqKE7\nWfjlRcm+7gXBrZ+z4phNY7TcdwfA5heCHuEqXLXt99s+XSqaB6MaemSXg+hGHDvw\n1BBOjOUY4tofcQo7hhtOEwBs/y2yZHwrYwKcOg7nrQKBgQDPBz9NETdwFD3DkyVT\nV6NgKDRNPbH/V4bKOBOO/kSKq3piUTnQ1Tm3ksYnRg1uvPrPb6DLjbYMSPB9shq8\nu5QsW0YXJtIzHOL+Xo49m7+U2f3sJXOzsl/VHj3dTv36DgnK7ZOIFRpEJE2uLjHl\n7HsrWEYtXgDazs5LfY25jIZhRw==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-94t2g@cyberproject-22962.iam.gserviceaccount.com",
        "client_id": "113020417083856001200",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-94t2g%40cyberproject-22962.iam.gserviceaccount.com"
        }
}

def uploadImage(user_email,name,path):
    # initialize our app
    firebase_storage=pyrebase.initialize_app(config)
    # reference to our storage
    storage=firebase_storage.storage()
    # uploading image
    storage.child("known").child(user_email).child(name).put(path)


# Downloading images from known folder to the images directory
def DownloadKnown(user_email):
    # initialize our app
    firebase_storage = pyrebase.initialize_app(config)
    # reference to our storage
    storage = firebase_storage.storage()
    known_files = storage.child("known").child(user_email).list_files()
    for file in known_files:
        if file.name.startswith(f"known/{user_email}"):
            file_name = file.name
            file_name = file_name.split("/")[-1]
            # construct new file path
            new_file_path = f"images/{file_name}"
            # download file to new file path
            file.download_to_filename(new_file_path)


# find images that are similar to the img we got and prepare a list of similar and different images
def compare_file_to_image(file,encodingOfImage):
    file_name = file.name
    if file_name.endswith((".jpg", ".jpeg", ".png", ".gif")):
        # replace spaces with underscores in the file name
        new_file_name = file_name.replace(" ", "_")
        new_file_name = new_file_name.split("/")[-1]
        # construct new file path
        new_file_path = f"celebsIMG/{new_file_name}"
        # download file to new file path
        file.download_to_filename(new_file_path)
        # load the downloaded image and compare faces
        img = face_recognition.load_image_file(new_file_path)
        try:
            encode = face_recognition.face_encodings(img)[0]
            results = face_recognition.compare_faces([encode], encodingOfImage)
            if results[0]==True:

                file.download_to_filename(f"similar/{new_file_name}")
            else:

                file.download_to_filename(f"differentFace/{new_file_name}")
        except IndexError as e:
            print(file_name)
            print(e)

# Download images from the celebs folder in the database
def DownloadImagesFromCelebs(encodingOfImage):
    # initialize our app
    firebase_storage = pyrebase.initialize_app(config)
    # reference to our storage
    storage = firebase_storage.storage()
    # create directories
    if not os.path.exists("celebsIMG"):
        os.mkdir("celebsIMG")
    if not os.path.exists("similar"):
        os.mkdir("similar")
    if not os.path.exists("differentFace"):
        os.mkdir("differentFace")
    # downloading images
    all_files = storage.child("celebs").list_files()
    for file in all_files:
        if file.name.startswith("celebs/") and (len(os.listdir("similar/"))<1 or len(os.listdir("differentFace/"))<4):
            th=threading.Thread(target=compare_file_to_image,args=(file,encodingOfImage))
            th.start()
            th.join()

def deleteIMG(filename):
    # initialize our app
    firebase_storage = pyrebase.initialize_app(config)
    # reference to our storage
    storage = firebase_storage.storage()
    # delete the image
    storage.delete(f"celebs/{filename}")

def replaceIMG(filename_to_replace,number):
    # initialize our app
    firebase_storage = pyrebase.initialize_app(config)
    # reference to our storage
    storage = firebase_storage.storage()
    PATH=r'C:\Users\User\Pictures\RandIMG'
    deleteIMG(filename_to_replace)
    new_name=Search_img.findFace(filename_to_replace.split(" face")[0],number,PATH)
    new_file_path=rf"C:\Users\User\Pictures\RandIMG\{new_name}"
    img = face_recognition.load_image_file(new_file_path)
    try:
        encode = face_recognition.face_encodings(img)[0]
    except:
        return -1
    storage.child(f"celebs/{new_name}").put(new_file_path)

    # iterate through all the files in the directory
    for filename in os.listdir(PATH):
        if filename.endswith('.jpg'):
            # construct the full path to the file
            file_path = os.path.join(PATH, filename)
            # delete the file
            os.remove(file_path)
    return 0

#Login function
def login(email, password):
    # Initialize Firebase App
    firebase = pyrebase.initialize_app(config)
    # Get Firebase Authentication instance
    auth = firebase.auth()
    # Print message for logging in
    print("Log in...")
    try:
        # Attempt to sign in with provided email and password
        login = auth.sign_in_with_email_and_password(email, password)
        # Return success message if signed in successfully
        return "Successfully logged in!"
    except:
        # Return error message if email or password is invalid
        return "Invalid email or password"


#Signup Function
def signup(email, password):
    # Initialize Firebase App
    firebase = pyrebase.initialize_app(config)
    # Get Firebase Authentication instance
    auth = firebase.auth()
    # Print message for signing up
    print("Sign up...")
    try:
        # Attempt to create user with provided email and password
        user = auth.create_user_with_email_and_password(email, password)
        # Return success message if user created successfully
        return "user Successfully created!"
    except:
        # Return error message if user already exists or password is weak
        return "user already exist or weak password"






if __name__ == "__main__":
    #DownloadImagesFromCelebs(encodeTest)
    # print(list_of_similar_images)
    #DownloadKnown()
    #replaceIMG("Adele face000002.jpg",1)
    print(signup("SAD@gamil.com",54645))



