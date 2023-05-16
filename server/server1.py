import socket
import FireBaseEx
import os
import BasicAiManagement
import base64
import random

# Set the server's port number
PORT=4546
# Get the IP address of the server
IP=socket.gethostbyname(socket.gethostname())

# Create a new socket object
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((IP,PORT))
server.listen()
print("waiting for clients")
conn,addr =server.accept()
print(addr)

# encode the data
def Base64_encode(data):
    data = data.encode("ascii")
    data = base64.b64encode(data)
    return data

# decode the data
def Base64_decode(data):
    data=base64.b64decode(data)
    data=data.decode('ascii')
    return data

# get the type - login or sign up
type_of_entry=conn.recv(1024)
type_of_entry=Base64_decode(type_of_entry)
if type_of_entry =="login":
    while True:
        # get the email and password
        email = conn.recv(1024)
        email=Base64_decode(email)
        conn.send("ok".encode())
        password = conn.recv(1024)
        password=Base64_decode(password)
        conn.send("ok".encode())
        # check if the data is correct
        login=FireBaseEx.login(email,password)
        print(login)
        if login=="Successfully logged in!":
            login=Base64_encode(login)
            conn.send(login)
            break
        else:
            print(login)
            login = Base64_encode(login)
            conn.send(login)
            type_of_entry = conn.recv(1024)
            type_of_entry = Base64_decode(type_of_entry)
else:
    while True:
        # get the code from the client
        code=conn.recv(1024)
        code=Base64_decode(code)
        print(code)
        if code=="1904":
            conn.send(Base64_encode("approved code"))
            break
        else:
            conn.send(Base64_encode("wrong code"))
    while True:
        # get the email and password
        email = conn.recv(1024)
        email = Base64_decode(email)
        conn.send("ok".encode())
        password = conn.recv(1024)
        password = Base64_decode(password)
        conn.send("ok".encode())
        # create a new user
        signup=FireBaseEx.signup(email,password)
        if signup == "user Successfully created!":
            conn.send(Base64_encode(signup))
            break
        else:
            conn.send(Base64_encode(signup))
    # get the path where the images are
    path=conn.recv(1024)
    path=Base64_decode(path)
    list_of_known_images=os.listdir(path)
    for img in list_of_known_images:
        # upload images to database
        FireBaseEx.uploadImage(email,img,path+f"/{img}")

    conn.send(Base64_encode("uploaded"))
    # delete all the images that were in the directory
    for filename in list_of_known_images:
        if filename.endswith('.jpg'):
            # construct the full path to the file
            file_path = os.path.join(path, filename)
            # delete the file
            os.remove(file_path)

    while True:
        # do the login process again
        login_note=conn.recv(1024)
        login_note=Base64_decode(login_note)
        email = conn.recv(1024)
        email = Base64_decode(email)
        conn.send("ok".encode())
        password = conn.recv(1024)
        password = Base64_decode(password)
        conn.send("ok".encode())
        login=FireBaseEx.login(email,password)
        print(login)
        if login == "Successfully logged in!":
            login = Base64_encode(login)
            conn.send(login)
            break
        else:
            print(login)
            login = Base64_encode(login)
            conn.send(login)


# Download known images from Firebase
FireBaseEx.DownloadKnown(email)
path = "images/"
listKnown = os.listdir(path)
# Get the names and preprocessed images of known people
namesKnown,images_list = BasicAiManagement.getNamesandPrep(listKnown,path)
# Encode the known images
encodeListKnown=BasicAiManagement.findEncoding(images_list)
# Choose a random name and send it to the client
name=random.choice(namesKnown)
conn.send(Base64_encode(name))
# Get the index of the name in the list of known names
indexOfName=namesKnown.index(name)
# Get the image of the person with the given name
imageOfName=images_list[indexOfName]

# Download similar and different images from Firebase to their specified directories
FireBaseEx.DownloadImagesFromCelebs(encodeListKnown[indexOfName])

# get the image in the similar directory
PATH_TO_SIMILAR="similar/"
similar=os.listdir(PATH_TO_SIMILAR)
filename = similar[0]

# in order to replace an image in the database i need it's number in order to get the next one
number_for_replacement=filename.split("0")[-1]
print(number_for_replacement)
if number_for_replacement==".jpg":
    number_for_replacement = filename.split("0")[-2]
else:
    number_for_replacement = number_for_replacement.split(".")[0]
print(number_for_replacement)
number_for_replacement=int(number_for_replacement)+1
# replace the image
flag =FireBaseEx.replaceIMG(filename.replace("_"," "),number_for_replacement)

# checks if the AI can use the image
print(flag)
while flag==-1:
    number_for_replacement = number_for_replacement + 1
    flag = FireBaseEx.replaceIMG(filename.replace("_", " "), number_for_replacement)
    print(flag)
celebs_name=filename.split(".")[0]
conn.send(Base64_encode(celebs_name))

with open(f"{PATH_TO_SIMILAR}{filename}", "rb") as f:
    # Read the image data
    image_data = f.read()

    # Send the image data to the client
    conn.send(image_data)
    conn.send("stop".encode())
    print(f"Sent {filename} ")
# Wait for the client to confirm receipt of the image data
    client_confirmation = conn.recv(1024).decode()
    print(client_confirmation)

# get the images in the differentFace directory
PATH_TO_DIFFERENT="differentFace/"
diff=os.listdir(PATH_TO_DIFFERENT)
for i in range(3):
    filename=diff[i]
    # Same process of getting the next number and replacing each image I use
    number_for_replacement = filename.split("0")[-1]
    print(number_for_replacement)
    if number_for_replacement == ".jpg" or number_for_replacement==".png":
        number_for_replacement = filename.split("0")[-2]
    else:
        number_for_replacement = number_for_replacement.split(".")[0]
    print(number_for_replacement)
    number_for_replacement = int(number_for_replacement) + 1
    flag = FireBaseEx.replaceIMG(filename.replace("_", " "), number_for_replacement)
    while flag == -1:
        number_for_replacement = number_for_replacement + 1
        flag = FireBaseEx.replaceIMG(filename.replace("_", " "), number_for_replacement)

    conn.send(Base64_encode(filename.split(".")[0]))
    with open(f"{PATH_TO_DIFFERENT}{filename}", "rb") as f:
        # Read the image data
        image_data = f.read()

        # Send the image data to the client
        conn.send(image_data)
        conn.send("stop".encode())
        print(f"Sent {filename} ")
        # Wait for the client to confirm receipt of the image data
        client_confirmation = conn.recv(1024).decode()
        print(client_confirmation)


print("sent all")
# delete all the images in differentFace directory
for filename in os.listdir(PATH_TO_DIFFERENT):
    if filename.endswith('.jpg') or filename.endswith(".png"):
        # construct the full path to the file
        file_path = os.path.join(PATH_TO_DIFFERENT, filename)
        # delete the file
        os.remove(file_path)

# delete the image in similar directory
file_path = os.path.join(PATH_TO_SIMILAR, os.listdir(PATH_TO_SIMILAR)[0])
os.remove(file_path)

# delete all the images in images directory
for filename in os.listdir("images/"):
    if filename.endswith('.jpg') or filename.endswith(".png"):
        # construct the full path to the file
        file_path = os.path.join("images/", filename)
        # delete the file
        os.remove(file_path)

while True:
    # checks if the client pressed the correct image
    name_of_celeb=conn.recv(1024)
    name_of_celeb=Base64_decode(name_of_celeb)
    if name_of_celeb==celebs_name:
        conn.send(Base64_encode("ok"))
        break
    else:
        conn.send(Base64_encode("not correct"))


