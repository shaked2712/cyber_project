import os
import socket
import logging
import tkinter
import customtkinter
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import random
import base64

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

class ClientGui(customtkinter.CTk):
    def __init__(self):
        super().__init__()  # Initialize the parent class
        customtkinter.set_appearance_mode("dark")  # Set the appearance mode of the GUI
        customtkinter.set_default_color_theme("blue")  # Set the default color theme
        self.geometry(f"{1100}x{580}")  # Set the size of the GUI window
        self.title("login page")  # Set the title of the GUI window
        self.IP = socket.gethostbyname(socket.gethostname())  # Get the IP address of the client
        self.PORT = 4546  # Set the port number to connect to
        self.Create_frame()  # Create a new frame
        self.color = "Dark"  # Set the default color of the GUI

    def start_client(self):
        # Create a new socket object
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to the server using the IP and port number
            self.client.connect((self.IP, self.PORT))
        except ConnectionRefusedError:
            # If the connection is refused, log an error and exit the program
            logging.error("Connection refused. The server may not be running.")
            exit()

    def Create_frame(self):
        # Create a new frame object
        self.frame = customtkinter.CTkFrame(master=self)
        # Pack the frame object onto the GUI window with some padding and expansion options
        self.frame.pack(pady=20, padx=30, fill="both", expand=True)

    def login(self):
        # Create a label object for the main title with custom font settings
        main_label = customtkinter.CTkLabel(master=self.frame, text="Login", font=("calibri", 50),
                                            justify=tkinter.LEFT)
        # Pack the main title onto the frame with some padding and alignment options
        main_label.pack(pady=10, padx=10)

        # Create a label object for the email field with custom font settings
        email_label = customtkinter.CTkLabel(master=self.frame, text="email", font=("calibri", 25, "normal"),
                                             justify=tkinter.LEFT)
        # Pack the email label onto the frame with some padding and alignment options
        email_label.pack(pady=0, padx=10)
        # Create a text entry object for the email field with custom font settings and a placeholder text
        self.email_entered = customtkinter.CTkEntry(master=self.frame, placeholder_text="email",
                                                    font=("calibri", 15, "normal"))
        # Pack the email entry onto the frame with some padding and alignment options
        self.email_entered.pack(pady=0, padx=10)

        # Create a label object for the password field with custom font settings
        pass_label = customtkinter.CTkLabel(master=self.frame, text="password", font=("calibri", 25, "normal"),
                                            justify=tkinter.LEFT)
        # Pack the password label onto the frame with some padding and alignment options
        pass_label.pack(pady=0, padx=10)
        # Create a text entry object for the password field with custom font settings and a placeholder text
        self.pass_entered = customtkinter.CTkEntry(master=self.frame, placeholder_text="password",
                                                   font=("calibri", 15, "normal"))
        self.pass_entered.pack(pady=0, padx=10)

        button_log = customtkinter.CTkButton(master=self.frame, text="Login", command=self.check_login,
                                              font=("calibri", 20, "normal"))
        button_log.pack(pady=20, padx=10)
        button_signup = customtkinter.CTkButton(master=self.frame, text="sign up", command=self.check_code,
                                              font=("calibri", 20, "normal"))
        button_signup.pack(pady=120, padx=10)

    # Define a method to check login credentials
    def check_login(self):
        # Send a login request to the server using Base64 encoding
        self.client.send(Base64_encode("login"))

        # Get the email entered by the user in the email entry box
        user_email = self.email_entered.get()

        # Send the email to the server using Base64 encoding
        self.client.send(Base64_encode(user_email))

        # Receive a response from the server and decode it
        self.client.recv(1024).decode()

        # Get the password entered by the user in the password entry box
        user_password = self.pass_entered.get()

        # Send the password to the server using Base64 encoding
        self.client.send(Base64_encode(user_password))

        # Receive a response from the server and decode it
        self.client.recv(1024).decode()

        # Receive a response from the server and decode it
        login_label_text = self.client.recv(1024)
        login_label_text = Base64_decode(login_label_text)

        # Create a label to display the login result and place it on the frame
        login_label = customtkinter.CTkLabel(master=self.frame, text="20", font=("calibri", 30), justify=tkinter.LEFT)
        login_label.place(y=260, x=370)

        # Update the text of the label to display the login result
        login_label.configure(text=login_label_text)

        # If login is successful, call the AI_Page method
        if login_label_text == "Successfully logged in!":
            self.AI_Page()

        # If login is unsuccessful, clear the email and password entry boxes
        else:
            self.email_entered.delete(0, END)
            self.pass_entered.delete(0, END)

    def check_code(self):
        # destroy previous frame and create a new one
        self.frame.destroy()
        self.title("code_page")
        self.Create_frame()

        # send a message to the server indicating that the client wants to sign up
        self.client.send(Base64_encode("sign up"))

        # create a label and entry field for the user to enter their code
        label1 = customtkinter.CTkLabel(master=self.frame, text="enter code", font=("calibri", 30),
                                        justify=tkinter.LEFT)
        label1.pack(pady=10, padx=10)
        self.code_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="code", font=("calibri", 15))
        self.code_entry.pack(pady=10, padx=10)

        # create a button that, when clicked, sends the code to the server for verification
        code_button = customtkinter.CTkButton(master=self.frame, text="send code", command=self.send_code,
                                              font=("calibri", 20))
        code_button.pack(pady=10, padx=10)

    def send_code(self):
        # get the code entered by the user
        code = self.code_entry.get()

        # send the code to the server for verification
        self.client.send(Base64_encode(code))

        # receive a response from the server
        response = self.client.recv(1024)
        response = Base64_decode(response)

        # create a label to display the server's response
        answer_label = customtkinter.CTkLabel(master=self.frame, text="", font=("calibri", 30), justify=tkinter.LEFT)
        answer_label.place(y=215, x=450)

        # if the server approves the code, display a message and go to the sign up page
        if response == "approved code":
            answer_label.configure(text=response)
            self.sign_up()
        # otherwise, display the server's response
        else:
            answer_label.configure(text=response)

    def sign_up(self):
        # Destroy the current frame
        self.frame.destroy()
        # Set the window title to "sign up"
        self.title("sign up")
        # Create a new frame
        self.Create_frame()

        # Create a label for the main title
        main_label = customtkinter.CTkLabel(master=self.frame, text="sign up", font=("calibri", 50),
                                            justify=tkinter.LEFT)
        # Pack the main label
        main_label.pack(pady=10, padx=10)

        # Create a label for the email input field
        email_label = customtkinter.CTkLabel(master=self.frame, text="email", font=("calibri", 25, "normal"),
                                             justify=tkinter.LEFT)
        # Pack the email label
        email_label.pack(pady=0, padx=10)
        # Create an input field for the email
        self.email_entered = customtkinter.CTkEntry(master=self.frame, placeholder_text="email",
                                                    font=("calibri", 15, "normal"))
        # Pack the email input field
        self.email_entered.pack(pady=0, padx=10)

        # Create a label for the password input field
        pass_label = customtkinter.CTkLabel(master=self.frame, text="password", font=("calibri", 25, "normal"),
                                            justify=tkinter.LEFT)
        # Pack the password label
        pass_label.pack(pady=0, padx=10)
        # Create an input field for the password
        self.pass_entered = customtkinter.CTkEntry(master=self.frame, placeholder_text="password",
                                                   font=("calibri", 15, "normal"))
        # Pack the password input field
        self.pass_entered.pack(pady=0, padx=10)

        # Create a button to sign up
        button_log = customtkinter.CTkButton(master=self.frame, text="sign up", command=self.save_data,
                                             font=("calibri", 20, "normal"))
        # Pack the button
        button_log.pack(pady=20, padx=10)

    def save_data(self):
        # Get user email and send it to the server
        user_email = self.email_entered.get()
        self.client.send(Base64_encode(user_email))
        self.client.recv(1024).decode()

        # Get user password and send it to the server
        user_password = self.pass_entered.get()
        self.client.send(Base64_encode(user_password))
        self.client.recv(1024).decode()

        # Receive signup confirmation from server and display it in a label
        signup_label_text = self.client.recv(1024)
        signup_label_text = Base64_decode(signup_label_text)
        signup_label = customtkinter.CTkLabel(master=self.frame, text="", font=("calibri", 30), justify=tkinter.LEFT)
        signup_label.place(y=260, x=370)
        print(signup_label_text)
        if signup_label_text == "user Successfully created!":
            # If user was successfully created, display a congratulatory message and move on to the next step
            signup_label.configure(text="congratulation " + signup_label_text)
            self.frame.destroy()
            self.Create_frame()
            self.learning_user()
        else:
            # If there was an error with creating the user, display the error message and clear the email and password fields
            signup_label.configure(text=signup_label_text)
            self.email_entered.delete(0, END)
            self.pass_entered.delete(0, END)

    def learning_user(self):
        # Display welcome message and instructions for the user
        main_label = customtkinter.CTkLabel(master=self.frame, text="welcome to the AI learning stage",
                                            font=("calibri", 40), justify=tkinter.LEFT)
        main_label.pack()
        header1_label = customtkinter.CTkLabel(master=self.frame,
                                               text="Once you press the upload button, it will open a folder where you may save the images.",
                                               font=("calibri", 20), justify=tkinter.LEFT)
        header1_label.pack()
        header2_label = customtkinter.CTkLabel(master=self.frame,
                                               text="after that please close the folder and press the finish button",
                                               font=("calibri", 20), justify=tkinter.LEFT)
        header2_label.pack()

        # Create "Upload" and "Finish" buttons for the user to click
        upload_button = customtkinter.CTkButton(master=self.frame, text="upload", command=self.open_dir,
                                                font=("calibri", 20, "normal"))
        upload_button.pack()
        finish_button = customtkinter.CTkButton(master=self.frame, text="finish", command=self.upload_to_data,
                                                font=("calibri", 20, "normal"))
        finish_button.pack(pady=5)

    def open_dir(self):
        # This function opens a file dialog to allow the user to select multiple image files to upload
        dir_path = r"C:/Users/User/Pictures/cyber"  # The directory path where the images are located
        filedialog.askopenfilenames(initialdir=dir_path, filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

    def upload_to_data(self):
        # This function uploads the selected images to the server
        dir_path = r"C:/Users/User/Pictures/cyber"  # The directory path where the images are located
        images_list = os.listdir(dir_path)  # Get a list of all image files in the directory
        warning_label = customtkinter.CTkLabel(master=self.frame, text="", font=("calibri", 30), justify=tkinter.LEFT)
        warning_label.pack(pady=10)
        if len(images_list) < 4:
            warning_label.configure(
                text="you need at least 4 images")  # Show a warning message if less than 4 images are selected
        elif len(images_list) > 4:
            warning_label.configure(
                text="you have more than 4 images. please delete some")  # Show a warning message if more than 4 images are selected
        else:
            self.client.send(Base64_encode(dir_path))  # Send the directory path to the server
            self.client.recv(1024).decode()
            self.frame.destroy()
            self.Create_frame()
            self.login()

    def AI_Page(self):
        # Destroy the previous frame and create a new frame for AI page
        self.frame.destroy()
        self.title("AI page")
        self.geometry(f"{1200}x{1000}")
        self.Create_frame()

        # Receive the user's name from the server and display it on the screen
        name = self.client.recv(1024)
        name = Base64_decode(name)
        main_label = customtkinter.CTkLabel(master=self.frame, text=f"please press the image where {name} is on",
                                            font=("calibri", 30), justify=tkinter.LEFT)
        main_label.pack()

        # Receive 4 celebrity images from the server and create buttons with random images
        celebs_names = []
        celeb_images = []
        for i in range(4):
            # Receive the filename of the image from the server
            filename = self.client.recv(1024)
            filename = Base64_decode(filename)
            celebs_names.append(filename)

            # Receive the image data from the server and save it to a file
            with open(filename + 'copy.jpg', 'wb') as f:
                while True:
                    data = self.client.recv(1024)
                    if not data or data == b'stop':
                        break
                    if b"stop" in data:
                        data = data[:-4]
                        f.write(data)
                        break
                    f.write(data)

            # Load the image from the file, create a PhotoImage object, and append it to celeb_images list
            image = Image.open(filename + 'copy.jpg')
            image = image.resize((200, 200))  # adjust the size of the image as needed
            photo = ImageTk.PhotoImage(image)
            celeb_images.append(photo)

            # Remove the file after loading the image
            os.remove(filename + 'copy.jpg')

            # Send an "ok" signal to the server to indicate that the image has been received successfully
            self.client.send("ok".encode())

        # Randomly select 4 unique images and create buttons with them
        unique_images = random.sample(celeb_images, 4)
        for i in range(4):
            # Get the corresponding celebrity name for the image
            name = celebs_names[celeb_images.index(unique_images[i])]
            # Create a button with the unique image and bind it to the send_name method with the corresponding name as parameter
            button = customtkinter.CTkButton(self.frame, text=f"image {i}", image=unique_images[i],
                                             command=lambda name=name: self.send_name(name))
            button.pack()

    def send_name(self, name):
        # Encode the name using Base64 and send it to the server
        self.client.send(Base64_encode(name))
        # Receive the response from the server and decode it using Base64
        answer = self.client.recv(1024)
        answer = Base64_decode(answer)
        # If the response is "ok", go to the main website, otherwise show a warning label
        if answer == "ok":
            self.main_website()
        else:
            warning_label = customtkinter.CTkLabel(master=self.frame, text="wrong picture", font=("calibri", 30),
                                                   justify=tkinter.LEFT)
            warning_label.place(x=500, y=900)

    def main_website(self):
        # Destroy the current frame and create a new one for the main website
        self.frame.destroy()
        self.title("main website")
        self.Create_frame()
        # Add a label to the main website frame
        main_label = customtkinter.CTkLabel(master=self.frame, text=f"welcome to Shaked's website",
                                            font=("calibri", 40), justify=tkinter.LEFT)
        main_label.pack()


app = ClientGui()
app.start_client()
app.login()
app.mainloop()
