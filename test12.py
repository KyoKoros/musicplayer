from pygame import mixer
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
from tkinter import filedialog
from tkinter import ttk
import json
import bcrypt

'''Function to load user profiles from a JSON file'''
def load_user_profiles():
    try:
        with open('user_profiles.json', 'r') as file:
            user_profiles = json.load(file)
    except FileNotFoundError:
        user_profiles = {}
    return user_profiles

'''Function to save user profiles to a JSON file'''
def save_user_profiles(user_profiles):
    with open('user_profiles.json', 'w') as file:
        json.dump(user_profiles, file)

'''Function to show the music player and hide login/register widgets'''
def show_music_player():
    '''Hide login/register widgets'''
    register_label.grid_remove()
    register_username_label.grid_remove()
    register_username.grid_remove()
    register_password_label.grid_remove()
    register_password.grid_remove()
    register_button.grid_remove()
    register_status_label.grid_remove()

    login_label.grid_remove()
    login_username_label.grid_remove()
    login_username.grid_remove()
    login_password_label.grid_remove()
    login_password.grid_remove()
    login_button.grid_remove()
    login_status_label.grid_remove()

    play_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
    pause_button.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
    stop_button.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
    Resume_button.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")
    previous_button.grid(row=2, column=4, padx=10, pady=10, sticky="nsew")
    next_button.grid(row=2, column=5, padx=10, pady=10, sticky="nsew")

    '''Call update_idletasks to ensure widgets have correct sizes'''
    root.update_idletasks()

    '''Calculate the required height based on the widgets and progress bar height'''
    required_height = (
        sum(widget.winfo_reqheight() for widget in [songs_list, play_button, song_info]) +
        progress_bar.winfo_reqheight() + 50
    )

    '''Update the window size to fit the contents'''
    root.geometry(f"600x{required_height}")

    '''Adjust column weights to make them expand equally'''
    for i in range(6):
        root.grid_columnconfigure(i, weight=1)

    '''Adjust row weights to make them expand equally'''
    for i in range(15):
        root.grid_rowconfigure(i, weight=1)

'''Function to log out and show login/register widgets'''
def logout_user():
    global song_paths  # Access the global variable
    song_paths = {}  # Clear the playlist

    # Clear the song info
    song_info['text'] = ""

    # Show login/register widgets and clear login status
    show_login_register_widgets()
    clear_login_status()

    # Reset the window size to the initial size
    root.geometry("600x800")

'''Function to show login/register widgets and clear login status'''
def show_login_register_widgets():
    register_label.grid()
    register_username_label.grid()
    register_username.grid()
    register_password_label.grid()
    register_password.grid()
    register_button.grid()
    register_status_label.grid()

    login_label.grid()
    login_username_label.grid()
    login_username.grid()
    login_password_label.grid()
    login_password.grid()
    login_button.grid()
    login_status_label.grid()

'''Function to clear login status'''
def clear_login_status():
    login_status.set("")

'''Function to log in a user'''
def login_user():
    username = login_username.get()
    password = login_password.get()

    user_profiles = load_user_profiles()

    if username in user_profiles and bcrypt.checkpw(password.encode('utf-8'), user_profiles[username].encode('utf-8')):
        login_status.set("Login successful")
        show_music_player()
        messagebox.showinfo("Login Successful", "You have successfully logged in.")
    else:
        login_status.set("Login failed. Check your credentials.")

'''Function to check if a user is logged in'''
def is_user_logged_in():
    return login_status.get() == "Login successful"

'''Function to update the progress bar'''
def update_progress_bar():
    current_time = mixer.music.get_pos() // 1000
    song_length = song_length_var.get()
    if song_length > 0:
        progress = (current_time / song_length) * 100
        progress_bar['value'] = progress
    root.after(1000, update_progress_bar)

