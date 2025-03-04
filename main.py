import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

# Function to load the tracks from the JSON file
def load_tracks(json_file):
    with open(json_file, 'r') as file:
        tracks = json.load(file)
    return tracks

# Function to create the setup folder
def create_setup_folder(car_name, track_name, week_input, season_input):
    base_dir = os.path.join(os.path.expanduser("~"), "Documents", "iRacing", "setups")  # Dynamic user directory
    car_dir = os.path.join(base_dir, car_name, "Garage 61")

    # Check if the car folder exists
    if not os.path.exists(car_dir):
        print(f"\n❌ ERROR: The car folder '{car_name}' does not exist in the setup directory.")
        return

    # Create the full folder structure
    final_path = os.path.join(car_dir, str(2025), f"Season {season_input}", f"Week {week_input}", track_name)

    # Create the folder structure if it doesn't exist
    if not os.path.exists(final_path):
        os.makedirs(final_path)
        return final_path
    else:
        print(f"\n⚠️ The folder already exists: {final_path}")
        return None

# Function to filter tracks based on user input
def on_track_input(event):
    typed_text = track_name_entry.get().lower()
    
    # Filter tracks that match the typed text
    filtered_tracks = [track for track in track_names if typed_text in track.lower()]
    
    # Update the listbox with the filtered tracks
    update_listbox(filtered_tracks)

# Function to update the listbox with tracks
def update_listbox(tracks):
    track_listbox.delete(0, tk.END)  # Clear the listbox
    
    # Add the filtered tracks to the listbox
    for track in tracks:
        track_listbox.insert(tk.END, track)

# Function to handle track selection from the listbox
def on_select_track(event):
    selected_track = track_listbox.get(track_listbox.curselection())
    track_name_entry.delete(0, tk.END)
    track_name_entry.insert(0, selected_track)  # Fill the text entry with the selected track

# Function to load car names from the setup directory
def load_car_names():
    car_dir = os.path.join(os.path.expanduser("~"), "Documents", "iRacing", "setups")  # Dynamic user directory
    if not os.path.exists(car_dir):
        print(f"❌ ERROR: The directory '{car_dir}' does not exist.")
        return []
    
    # Get all the folder names (cars) in the directory
    car_names = [folder for folder in os.listdir(car_dir) if os.path.isdir(os.path.join(car_dir, folder))]
    return car_names

# Function to confirm the setup folder creation
def on_confirm():
    car_name = car_name_entry.get()
    track_name = track_name_entry.get()
    week_input = int(week_input_entry.get())
    season_input = int(season_input_entry.get())
    
    folder_created = create_setup_folder(car_name, track_name, week_input, season_input)
    
    if folder_created:
        messagebox.showinfo("Success", f"Setup folder created successfully:\n{folder_created}")
        
        # Clear all the fields after successful creation
        clear_fields()
    else:
        messagebox.showwarning("Warning", "The folder already exists.")

# Function to clear all fields
def clear_fields():
    car_name_entry.set('')
    track_name_entry.delete(0, tk.END)
    week_input_entry.delete(0, tk.END)
    season_input_entry.delete(0, tk.END)
    track_listbox.delete(0, tk.END)  # Clear listbox
    track_name_entry.focus()  # Focus back to the track name entry

# Load the tracks from the JSON file
tracks = load_tracks("tracks.json")  # The "tracks.json" file is in the same folder as the script

# Create the main window
root = tk.Tk()
root.title("Select Track and Car")

# Load the track names for filtering
track_names = [track['name'] for track in tracks]

# Load the car names
car_names = load_car_names()

# Add an entry for the car name
tk.Label(root, text="Choose the car name:").grid(row=0, column=0)
car_name_entry = ttk.Combobox(root, values=car_names)
car_name_entry.grid(row=0, column=1)

# Add an entry for the week number
tk.Label(root, text="Enter the week number (e.g., 12):").grid(row=1, column=0)
week_input_entry = tk.Entry(root)
week_input_entry.grid(row=1, column=1)

# Add an entry for the season number
tk.Label(root, text="Enter the season number (e.g., 1):").grid(row=2, column=0)
season_input_entry = tk.Entry(root)
season_input_entry.grid(row=2, column=1)

# Add an entry for the track name and a listbox for suggestions
tk.Label(root, text="Enter the track name:").grid(row=3, column=0)
track_name_entry = tk.Entry(root)
track_name_entry.grid(row=3, column=1)

# Listbox to display track suggestions
track_listbox = tk.Listbox(root, height=6, width=40)
track_listbox.grid(row=4, column=1)
track_listbox.bind("<ButtonRelease-1>", on_select_track)  # When clicked, fill the entry with the selected track

# Add a key release event to filter tracks as the user types
track_name_entry.bind("<KeyRelease>", on_track_input)

# Button to confirm the setup creation
confirm_button = tk.Button(root, text="Create Setup Folder", command=on_confirm)
confirm_button.grid(row=5, column=1)

# Start the Tkinter event loop
root.mainloop()
