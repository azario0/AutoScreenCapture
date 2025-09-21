import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyautogui
import threading
import time
import os
from datetime import datetime
from PIL import Image, ImageTk
import sys

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated Screenshot Capture")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variables
        self.save_folder = tk.StringVar(value=os.path.expanduser("~/Desktop"))
        self.interval = tk.IntVar(value=60)  # seconds
        self.is_capturing = False
        self.capture_thread = None
        self.screenshot_count = 0
        
        # Create GUI
        self.create_widgets()
        
        # Center window
        self.center_window()
        
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
    def create_widgets(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="📸 Automated Screenshot Capture", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Folder selection frame
        folder_frame = ttk.LabelFrame(main_frame, text="Save Location", padding="10")
        folder_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        folder_frame.columnconfigure(0, weight=1)
        
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.save_folder, 
                                     font=('Arial', 10), state='readonly')
        self.folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.browse_btn = ttk.Button(folder_frame, text="Browse", 
                                    command=self.browse_folder)
        self.browse_btn.grid(row=0, column=1)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Capture Settings", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Interval setting
        ttk.Label(settings_frame, text="Screenshot Interval:").grid(row=0, column=0, sticky=tk.W)
        
        interval_frame = ttk.Frame(settings_frame)
        interval_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        self.interval_scale = ttk.Scale(interval_frame, from_=5, to=300, 
                                       variable=self.interval, orient=tk.HORIZONTAL)
        self.interval_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.interval_scale.bind("<Motion>", self.update_interval_label)
        
        self.interval_label = ttk.Label(interval_frame, text=f"{self.interval.get()} seconds")
        self.interval_label.grid(row=0, column=1, padx=(10, 0))
        
        interval_frame.columnconfigure(0, weight=1)
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, pady=(0, 15))
        
        self.start_btn = ttk.Button(control_frame, text="▶ Start Capture", 
                                   command=self.start_capture, style='Accent.TButton')
        self.start_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_btn = ttk.Button(control_frame, text="⏹ Stop Capture", 
                                  command=self.stop_capture, state='disabled')
        self.stop_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.test_btn = ttk.Button(control_frame, text="📷 Test Screenshot", 
                                  command=self.take_test_screenshot)
        self.test_btn.grid(row=0, column=2)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(status_frame, text="Ready to capture screenshots", 
                                     font=('Arial', 10))
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.count_label = ttk.Label(status_frame, text="Screenshots taken: 0", 
                                    font=('Arial', 10))
        self.count_label.grid(row=1, column=0, sticky=tk.W)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Preview frame (initially hidden)
        self.preview_frame = ttk.LabelFrame(main_frame, text="Last Screenshot Preview", padding="10")
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.grid(row=0, column=0)
        
        # Footer
        footer_label = ttk.Label(main_frame, text="Screenshots will be saved with timestamp filenames", 
                                font=('Arial', 9), foreground='gray')
        footer_label.grid(row=6, column=0, columnspan=3, pady=(15, 0))
        
    def update_interval_label(self, event=None):
        self.interval_label.config(text=f"{int(self.interval.get())} seconds")
        
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.save_folder.get(),
                                       title="Select folder to save screenshots")
        if folder:
            self.save_folder.set(folder)
            
    def take_test_screenshot(self):
        try:
            if not os.path.exists(self.save_folder.get()):
                os.makedirs(self.save_folder.get())
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_screenshot_{timestamp}.png"
            filepath = os.path.join(self.save_folder.get(), filename)
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            
            # Show preview
            self.show_preview(screenshot)
            
            self.status_label.config(text=f"Test screenshot saved: {filename}")
            messagebox.showinfo("Success", f"Test screenshot saved successfully!\n{filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to take test screenshot:\n{str(e)}")
            
    def show_preview(self, screenshot):
        # Resize screenshot for preview (max 200x150)
        preview_size = (200, 150)
        screenshot.thumbnail(preview_size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(screenshot)
        
        # Update preview
        self.preview_label.config(image=photo)
        self.preview_label.image = photo  # Keep a reference
        
        # Show preview frame
        self.preview_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
    def start_capture(self):
        if not os.path.exists(self.save_folder.get()):
            try:
                os.makedirs(self.save_folder.get())
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create save folder:\n{str(e)}")
                return
                
        self.is_capturing = True
        self.screenshot_count = 0
        
        # Update UI
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.browse_btn.config(state='disabled')
        self.test_btn.config(state='disabled')
        
        self.progress.start(10)
        self.status_label.config(text="Starting capture...")
        
        # Start capture thread
        self.capture_thread = threading.Thread(target=self.capture_loop, daemon=True)
        self.capture_thread.start()
        
    def stop_capture(self):
        self.is_capturing = False
        
        # Update UI
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.browse_btn.config(state='normal')
        self.test_btn.config(state='normal')
        
        self.progress.stop()
        self.status_label.config(text=f"Capture stopped. Total screenshots: {self.screenshot_count}")
        
    def capture_loop(self):
        while self.is_capturing:
            try:
                # Take screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                filepath = os.path.join(self.save_folder.get(), filename)
                
                screenshot = pyautogui.screenshot()
                screenshot.save(filepath)
                
                self.screenshot_count += 1
                
                # Update UI in main thread
                self.root.after(0, self.update_capture_status, filename)
                
                # Wait for interval
                time.sleep(self.interval.get())
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", 
                    f"Screenshot capture failed:\n{str(e)}"))
                break
                
    def update_capture_status(self, filename):
        self.status_label.config(text=f"Last capture: {filename}")
        self.count_label.config(text=f"Screenshots taken: {self.screenshot_count}")
        
    def on_closing(self):
        if self.is_capturing:
            if messagebox.askokcancel("Quit", "Screenshot capture is running. Stop and quit?"):
                self.stop_capture()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    # Check if pyautogui is available
    try:
        import pyautogui
        # Disable pyautogui failsafe (optional)
        pyautogui.FAILSAFE = True
    except ImportError:
        messagebox.showerror("Missing Dependency", 
            "This application requires 'pyautogui' to be installed.\n\n"
            "Install it using: pip install pyautogui")
        return
        
    try:
        from PIL import Image, ImageTk
    except ImportError:
        messagebox.showerror("Missing Dependency", 
            "This application requires 'Pillow' to be installed.\n\n"
            "Install it using: pip install Pillow")
        return
    
    root = tk.Tk()
    app = ScreenshotApp(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    main()
    