'''Function to play a song'''
def Play():
    if not is_user_logged_in():
        login_status.set("Please login first")
        return

    song = songs_list.get(ACTIVE)
    song_path = song_paths[song]
    mixer.music.load(song_path)
    mixer.music.play()
    song_length = mixer.Sound(song_path).get_length()
    song_info['text'] = f"Playing: {song}"
    song_length_var.set(song_length)
    progress_bar['maximum'] = 100
    root.after(1000, update_progress_bar)

'''Function to add songs to the playlist'''
def addsongs():
    temp_song = filedialog.askopenfilenames(initialdir=r"C:\Users\Kyo\Desktop", title="Choose a song",
                                            filetypes=(("mp3 Files", "*.mp3"),))
    for s in temp_song:
        s = s.replace(r"C:\Users\Kyo\Desktop", "")
        songs_list.insert(END, s)
        song_paths[s] = s

'''Function to delete a selected song from the playlist'''
def deletesong():
    curr_song = songs_list.curselection()
    selected_song = songs_list.get(curr_song)
    songs_list.delete(curr_song)
    del song_paths[selected_song]

'''Function to pause the song'''
def Pause():
    mixer.music.pause()

'''Function to stop the song'''
def Stop():
    mixer.music.stop()
    songs_list.selection_clear(ACTIVE)

'''Function to resume the song'''
def Resume():
    mixer.music.unpause()

'''Function to navigate to the previous song'''
def Previous():
    previous_one = songs_list.curselection()
    previous_one = previous_one[0] - 1
    temp2 = songs_list.get(previous_one)
    temp2 = song_paths[temp2]
    mixer.music.load(temp2)
    mixer.music.play()
    songs_list.selection_clear(0, END)
    songs_list.activate(previous_one)
    songs_list.selection_set(previous_one)

'''Function to navigate to the next song'''
def Next():
    next_one = songs_list.curselection()
    next_one = next_one[0] + 1
    temp = songs_list.get(next_one)
    temp = song_paths[temp]
    mixer.music.load(temp)
    mixer.music.play()
    songs_list.selection_clear(0, END)
    songs_list.activate(next_one)
    songs_list.selection_set(next_one)


'''Initialize the root window'''
root = Tk()
root.title('Kyo Music Player App')
root.geometry("600x800")
root.resizable(False, False)
'''Initialize the mixer from pygame for audio playback'''
mixer.init()


'''Create a Listbox widget for the playlist'''
songs_list = Listbox(root, selectmode=SINGLE, bg="#FCFCFC", fg="black", font=('arial', 15), height=12, width=47,
                     selectbackground="gray", selectforeground="black")
songs_list.grid(row=1, column=0, columnspan=6)

button_font = font.Font(family='Helvetica', size=12)


'''Create buttons for various playback actions (Play, Pause, Stop, etc.)'''
play_button = Button(root, text="Play", width=7, command=Play, bg="#F5FFFA")
play_button['font'] = button_font
play_button.grid(row=2, column=0, padx=10, pady=10)

pause_button = Button(root, text="Pause", width=7, command=Pause, bg="#F5FFFA")
pause_button['font'] = button_font
pause_button.grid(row=2, column=1, padx=10, pady=10)

stop_button = Button(root, text="Stop", width=7, command=Stop, bg="#F5FFFA")
stop_button['font'] = button_font
stop_button.grid(row=2, column=2, padx=10, pady=10)

Resume_button = Button(root, text="Resume", width=7, command=Resume, bg="#F5FFFA")
Resume_button['font'] = button_font
Resume_button.grid(row=2, column=3, padx=10, pady=10)

previous_button = Button(root, text="Prev", width=7, command=Previous, bg="#F5FFFA")
previous_button['font'] = button_font
previous_button.grid(row=2, column=4, padx=10, pady=10)

next_button = Button(root, text="Next", width=7, command=Next, bg="#F5FFFA")
next_button['font'] = button_font
next_button.grid(row=2, column=5, padx=10, pady=10)

