import os
import json
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from tkcalendar import DateEntry


#This file will be the main file in this program used to let the user track movies and tv shows that the user has watched and would like to rate.
#The user will be able to add a movie or tv show to the database and then rate it.
#The user will also be able to see the ratings of the movie or tv show.
#The user will be able to search through their list of movies and tv shows and find what they liked and may rewatch it.
#The program will keep track of what platform the content is watchable on.
#The program will let the user keep track of movies and tv shwos that they have not watched yet but want to save into a backlog.


class MediaTracker:
    def __init__(self):
        self.media_list = []
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists('media_database.json'):
                with open('media_database.json', 'r') as file:
                    self.media_list = json.load(file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load database: {str(e)}")

    def save_data(self):
        try:
            with open('media_database.json', 'w') as file:
                json.dump(self.media_list, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save database: {str(e)}")

    def add_media(self, title, media_type, platform, rating=None, watched=False, watch_date=None):
        media = {
            'Title': title,
            'Type': media_type,
            'Platform': platform,
            'Watched': watched,
            'Rating': rating,
            'WatchDate': watch_date
        }
        self.media_list.append(media)
        self.save_data()

    def rate_media(self, title, rating):
        for media in self.media_list:
            if media['Title'] == title:
                media['Rating'] = rating
                self.save_data()
                return f"Rated {title} with {rating} stars."
        return "Media not found."

    def mark_as_watched(self, title, watch_date=None):
        for media in self.media_list:
            if media['Title'] == title:
                media['Watched'] = True
                media['WatchDate'] = watch_date
                self.save_data()
                return f"Marked {title} as watched."
        return "Media not found."

    def search_media(self, title):
        for media in self.media_list:
            if media['Title'] == title:
                return media
        return "Media not found."

    def list_media(self):
        return self.media_list

class MediaTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Tracker")
        self.root.geometry("900x700")
        
        # Ensure window is visible
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        
        # Configure theme colors
        self.bg_color = 'white'
        self.accent_color = '#007AFF'  # macOS blue
        self.text_color = 'black'
        self.success_color = '#34C759'  # macOS green
        self.error_color = '#FF3B30'    # macOS red
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('default')  # Use default theme
        
        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color, font=('Helvetica', 10))
        self.style.configure('TButton', background=self.accent_color, foreground='white', font=('Helvetica', 10))
        self.style.configure('TEntry', fieldbackground='white', font=('Helvetica', 10))
        self.style.configure('TCombobox', fieldbackground='white', font=('Helvetica', 10))
        self.style.configure('TNotebook', background=self.bg_color)
        self.style.configure('TNotebook.Tab', background=self.bg_color, padding=[10, 5])
        self.style.map('TButton', background=[('active', self.accent_color)])
        
        self.tracker = MediaTracker()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(header_frame, text="Media Tracker", font=('Helvetica', 24, 'bold')).pack()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Add Media Tab
        self.add_tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.add_tab, text="Add Media")
        self.setup_add_tab()
        
        # Rate Media Tab
        self.rate_tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.rate_tab, text="Rate Media")
        self.setup_rate_tab()
        
        # Mark as Watched Tab
        self.watch_tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.watch_tab, text="Mark as Watched")
        self.setup_watch_tab()
        
        # Search Tab
        self.search_tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.search_tab, text="Search")
        self.setup_search_tab()
        
        # List Media Tab
        self.list_tab = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.list_tab, text="List Media")
        self.setup_list_tab()
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

    def on_closing(self):
        try:
            self.tracker.save_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save database: {str(e)}")
        self.root.destroy()

    def create_styled_entry(self, parent, width=40):
        entry = ttk.Entry(parent, width=width)
        entry.configure(style='TEntry')
        return entry

    def create_styled_button(self, parent, text, command):
        button = ttk.Button(parent, text=text, command=command)
        button.configure(style='TButton')
        return button

    def setup_add_tab(self):
        # Title
        ttk.Label(self.add_tab, text="Title:", font=('Helvetica', 11)).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.title_entry = self.create_styled_entry(self.add_tab)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Type
        ttk.Label(self.add_tab, text="Type:", font=('Helvetica', 11)).grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(self.add_tab, textvariable=self.type_var, values=["Movie", "TV Show"], width=37)
        self.type_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Platform
        ttk.Label(self.add_tab, text="Platform:", font=('Helvetica', 11)).grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        self.platform_var = tk.StringVar()
        self.platform_combo = ttk.Combobox(self.add_tab, textvariable=self.platform_var, 
                                         values=["Netflix", "Amazon", "Hulu", "Disney+", "Apple TV"], width=37)
        self.platform_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Rating
        ttk.Label(self.add_tab, text="Rating (1-10):", font=('Helvetica', 11)).grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        self.add_rating_var = tk.StringVar()
        self.add_rating_combo = ttk.Combobox(self.add_tab, textvariable=self.add_rating_var, 
                                           values=["Not Rated", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], width=37)
        self.add_rating_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        self.add_rating_combo.set("Not Rated")
        
        # Watched Status
        self.watched_var = tk.BooleanVar()
        self.watched_check = ttk.Checkbutton(self.add_tab, text="Mark as Watched", 
                                           variable=self.watched_var, command=self.toggle_watch_date)
        self.watched_check.grid(row=4, column=0, columnspan=2, pady=(0, 10))
        
        # Watch Date
        self.watch_date_frame = ttk.Frame(self.add_tab)
        self.watch_date_frame.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        ttk.Label(self.watch_date_frame, text="Watch Date:", font=('Helvetica', 11)).pack(side=tk.LEFT, padx=(0, 10))
        self.watch_date_cal = DateEntry(self.watch_date_frame, width=12, background='darkblue',
                                      foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.watch_date_cal.pack(side=tk.LEFT)
        self.watch_date_frame.grid_remove()  # Initially hidden
        
        # Add button
        self.create_styled_button(self.add_tab, "Add Media", self.add_media).grid(row=6, column=0, columnspan=2, pady=20)

    def setup_rate_tab(self):
        # Title
        ttk.Label(self.rate_tab, text="Title:", font=('Helvetica', 11)).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.rate_title_entry = self.create_styled_entry(self.rate_tab)
        self.rate_title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Rating
        ttk.Label(self.rate_tab, text="Rating (1-10):", font=('Helvetica', 11)).grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.rating_var = tk.StringVar()
        self.rating_combo = ttk.Combobox(self.rate_tab, textvariable=self.rating_var, 
                                       values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], width=37)
        self.rating_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Rate button
        self.create_styled_button(self.rate_tab, "Rate Media", self.rate_media).grid(row=2, column=0, columnspan=2, pady=20)

    def setup_watch_tab(self):
        # Title
        ttk.Label(self.watch_tab, text="Title:", font=('Helvetica', 11)).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.watch_title_entry = self.create_styled_entry(self.watch_tab)
        self.watch_title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))

        # Watch Date
        ttk.Label(self.watch_tab, text="Watch Date:", font=('Helvetica', 11)).grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.watch_tab_date_cal = DateEntry(self.watch_tab, width=12, background='darkblue',
                                          foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.watch_tab_date_cal.grid(row=1, column=1, sticky=tk.W, pady=(0, 10))
        
        # Watch button
        self.create_styled_button(self.watch_tab, "Mark as Watched", self.mark_watched).grid(row=2, column=0, columnspan=2, pady=20)

    def toggle_watch_date(self):
        if self.watched_var.get():
            self.watch_date_frame.grid()
        else:
            self.watch_date_frame.grid_remove()

    def setup_search_tab(self):
        # Title
        ttk.Label(self.search_tab, text="Title:", font=('Helvetica', 11)).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.search_title_entry = self.create_styled_entry(self.search_tab)
        self.search_title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Search results
        self.search_result = ScrolledText(self.search_tab, height=15, width=60, font=('Segoe UI', 10))
        self.search_result.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Search button
        self.create_styled_button(self.search_tab, "Search", self.search_media).grid(row=2, column=0, columnspan=2, pady=20)

    def setup_list_tab(self):
        # List results
        self.list_result = ScrolledText(self.list_tab, height=25, width=70, font=('Segoe UI', 10))
        self.list_result.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Refresh button
        self.create_styled_button(self.list_tab, "Refresh List", self.refresh_list).grid(row=1, column=0, pady=20)
        self.refresh_list()

    def add_media(self):
        title = self.title_entry.get()
        media_type = self.type_var.get()
        platform = self.platform_var.get()
        rating = self.add_rating_var.get()
        watched = self.watched_var.get()
        watch_date = self.watch_date_cal.get_date().strftime("%Y-%m-%d") if watched else None
        
        if not all([title, media_type, platform]):
            messagebox.showerror("Error", "Please fill in all required fields (Title, Type, Platform)")
            return
        
        # Convert rating to None if "Not Rated" is selected
        rating = None if rating == "Not Rated" else rating
            
        self.tracker.add_media(title, media_type, platform, rating, watched, watch_date)
        messagebox.showinfo("Success", f"Added {title} to the database")
        
        # Clear all fields
        self.title_entry.delete(0, tk.END)
        self.type_var.set("")
        self.platform_var.set("")
        self.add_rating_var.set("Not Rated")
        self.watched_var.set(False)
        self.watch_date_frame.grid_remove()
        self.watch_date_cal.set_date(datetime.now())

    def rate_media(self):
        title = self.rate_title_entry.get()
        rating = self.rating_var.get()
        
        if not all([title, rating]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        result = self.tracker.rate_media(title, rating)
        messagebox.showinfo("Result", result)
        self.rate_title_entry.delete(0, tk.END)
        self.rating_var.set("")

    def mark_watched(self):
        title = self.watch_title_entry.get()
        watch_date = self.watch_tab_date_cal.get_date().strftime("%Y-%m-%d")
        
        if not title:
            messagebox.showerror("Error", "Please enter a title")
            return
            
        result = self.tracker.mark_as_watched(title, watch_date)
        messagebox.showinfo("Result", result)
        self.watch_title_entry.delete(0, tk.END)
        self.watch_tab_date_cal.set_date(datetime.now())

    def search_media(self):
        title = self.search_title_entry.get()
        
        if not title:
            messagebox.showerror("Error", "Please enter a title")
            return
            
        result = self.tracker.search_media(title)
        self.search_result.delete(1.0, tk.END)
        self.search_result.insert(tk.END, str(result))
        self.search_title_entry.delete(0, tk.END)

    def refresh_list(self):
        media_list = self.tracker.list_media()
        self.list_result.delete(1.0, tk.END)
        if not media_list:
            self.list_result.insert(tk.END, "No media in the database")
        else:
            for media in media_list:
                self.list_result.insert(tk.END, f"Title: {media['Title']}\n")
                self.list_result.insert(tk.END, f"Type: {media['Type']}\n")
                self.list_result.insert(tk.END, f"Platform: {media['Platform']}\n")
                self.list_result.insert(tk.END, f"Watched: {'Yes' if media['Watched'] else 'No'}\n")
                if media['Watched'] and media.get('WatchDate'):
                    self.list_result.insert(tk.END, f"Watch Date: {media['WatchDate']}\n")
                self.list_result.insert(tk.END, f"Rating: {media['Rating'] or 'Not rated'}\n")
                self.list_result.insert(tk.END, "-" * 50 + "\n")

def main():
    print("Starting application...")
    root = tk.Tk()
    print("Tk root created")
    
    # Set up the window
    root.title("Media Tracker")
    root.geometry("900x700")
    
    # Create a simple frame
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create a simple label
    label = ttk.Label(main_frame, text="Media Tracker", font=('Helvetica', 24, 'bold'))
    label.pack(pady=20)
    
    # Create a simple button
    button = ttk.Button(main_frame, text="Test Button", command=lambda: print("Button clicked"))
    button.pack(pady=20)
    
    # Create a simple entry
    entry = ttk.Entry(main_frame, width=40)
    entry.pack(pady=20)
    
    # Create a simple combobox
    combo = ttk.Combobox(main_frame, values=["Option 1", "Option 2", "Option 3"], width=37)
    combo.pack(pady=20)
    
    # Make sure the window is visible
    root.deiconify()
    root.lift()
    root.focus_force()
    
    # Start the event loop
    print("Starting mainloop...")
    root.mainloop()
    print("Mainloop ended")

if __name__ == "__main__":
    main()
            
