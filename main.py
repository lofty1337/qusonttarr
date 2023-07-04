import os
import shutil
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter import  Menu, Toplevel, Label, Entry, Button
from PIL import Image, ImageTk
import ctypes


class WallpaperChanger:
    def __init__(self):
        self.mode = 0  # 0: Manually, 1: Timer
        self.interval = 10  # Interval in seconds for wallpaper change
        self.timer = 0
        self.current_wallpaper_index = 0
        self.file_names = []
        self.folder = os.path.abspath("images")

        self.root = tk.Tk()
        self.root.title("qusonttarr")
        self.root.iconbitmap(default="iconka.ico")
        self.root.geometry("800x600")
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        self.create_file_menu()
        self.create_mode_menu()

        # Start the timer
        self.update_timer()

        # Update the file_names list
        self.update_file_names()
        self.display_images()

        # Call the function to start changing wallpapers periodically
        self.change_wallpaper_periodically()

        self.root.mainloop()

    def create_file_menu(self):
        file_menu = Menu(self.menubar)
        file_menu.add_command(label="Select files", command=self.select_files)
        file_menu.add_command(label="Delete all files", command=self.delete_all_images)
        self.menubar.add_cascade(label="File", menu=file_menu)

    def create_mode_menu(self):
        mode_menu = Menu(self.menubar)
        mode_menu.add_command(label="Manually", command=self.set_mode_manually)
        mode_menu.add_command(label="Timer", command=self.set_mode_timer)
        self.menubar.add_cascade(label="Mode", menu=mode_menu)

    def set_mode_manually(self):
        self.mode = 0

    def set_mode_timer(self):
        self.mode = 1
        self.update_file_names()
        self.open_interval_window()

    def update_file_names(self, folder=None):
        self.file_names = []
        folder = folder or self.folder

        for root, dirs, files in os.walk(folder):
            for file in files:
                self.file_names.append(os.path.join(root, file))
    def open_interval_window(self):
        interval_window = Toplevel(self.root)
        interval_window.title("Change Interval")

        # Label and entry for interval
        interval_label = Label(interval_window, text="Interval (seconds):")
        interval_label.pack()
        interval_entry = Entry(interval_window)
        interval_entry.insert(tk.END, str(self.interval))
        interval_entry.pack()

        # Button to save interval
        save_button = Button(interval_window, text="Save",
                             command=lambda: self.save_interval(interval_entry.get(), interval_window))
        save_button.pack()

    def save_interval(self, new_interval, window):
        try:
            self.interval = int(new_interval)
            window.destroy()
        except ValueError:
            showerror("Invalid Interval", "Interval must be an integer value.")

    def select_files(self):
        filetypes = (('jpg files', '*.jpg'), ('png files', '*.png'))
        filenames = fd.askopenfilenames(title='Open files', initialdir='/', filetypes=filetypes)
        destination_folder = os.path.abspath("images")

        # Create the destination folder if it does not exist
        os.makedirs(destination_folder, exist_ok=True)

        # Copy selected files to the destination folder
        for filename in filenames:
            shutil.copy(filename, destination_folder)

        showinfo(title='File Copy', message='Selected files have been copied.')

        # Update the file_names list
        self.update_file_names()

        # Display the copied images
        self.display_images()


    def resize_image(self, image, width, height):
        resized_image = image.resize((width, height))
        return resized_image

    def display_images(self):
        for label in self.root.grid_slaves():
            label.grid_forget()

        row = 0
        col = 0

        for file in self.file_names:
            image_path = os.path.join(self.folder, file)
            image = Image.open(image_path)
            resized_image = self.resize_image(image, 160, 90)
            photo = ImageTk.PhotoImage(resized_image)
            label = tk.Label(self.root, image=photo)
            label.image = photo
            label.file_path = image_path  # Store the image path as a custom attribute
            label.grid(row=row, column=col, padx=5, pady=5, sticky='WE')
            # Bind the click event to the set_wallpaper function
            label.bind("<Button-1>", lambda event, file_path=image_path: self.set_wallpaper(file_path))
            label.bind("<Button-3>", lambda event, file_path=image_path: self.delete_image(file_path))
            col += 1
            if col == 4:
                col = 0
                row += 1

    def delete_image(self, file_path):
        # Check if the file exists
        if os.path.exists(file_path):
            # Remove the file from the disk
            os.remove(file_path)

            # Update the file_names list after deleting the image
            self.update_file_names()

            # Clear the current image display
            self.display_images()

            showinfo(title='Image Deleted', message='The selected image has been deleted.')
        else:
            showinfo(title='Image Not Found', message='The selected image does not exist.')

    def delete_all_images(self):
        folder_path = os.path.abspath("images")

        if os.path.exists(folder_path):
            response = askyesno("Delete All Images", "Are you sure you want to delete all images?")
            if response:
                file_names = os.listdir(folder_path)
                for file_name in file_names:
                    file_path = os.path.join(folder_path, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

                self.update_file_names()

                # Clear the current image display
                self.display_images()

                showinfo(title='Deleted', message='All images have been deleted.')
        else:
            showinfo(title='Folder Not Found', message='"images" does not exist.')

    def set_wallpaper(self, file_path):
        wallpaper = bytes(file_path, 'utf-8')
        ctypes.windll.user32.SystemParametersInfoA(20, 0, wallpaper, 3)

    def update_timer(self):
        if self.mode == 1:  # Only update the timer if mode is set to 1 (timer)
            self.timer = (self.timer + 1) % 11
        self.root.after(1000, self.update_timer)

    def change_wallpaper_periodically(self):
        if self.mode == 1:  # Only change wallpaper if mode is set to 1 (timer)
            if self.current_wallpaper_index >= len(self.file_names):
                self.current_wallpaper_index = 0

            selected_image = self.file_names[self.current_wallpaper_index]
            image_path = os.path.join(self.folder, selected_image)
            self.set_wallpaper(image_path)
            self.current_wallpaper_index += 1

        # Call change_wallpaper_periodically() again after the specified interval (in seconds)
        self.root.after(self.interval * 1000, self.change_wallpaper_periodically)


if __name__ == "__main__":
    WallpaperChanger()
