import tkinter as tk # import tkinter library for GUI
import csv # import csv library for reading and writing csv files
import cv2 # import cv2 library for computer vision
import os # import os library for file and directory operations
import numpy as np # import numpy library for numerical operations
from PIL import Image # import Image library for image processing
import pandas as pd # import pandas library for data analysis
import datetime # import datetime library for date and time operations
import time # import time library for time operations

window = tk.Tk() # create a window object
window.title("STUDENT ATTENDANCE USING FACE RECOGNITION SYSTEM") # set the title of the window
window.geometry('800x500') # set the size of the window

dialog_title = 'QUIT' # set the title of the quit dialog
dialog_text = "are you sure?" # set the text of the quit dialog
window.configure(background='green') # set the background color of the window
window.grid_rowconfigure(0, weight=1) # configure the grid layout of the window
window.grid_columnconfigure(0, weight=1) # configure the grid layout of the window


def clear(): # define a function to clear the name entry
    std_name.delete(0, 'end') # delete the text in the name entry
    res = "" # set an empty string as the result
    label4.configure(text=res) # update the label with the result


def clear2(): # define a function to clear the matric number entry
    std_number.delete(0, 'end') # delete the text in the matric number entry
    res = "" # set an empty string as the result
    label4.configure(text=res) # update the label with the result


def takeImage(): # define a function to take image of a student
    name = (std_name.get()) # get the name from the name entry
    Id = (std_number.get()) # get the matric number from the matric number entry
    if name.isalpha(): # check if the name is valid (only alphabets)
        cam = cv2.VideoCapture(0) # create a camera object to capture video from webcam
        harcascadePath = "haarcascade_frontalface_default.xml" # set the path of the face detector file
        detector = cv2.CascadeClassifier(harcascadePath) # create a face detector object using the file
        sampleNum = 0 # initialize a variable to count the number of samples

        while True: # loop until break condition is met
            ret, img = cam.read() # read a frame from the camera object
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert the frame to grayscale
            faces = detector.detectMultiScale(gray, 1.1, 3) # detect faces in the frame using the face detector object
            for (x, y, w, h) in faces: # loop over each detected face
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) # draw a rectangle around the face on the frame
                sampleNum = sampleNum + 1 # increment the sample number by one
                # store each student picture with its name and id in a folder named TrainingImages
                cv2.imwrite("TrainingImages\ " + name + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + h])
                cv2.imshow('FACE RECOGNIZER', img) # show the frame on a window named FACE RECOGNIZER
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # stop the camera when the number of picture exceed 50 pictures for each student
            if sampleNum > 50:
                break

        cam.release()
        cv2.destroyAllWindows()
        # print the student name and id after a successful face capturing
        res = 'Student details saved with: \n Matric number : ' + Id + ' and  Full Name: ' + name

        row = [Id, name]

        with open('studentDetailss.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        label4.configure(text=res)
    else:

        if name.isalpha():
            res = "Enter correct Matric Number"
            label4.configure(text=res)


def getImagesAndLabels(path): # define a function to get images and labels from a given path
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)] # get the list of image paths in the given path
    faces = [] # initialize an empty list to store faces
    Ids = [] # initialize an empty list to store ids
    for imagePath in imagePaths: # loop over each image path
        pilImage = Image.open(imagePath).convert('L') # open the image and convert it to grayscale
        imageNp = np.array(pilImage, 'uint8') # convert the image to a numpy array
        Id = int(os.path.split(imagePath)[-1].split(".")[1]) # get the id from the image name
        faces.append(imageNp) # append the face to the faces list
        Ids.append(Id) # append the id to the ids list
    return faces, Ids # return the faces and ids lists


