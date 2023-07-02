import os
import shutil
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import Menu
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import ctypes


def set_wallpaper(file_path):
    wallpaper = bytes(file_path, 'utf-8')
    ctypes.windll.user32.SystemParametersInfoA(20, 0, wallpaper, 3)


def select_files():
    filetypes = (
        ('jpg files', '*.jpg'),
        ('png files', '*.png'),
    )

    filenames = fd.askopenfilenames(
        title='Open files',
        initialdir='/',
        filetypes=filetypes)

    # Папка назначения
    destination_folder = os.path.abspath("images")

    # Создать папку назначения, если она не существует
    os.makedirs(destination_folder, exist_ok=True)

    # Копировать выбранные файлы в папку назначения
    for filename in filenames:
        shutil.copy(filename, destination_folder)

    showinfo(
        title='File Copy',
        message='Selected files have been copied.'
    )

    # Update the file_names list
    update_file_names()

    # Display the copied images
    display_images()


def update_file_names():
    global file_names

    file_names = []
    folder = os.path.abspath("images")

    for file in os.listdir(folder):
        #file_path = os.path.join(folder, file)  # Полный путь к файлу
        #im = Image.open(file_path)
        file_names.append(file)

def resize_image(image, width, height):
    resized_image = image.resize((width, height))
    return resized_image


def display_images():
    row = 0
    col = 0

    for file in file_names:
        image_path = os.path.join(folder, file)
        image = Image.open(image_path)
        resized_image = resize_image(image, 160, 90)
        photo = ImageTk.PhotoImage(resized_image)
        label = tk.Label(root, image=photo)
        label.image = photo
        label.file_path = image_path  # Store the image path as a custom attribute
        label.grid(row=row, column=col, padx=5, pady=5, sticky='WE')
        # Bind the click event to the set_wallpaper function
        label.bind("<Button-1>", lambda event, file_path=image_path: set_wallpaper(file_path))
        label.bind("<Button-3>", lambda event, file_path=image_path: delete_image(file_path))
        col += 1
        if col == 4:
           col = 0
           row += 1


def delete_image(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # Remove the file from the disk
        os.remove(file_path)

        # Update the file_names list after deleting the image
        update_file_names()

        # Clear the current image display
        for label in root.grid_slaves():
            label.grid_forget()

        # Display the updated images
        display_images()

        showinfo(
            title='Image Deleted',
            message='The selected image has been deleted.'
        )
    else:
        showinfo(
            title='Image Not Found',
            message='The selected image does not exist.'
        )


# Create the Tkinter window
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
print(screensize)

root = tk.Tk()
root.title("qusonttarr")
root.iconbitmap(default="iconka.ico")
root.geometry("800x600")
root.attributes("-alpha", 0.99)
root.title("Простое меню")

menubar = Menu(root)
root.config(menu=menubar)

fileMenu = Menu(menubar)
fileMenu.add_command(label="Select files", command=select_files)
menubar.add_cascade(label="File", menu=fileMenu)


# Initialize file_names
file_names = []
folder = os.path.abspath("images")

# Update the file_names list
update_file_names()
display_images()

root.mainloop()