'''Initialize a DoubleVar for song length and set it to 0.0'''
song_length_var = DoubleVar()
song_length_var.set(0.0)

'''Create a Label to display song information'''
song_info = Label(root, text="", font=('arial', 12))
song_info.grid(row=3, column=0, columnspan=6, pady=(0, 20))

'''Create a Progressbar to show the progress of the song'''
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate')
progress_bar.grid(row=4, column=0, columnspan=6, pady=(0, 20))

'''Dictionary to store song paths'''
song_paths = {}

'''Create a menu for adding songs and deleting songs from the playlist'''
my_menu = Menu(root)
root.config(menu=my_menu)
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Menu", menu=add_song_menu)
add_song_menu.add_command(label="Add songs", command=addsongs)
add_song_menu.add_command(label="Delete song", command=deletesong)

'''Add a "Logout" option to the menu'''
my_menu.add_command(label="Logout", command=logout_user)

'''Create labels and entry fields for registration'''
register_label = Label(root, text="Register", font=('arial', 15), fg="#800000")
register_label.grid(row=5, column=0, columnspan=6, pady=(20, 0))

register_username_label = Label(root, text="Username:", fg="#FF4500")
register_username_label.grid(row=6, column=0, pady=5)

register_username = Entry(root)
register_username.grid(row=6, column=1, pady=5)

register_password_label = Label(root, text="Password:", fg="#FF4500")
register_password_label.grid(row=7, column=0, pady=5)

register_password = Entry(root, show="*")
register_password.grid(row=7, column=1, pady=5)

'''Function to register a new user'''
def register_user():
    username = register_username.get()
    password = register_password.get()

    if not username or not password:
        register_status.set("Username and password are required.")
        return

    '''Password validation: 4 to 7 characters and at least one uppercase character'''
    if len(password) < 4 or len(password) > 7 or not any(char.isupper() for char in password):
        register_status.set("Password must be 4 to 7 characters long and contain at least one uppercase character.")
        return

    '''Hash the password before storing it'''
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    user_profiles = load_user_profiles()

    if username in user_profiles:
        register_status.set("Username already exists.")
    else:
        user_profiles[username] = hashed_password
        save_user_profiles(user_profiles)
        register_status.set("Registration successful. You can now log in.")
        register_username.delete(0, END)
        register_password.delete(0, END)
        messagebox.showinfo("Registration Successful", "You have successfully registered. You can now log in.")

register_button = Button(root, text="Register", command=register_user, bg="#FF6347")
register_button.grid(row=8, column=0, columnspan=3, pady=10)

register_status = StringVar()
register_status_label = Label(root, textvariable=register_status, fg="red", width=40, wraplength=250)
register_status_label.grid(row=9, column=0, columnspan=3, pady=5)  # Adjust the columnspan value as needed

login_label = Label(root, text="Login", font=('arial', 15), fg="#800000")
login_label.grid(row=10, column=0, columnspan=6, pady=(20, 0))

login_username_label = Label(root, text="Username:", fg="#FF4500")
login_username_label.grid(row=11, column=0, pady=5)

login_username = Entry(root)
login_username.grid(row=11, column=1, pady=5)

login_password_label = Label(root, text="Password:", fg="#FF4500")
login_password_label.grid(row=12, column=0, pady=5)

login_password = Entry(root, show="*")
login_password.grid(row=12, column=1, pady=5)

login_button = Button(root, text="Login", command=login_user, bg="#FF6347")
login_button.grid(row=13, column=0, columnspan=3, pady=10)

login_status = StringVar()
login_status_label = Label(root, textvariable=login_status, fg="green")
login_status_label.grid(row=14, column=0, columnspan=2, pady=5)


'''Start the main event loop'''
def main():
    '''Update the progress bar periodically'''
    root.after(1000, update_progress_bar)
    root.mainloop()

if __name__ == "__main__":
    main()