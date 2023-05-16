import cv2
import face_recognition
import os
import FireBaseEx


# get the names of the images without jpg and read the images for encoding and printing later
def getNamesandPrep(mylist,path):
    image_list = []
    names = []
    for cl in mylist:
        curImg=cv2.imread(f"{path}/{cl}")
        image_list.append(curImg)
        names.append(os.path.splitext(cl)[0])
    return names, image_list



#get the encodings of the images
def findEncoding(images):
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    print("encoding complete")
    return encodeList


if __name__=="__main__":
    # get images from database
    FireBaseEx.DownloadKnown()
    # get the images as a list
    path = "images/"
    listKnown = os.listdir(path)
    namesKnown,images_list = getNamesandPrep(listKnown,path)
    encodeListKnown=findEncoding(images_list)
    # get a name of a specific person and its index
    # make sure the user chooses a name thatis in the list
    while True:
        name = input(f"choose a name from the following list: {namesKnown}")
        if name in namesKnown:
            print("good Choice")
            break
        else:
            print("we do not have that person in the list")

    # get the image ready for show
    indexOfName=namesKnown.index(name)
    imageOfName=images_list[indexOfName]

    # Prepare a lists of similar and different faces
    FireBaseEx.DownloadImagesFromCelebs(encodeListKnown[indexOfName])

