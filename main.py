import os
import shutil
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import messagebox, Menu, Toplevel, Label, Entry, Button#, ttk
from PIL import Image, ImageTk
import ctypes


mode = 0  # 0: Manually, 1: Timer, 2: Day and Night
interval = 10  # Interval in seconds for wallpaper change
timer=0


def set_mode_manually():
    global mode
    mode = 0
    print(f"{mode}mode")

def set_mode_timer():
    global mode
    mode = 1
    open_interval_window()
    print(f"{mode}mode")


# Function to open window for changing interval
def open_interval_window():
    interval_window = Toplevel(root)
    interval_window.title("Change Interval")

    # Label and entry for interval
    interval_label = Label(interval_window, text="Interval (seconds):")
    interval_label.pack()
    interval_entry = Entry(interval_window)
    interval_entry.insert(tk.END, str(interval))
    interval_entry.pack()

    # Button to save interval
    save_button = Button(interval_window, text="Save",
                         command=lambda: save_interval(interval_entry.get(), interval_window))
    save_button.pack()


def set_wallpaper(file_path):
    wallpaper = bytes(file_path, 'utf-8')
    ctypes.windll.user32.SystemParametersInfoA(20, 0, wallpaper, 3)


def update_timer(root, counter=0):
    global timer
    if mode == 1:  # Only update the timer if mode is set to 1 (timer)
        timer = counter
    root.after(1000, update_timer, root, (counter + 1) % 11)  # Call update_timer() again after 1000 milliseconds (1 second)
    print(timer)


def change_wallpaper_periodically():
    global mode, current_wallpaper_index, interval

    if mode == 1:  # Only change wallpaper if mode is set to 1 (timer)
        if current_wallpaper_index >= len(file_names):
            current_wallpaper_index = 0

        selected_image = file_names[current_wallpaper_index]
        image_path = os.path.join(folder, selected_image)
        set_wallpaper(image_path)
        current_wallpaper_index += 1
    # Call change_wallpaper_periodically() again after the specified interval (in seconds)
    root.after(interval * 1000, change_wallpaper_periodically)



# Function to save the interval and close the interval window
def save_interval(new_interval, window):
    global interval
    try:
        interval = int(new_interval)
        window.destroy()
    except ValueError:
        messagebox.showerror("Invalid Interval", "Interval must be an integer value.")


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

root = tk.Tk()
root.title("qusonttarr")
root.iconbitmap(default="iconka.ico")
root.geometry("800x600")
root.attributes("-alpha", 0.99)
root.title("Простое меню")

# Start the timer
update_timer(root)

menubar = Menu(root)
root.config(menu=menubar)

fileMenu = Menu(menubar)
fileMenu.add_command(label="Select files", command=select_files)
menubar.add_cascade(label="File", menu=fileMenu)

modeMenu = Menu(menubar)
modeMenu.add_command(label="Manually", command=set_mode_manually)
modeMenu.add_command(label="Timer", command=set_mode_timer)
menubar.add_cascade(label="Mode", menu=modeMenu)

# Initialize file_names
file_names = []
folder = os.path.abspath("images")

# Update the file_names list
update_file_names()
display_images()
current_wallpaper_index = 0

# Call the function to start changing wallpapers periodically
change_wallpaper_periodically()

root.mainloop()