def trackImage(): # define a function to track the image and mark attendance
    recognizer = cv2.face.LBPHFaceRecognizer_create() # create a face recognizer object using LBPH algorithm
    recognizer.read("Trainner.yml") # read the trained model from Trainner.yml file
    harcascadePath = "haarcascade_frontalface_default.xml" # set the path of the face detector file
    faceCascade = cv2.CascadeClassifier(harcascadePath) # create a face detector object using the file
    df = pd.read_csv("studentDetailss.csv") # read the student details from studentDetailss.csv file
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL # set a font for text on frame
    cam = cv2.VideoCapture(0) # create a camera object to capture video from webcam
    # create a dataframe to hold the student id,name,date and time
    col_names = {'Id', 'Name', 'Date', 'Time'}
    attendance = pd.DataFrame(columns=col_names)
    while True: # loop until break condition is met
        ret, img = cam.read() # read a frame from the camera object
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert the frame to grayscale
        faces = faceCascade.detectMultiScale(gray, 1.1, 3) # detect faces in the frame using the face detector object
        for (x, y, w, h) in faces: # loop over each detected face
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) # draw a rectangle around the face on the frame
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w]) # predict the id and confidence of the face using the face recognizer object
            #  a confidence less than 50 indicates a good face recognition
            if conf < 60:
                ts = time.time()

                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
                aa = df.loc[df['ID'] == Id]['NAME'].values
                tt = str(Id) + "-" + aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                row2 = [Id, aa, date, timeStamp]
                #   open the attendance file for update
                with open('AttendanceFile.csv', 'a+') as csvFile2:
                    writer2 = csv.writer(csvFile2)
                    writer2.writerow(row2)
                csvFile2.close()
                # print attendance updated on the notification board of the GUI
                res = 'ATTENDANCE UPDATED WITH DETAILS'

                label4.configure(text=res) # update the label with the result

            else: # if the confidence is not less than 50
                Id = 'Unknown' # set the id as Unknown
                tt = str(Id) # set the text as Unknown
                #  store the unknown images in the images unknown folder
                if conf > 65: # if the confidence is greater than 65
                    noOfFile = len(os.listdir("ImagesUnknown")) + 1 # get the number of files in the ImagesUnknown folder and add one
                    cv2.imwrite("ImagesUnknown\Image" + str(noOfFile) + ".jpg", img[y:y + h, x:x + w]) # save the unknown image in the ImagesUnknown folder
                    res = 'ID UNKNOWN, ATTENDANCE NOT UPDATED' # set a string as the result
                    label4.configure(text=res) # update the label with the result
            # To avoid duplication in the attendance file.
            attendance = attendance.drop_duplicates(subset=['Id'], keep='first') # drop any duplicate rows in the attendance dataframe based on id column and keep the first one
            # show the student id and name
            cv2.putText(img, str(tt), (x, y + h - 10), font, 0.8, (255, 255, 255), 1) # put the text on the frame near the face
            cv2.imshow('FACE RECOGNIZER', img) # show the frame on a window named FACE RECOGNIZER
        if cv2.waitKey(1000) == ord('q'): # if q key is pressed within 1000 milliseconds
            break # break the loop

        cam.release() # release the camera object
        cv2.destroyAllWindows() # destroy all windows


label1 = tk.Label(window, background="green", fg="black", text="Name :", width=10, height=1,
                  font=('Helvetica', 16)) # create a label for name
label1.place(x=83, y=40) # place the label on the window
std_name = tk.Entry(window, background="yellow", fg="black", width=25, font=('Helvetica', 14)) # create an entry for name
std_name.place(x=280, y=41) # place the entry on the window
label2 = tk.Label(window, background="green", fg="black", text="Matric Number :", width=14, height=1,
                  font=('Helvetica', 16)) # create a label for matric number
label2.place(x=100, y=90) # place the label on the window
std_number = tk.Entry(window, background="yellow", fg="black", width=25, font=('Helvetica', 14)) # create an entry for matric number
std_number.place(x=280, y=91) # place the entry on the window

clearBtn1 = tk.Button(window, background="red", command=clear, fg="white", text="CLEAR", width=8, height=1,
                      activebackground="red", font=('Helvetica', 10)) # create a button to clear name entry
clearBtn1.place(x=580, y=42) # place the button on the window
clearBtn2 = tk.Button(window, background="red", command=clear2, fg="white", text="CLEAR", width=8,
                      activebackground="red", height=1, font=('Helvetica', 10)) # create a button to clear matric number entry
clearBtn2.place(x=580, y=92) # place the button on the window

label3 = tk.Label(window, background="green", fg="red", text="Notification", width=10, height=1,
                  font=('Helvetica', 20, 'underline')) # create a label for notification
label3.place(x=320, y=155) # place the label on the window
label4 = tk.Label(window, background="yellow", fg="black", width=55, height=4, font=('Helvetica', 14, 'italic')) # create a label to show notification messages
label4.place(x=95, y=205) # place the label on the window

takeImageBtn = tk.Button(window, command=takeImage, background="yellow", fg="black", text="CAPTURE IMAGE",
                         activebackground="red",
                         width=15, height=3, font=('Helvetica', 12)) # create a button to capture image of a student
takeImageBtn.place(x=350, y=360) # place the button on the window

window.mainloop() # start the main loop of the window
