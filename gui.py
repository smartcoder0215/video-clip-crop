import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from video_clipper import clip_video, crop_video_bottom
from image_converter import convert_image
from audio_processor import extract_audio
from PIL import Image, ImageTk
import cv2
import threading
from moviepy.editor import VideoFileClip
import customtkinter as ctk
import json

# Try to import tkinterdnd2, but provide a fallback if not available
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DRAG_AND_DROP_AVAILABLE = True
except ImportError:
    print("Warning: tkinterdnd2 not available. Drag and drop will be disabled.")
    DRAG_AND_DROP_AVAILABLE = False
    # Create a dummy TkinterDnD class that just returns a regular Tk window
    class TkinterDnD:
        @staticmethod
        def Tk():
            return tk.Tk()

# --- Tooltip helper ---
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)
    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0,0,0,0)
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1, font=("tahoma", "10", "normal"))
        label.pack(ipadx=1)
    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

# --- Toast notification helper ---
def show_toast(root, message, color="#232946"):
    toast = tk.Toplevel(root)
    toast.overrideredirect(True)
    toast.configure(bg=color)
    toast.attributes("-topmost", True)
    x = root.winfo_rootx() + 50
    y = root.winfo_rooty() + 50
    toast.geometry(f"+{x}+{y}")
    label = tk.Label(toast, text=message, bg=color, fg="#fff", font=("Arial", 12, "bold"))
    label.pack(ipadx=10, ipady=5)
    toast.after(1800, toast.destroy)

class MediaToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Tools")
        self.root.geometry("900x700")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main container
        self.main_container = ctk.CTkFrame(root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(pady=10, expand=True, fill="both")
        
        # Create tabs
        self.video_tab = ctk.CTkFrame(self.notebook)
        self.image_tab = ctk.CTkFrame(self.notebook)
        self.audio_tab = ctk.CTkFrame(self.notebook)
        self.settings_tab = ctk.CTkFrame(self.notebook)
        
        self.notebook.add(self.video_tab, text="Video Tools")
        self.notebook.add(self.image_tab, text="Image Tools")
        self.notebook.add(self.audio_tab, text="Audio Tools")
        self.notebook.add(self.settings_tab, text="Settings")
        
        # Initialize variables
        self.current_video = None
        self.current_image = None
        self.processing = False
        self.last_output_dir = self.load_last_output_dir()
        
        # Setup tabs
        self.setup_video_tab()
        self.setup_image_tab()
        self.setup_audio_tab()
        self.setup_settings_tab()
        
        # Setup drag and drop if available
        if DRAG_AND_DROP_AVAILABLE:
            self.setup_drag_drop()
    
    def load_last_output_dir(self):
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r") as f:
                    data = json.load(f)
                    return data.get("output_dir", "")
            except Exception:
                return ""
        return ""

    def save_last_output_dir(self, directory):
        try:
            with open("settings.json", "w") as f:
                json.dump({"output_dir": directory}, f)
        except Exception:
            pass
    
    def setup_drag_drop(self):
        if DRAG_AND_DROP_AVAILABLE:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.handle_drop)
            # Highlight area on drag
            self.root.dnd_bind('<<DragEnter>>', lambda e: self.root.configure(bg="#eebf3f"))
            self.root.dnd_bind('<<DragLeave>>', lambda e: self.root.configure(bg="#232946"))
            self.root.dnd_bind('<<Drop>>', lambda e: self.root.configure(bg="#232946"))
    
    def handle_drop(self, event):
        if not DRAG_AND_DROP_AVAILABLE:
            return
            
        file_path = event.data
        if file_path.lower().endswith(('.mp4', '.avi', '.mov')):
            self.notebook.select(0)  # Switch to video tab
            self.video_input_label.configure(text=file_path)
            self.current_video = file_path
            self.update_video_preview()
        elif file_path.lower().endswith(('.webp', '.png', '.jpg', '.jpeg')):
            self.notebook.select(1)  # Switch to image tab
            self.image_input_label.configure(text=file_path)
            self.current_image = file_path
            self.update_image_preview()
    
    def setup_video_tab(self):
        # Modern color palette
        section_bg = "#232946"
        highlight_bg = "#2a4d6c"
        heading_fg = "#eebf3f"
        label_fg = "#e0e0e0"
        # Video clip section
        clip_frame = ctk.CTkFrame(self.video_tab, fg_color=section_bg)
        clip_frame.pack(fill="x", padx=16, pady=(16, 8))
        
        clip_heading = ctk.CTkLabel(clip_frame, text="✂️ Video Cutting", font=("Arial", 18, "bold"), text_color=heading_fg)
        clip_heading.pack(fill="x", pady=(8, 12))
        
        # Preview section
        preview_frame = ctk.CTkFrame(clip_frame, fg_color=highlight_bg)
        preview_frame.pack(fill="x", pady=8)
        
        self.video_preview = ctk.CTkLabel(preview_frame, text="No video selected", text_color=label_fg)
        self.video_preview.pack(fill="x", pady=8)
        
        # File selection
        file_frame = ctk.CTkFrame(clip_frame, fg_color=section_bg)
        file_frame.pack(fill="x", pady=8)
        
        ctk.CTkButton(file_frame, text="🎬 Select Input Video", command=self.select_video_input).pack(fill="x", pady=5)
        self.video_input_label = ctk.CTkLabel(file_frame, text="No file selected", text_color=label_fg)
        self.video_input_label.pack(fill="x")
        
        ctk.CTkButton(file_frame, text="💾 Select Output Location", command=self.select_video_output).pack(fill="x", pady=5)
        self.video_output_label = ctk.CTkLabel(file_frame, text="No file selected", text_color=label_fg)
        self.video_output_label.pack(fill="x")
        
        # Time controls
        time_frame = ctk.CTkFrame(clip_frame, fg_color=section_bg)
        time_frame.pack(fill="x", pady=8)
        
        ctk.CTkLabel(time_frame, text="Start Time (seconds):", text_color=label_fg).pack(side="left")
        self.start_time = ctk.CTkEntry(time_frame, width=100, placeholder_text="e.g. 0.0")
        self.start_time.pack(side="left", padx=5)
        
        ctk.CTkLabel(time_frame, text="End Time (seconds):", text_color=label_fg).pack(side="left", padx=5)
        self.end_time = ctk.CTkEntry(time_frame, width=100, placeholder_text="e.g. 10.0")
        self.end_time.pack(side="left")
        
        # Progress bar and status for video cutting
        self.cut_progress = ctk.CTkProgressBar(clip_frame)
        self.cut_progress.pack(fill="x", pady=5)
        self.cut_progress.set(0)
        self.cut_status = ctk.CTkLabel(clip_frame, text="Idle", text_color="#ffcc00")
        self.cut_status.pack(fill="x", pady=2)
        
        # Action buttons
        button_frame = ctk.CTkFrame(clip_frame, fg_color=section_bg)
        button_frame.pack(fill="x", pady=8)
        
        ctk.CTkButton(button_frame, text="✂️ Cut Video", command=self.process_video_clip).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🔄 Rotate Video", command=self.rotate_video).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="⏩ Adjust Speed", command=self.adjust_video_speed).pack(side="left", padx=5)
        
        # --- HIGHLIGHTED Video crop section ---
        crop_frame = ctk.CTkFrame(self.video_tab, fg_color=highlight_bg)
        crop_frame.pack(fill="x", padx=16, pady=(24, 16))
        
        crop_label = ctk.CTkLabel(crop_frame, text="✂️ Video Cropping", font=("Arial", 18, "bold"), text_color=heading_fg)
        crop_label.pack(fill="x", pady=(8, 12))
        
        ctk.CTkButton(crop_frame, text="🎬 Select Input Video", command=self.select_crop_input).pack(fill="x", pady=5)
        self.crop_input_label = ctk.CTkLabel(crop_frame, text="No file selected", text_color=label_fg)
        self.crop_input_label.pack(fill="x")
        
        ctk.CTkButton(crop_frame, text="💾 Select Output Location", command=self.select_crop_output).pack(fill="x", pady=5)
        self.crop_output_label = ctk.CTkLabel(crop_frame, text="No file selected", text_color=label_fg)
        self.crop_output_label.pack(fill="x")
        
        height_frame = ctk.CTkFrame(crop_frame, fg_color=highlight_bg)
        height_frame.pack(fill="x", pady=8)
        
        ctk.CTkLabel(height_frame, text="Height to keep (pixels):", text_color=label_fg).pack(side="left")
        self.crop_height = ctk.CTkEntry(height_frame, width=100, placeholder_text="e.g. 360")
        self.crop_height.pack(side="left", padx=5)
        
        # Cropping progress bar and status
        self.crop_progress = ctk.CTkProgressBar(crop_frame)
        self.crop_progress.pack(fill="x", pady=5)
        self.crop_progress.set(0)
        self.crop_status = ctk.CTkLabel(crop_frame, text="Idle", text_color="#ffcc00")
        self.crop_status.pack(fill="x", pady=2)
        
        ctk.CTkButton(crop_frame, text="✂️ Crop Video", command=self.process_video_crop).pack(fill="x", pady=5)
    
    def setup_image_tab(self):
        section_bg = "#232946"
        heading_fg = "#eebf3f"
        label_fg = "#e0e0e0"
        # Image conversion section
        convert_frame = ctk.CTkFrame(self.image_tab, fg_color=section_bg)
        convert_frame.pack(fill="both", padx=16, pady=(16, 8), expand=True)
        
        image_heading = ctk.CTkLabel(convert_frame, text="🖼️ Image Type Converter", font=("Arial", 18, "bold"), text_color=heading_fg)
        image_heading.pack(fill="x", pady=(8, 12))
        
        # Preview section
        preview_frame = ctk.CTkFrame(convert_frame, fg_color="#2a4d6c")
        preview_frame.pack(fill="x", pady=8)
        self.image_preview = ctk.CTkLabel(preview_frame, text="No image selected", text_color=label_fg)
        self.image_preview.pack(fill="x", pady=8)
        
        # File selection
        file_frame = ctk.CTkFrame(convert_frame, fg_color=section_bg)
        file_frame.pack(fill="x", pady=8)
        self.image_input_label = ctk.CTkLabel(file_frame, text="No file selected", text_color=label_fg)
        ctk.CTkButton(file_frame, text="🖼️ Select Input Image", command=self.select_image_input).pack(fill="x", pady=5)
        self.image_input_label.pack(fill="x")
        self.image_output_label = ctk.CTkLabel(file_frame, text="No file selected", text_color=label_fg)
        ctk.CTkButton(file_frame, text="💾 Select Output Location", command=self.select_image_output).pack(fill="x", pady=5)
        self.image_output_label.pack(fill="x")
        
        # Format selection
        format_frame = ctk.CTkFrame(convert_frame, fg_color=section_bg)
        format_frame.pack(fill="x", pady=8)
        self.format_var = tk.StringVar(value="PNG")
        ctk.CTkRadioButton(format_frame, text="PNG", variable=self.format_var, value="PNG").pack(side="left", padx=5)
        ctk.CTkRadioButton(format_frame, text="JPEG", variable=self.format_var, value="JPEG").pack(side="left", padx=5)
        ctk.CTkRadioButton(format_frame, text="JFIF", variable=self.format_var, value="JFIF").pack(side="left")
        
        # Progress bar and status for image conversion
        self.image_progress = ctk.CTkProgressBar(convert_frame)
        self.image_progress.pack(fill="x", pady=5)
        self.image_progress.set(0)
        self.image_status = ctk.CTkLabel(convert_frame, text="Idle", text_color="#ffcc00")
        self.image_status.pack(fill="x", pady=2)
        
        # Only the convert button
        button_frame = ctk.CTkFrame(convert_frame, fg_color=section_bg)
        button_frame.pack(fill="x", pady=8)
        self.convert_button = ctk.CTkButton(button_frame, text="🖼️ Convert Image", command=self.process_image)
        self.convert_button.pack(side="left", padx=5)
    
    def setup_audio_tab(self):
        section_bg = "#232946"
        heading_fg = "#eebf3f"
        label_fg = "#e0e0e0"
        # Audio extraction section
        extract_frame = ctk.CTkFrame(self.audio_tab, fg_color=section_bg)
        extract_frame.pack(fill="both", padx=16, pady=(16, 8), expand=True)
        audio_heading = ctk.CTkLabel(extract_frame, text="🔊 Audio Extraction", font=("Arial", 18, "bold"), text_color=heading_fg)
        audio_heading.pack(fill="x", pady=(8, 12))
        ctk.CTkButton(extract_frame, text="🎬 Select Video", command=self.select_audio_input).pack(fill="x", pady=5)
        self.audio_input_label = ctk.CTkLabel(extract_frame, text="No file selected", text_color=label_fg)
        self.audio_input_label.pack(fill="x")
        ctk.CTkButton(extract_frame, text="💾 Select Output Location", command=self.select_audio_output).pack(fill="x", pady=5)
        self.audio_output_label = ctk.CTkLabel(extract_frame, text="No file selected", text_color=label_fg)
        self.audio_output_label.pack(fill="x")
        # Format selection
        format_frame = ctk.CTkFrame(extract_frame, fg_color=section_bg)
        format_frame.pack(fill="x", pady=8)
        self.audio_format_var = tk.StringVar(value="MP3")
        ctk.CTkRadioButton(format_frame, text="MP3", variable=self.audio_format_var, value="MP3").pack(side="left", padx=5)
        ctk.CTkRadioButton(format_frame, text="WAV", variable=self.audio_format_var, value="WAV").pack(side="left")
        # Volume adjustment
        volume_frame = ctk.CTkFrame(extract_frame, fg_color=section_bg)
        volume_frame.pack(fill="x", pady=8)
        ctk.CTkLabel(volume_frame, text="Volume:", text_color=label_fg).pack(side="left")
        self.volume = ctk.CTkSlider(volume_frame, from_=0, to=2)
        self.volume.pack(side="left", padx=5)
        self.volume.set(1)
        # Action button
        ctk.CTkButton(extract_frame, text="🔊 Extract Audio", command=self.extract_audio).pack(fill="x", pady=10)
    
    def setup_settings_tab(self):
        section_bg = "#232946"
        heading_fg = "#eebf3f"
        label_fg = "#e0e0e0"
        # Theme selection
        theme_frame = ctk.CTkFrame(self.settings_tab, fg_color=section_bg)
        theme_frame.pack(fill="x", padx=16, pady=(16, 8))
        ctk.CTkLabel(theme_frame, text="⚙️ Settings", font=("Arial", 18, "bold"), text_color=heading_fg).pack(fill="x", pady=(8, 12))
        ctk.CTkLabel(theme_frame, text="Theme:", text_color=label_fg).pack(side="left")
        self.theme_var = tk.StringVar(value="dark")
        ctk.CTkRadioButton(theme_frame, text="Dark", variable=self.theme_var, value="dark", command=self.change_theme).pack(side="left", padx=5)
        ctk.CTkRadioButton(theme_frame, text="Light", variable=self.theme_var, value="light", command=self.change_theme).pack(side="left")
        # Default output directory
        output_frame = ctk.CTkFrame(self.settings_tab, fg_color=section_bg)
        output_frame.pack(fill="x", padx=16, pady=(16, 8))
        ctk.CTkButton(output_frame, text="📁 Set Default Output Directory", command=self.set_default_output).pack(fill="x", pady=5)
        self.output_dir_label = ctk.CTkLabel(output_frame, text="No default directory set", text_color=label_fg)
        self.output_dir_label.pack(fill="x")
    
    def select_video_input(self):
        filename = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if filename:
            self.video_input_label.configure(text=filename)
            self.current_video = filename
            self.update_video_preview()
    
    def select_video_output(self):
        initialdir = self.last_output_dir or os.path.expanduser("~")
        filename = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")], initialdir=initialdir)
        if filename:
            self.video_output_label.configure(text=filename)
            self.last_output_dir = os.path.dirname(filename)
            self.save_last_output_dir(self.last_output_dir)
    
    def select_crop_input(self):
        filename = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if filename:
            self.crop_input_label.configure(text=filename)
            self.current_video = filename
            self.update_video_preview()
    
    def select_crop_output(self):
        initialdir = self.last_output_dir or os.path.expanduser("~")
        filename = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")], initialdir=initialdir)
        if filename:
            self.crop_output_label.configure(text=filename)
            self.last_output_dir = os.path.dirname(filename)
            self.save_last_output_dir(self.last_output_dir)
    
    def select_image_input(self):
        filename = filedialog.askopenfilename(filetypes=[
            ("All Image files", "*.webp *.png *.jpg *.jpeg *.jfif *.bmp *.gif *.tiff *.tif *.ico *.svg"),
            ("WebP files", "*.webp"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg;*.jpeg;*.jfif"),
            ("BMP files", "*.bmp"),
            ("GIF files", "*.gif"),
            ("TIFF files", "*.tiff;*.tif"),
            ("ICO files", "*.ico"),
            ("SVG files", "*.svg")
        ])
        if filename:
            self.image_input_label.configure(text=filename)
            self.current_image = filename
            self.update_image_preview()
    
    def select_image_output(self):
        initialdir = self.last_output_dir or os.path.expanduser("~")
        output_format = self.format_var.get()
        if output_format == "JPEG":
            defaultext = ".jpg"
            filetypes = [("JPEG files", "*.jpg;*.jpeg"), ("PNG files", "*.png"), ("BMP files", "*.bmp")]
        elif output_format == "JFIF":
            defaultext = ".jfif"
            filetypes = [("JFIF files", "*.jfif"), ("JPEG files", "*.jpg;*.jpeg"), ("PNG files", "*.png")]
        else:
            defaultext = ".png"
            filetypes = [("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("BMP files", "*.bmp")]
        filename = filedialog.asksaveasfilename(defaultextension=defaultext, filetypes=filetypes, initialdir=initialdir)
        if filename:
            self.image_output_label.configure(text=filename)
            self.last_output_dir = os.path.dirname(filename)
            self.save_last_output_dir(self.last_output_dir)
    
    def select_audio_input(self):
        filename = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if filename:
            self.audio_input_label.configure(text=filename)
    
    def select_audio_output(self):
        initialdir = self.last_output_dir or os.path.expanduser("~")
        filename = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav")], initialdir=initialdir)
        if filename:
            self.audio_output_label.configure(text=filename)
            self.last_output_dir = os.path.dirname(filename)
            self.save_last_output_dir(self.last_output_dir)
    
    def update_video_preview(self):
        if self.current_video:
            try:
                cap = cv2.VideoCapture(self.current_video)
                ret, frame = cap.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(frame, (320, 180))
                    photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                    self.video_preview.configure(image=photo)
                    self.video_preview.image = photo
                cap.release()
            except Exception as e:
                print(f"Error updating video preview: {str(e)}")
    
    def update_image_preview(self):
        if self.current_image:
            try:
                img = Image.open(self.current_image)
                img = img.resize((320, 180), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image=img)
                self.image_preview.configure(image=photo)
                self.image_preview.image = photo
            except Exception as e:
                print(f"Error updating image preview: {str(e)}")
    
    def process_video_clip(self):
        try:
            if self.processing:
                return
            self.processing = True
            self.cut_progress.set(0)
            self.cut_status.configure(text="Cutting...", text_color="#00ff00")
            self.disable_video_buttons()
            input_path = self.video_input_label.cget("text")
            output_path = self.video_output_label.cget("text")
            start_time_str = self.start_time.get().strip()
            end_time_str = self.end_time.get().strip()

            if input_path == "No file selected" or output_path == "No file selected":
                messagebox.showerror("Error", "Please select input and output files")
                return

            # Validate start and end time
            if not start_time_str or not end_time_str:
                messagebox.showerror("Error", "Please enter both start and end times.")
                return
            try:
                start_time = float(start_time_str)
                end_time = float(end_time_str)
            except ValueError:
                messagebox.showerror("Error", "Start and end times must be valid numbers.")
                return
            if start_time < 0 or end_time <= start_time:
                messagebox.showerror("Error", "End time must be greater than start time, and both must be non-negative.")
                return

            def process():
                clip_video(input_path, output_path, start_time, end_time)
                self.cut_progress.set(1)
                self.cut_status.configure(text="Done!", text_color="#00ff00")
                self.processing = False
                self.enable_video_buttons()
                show_toast(self.root, "Video clip created!")
                messagebox.showinfo("Success", "Video clip created successfully!")

            threading.Thread(target=process).start()

        except Exception as e:
            self.cut_status.configure(text="Error", text_color="#ff0000")
            self.processing = False
            self.enable_video_buttons()
            show_toast(self.root, "Error during video cut", color="#e74c3c")
            messagebox.showerror("Error", str(e))
    
    def process_video_crop(self):
        try:
            if self.processing:
                return
            self.processing = True
            self.crop_progress.set(0)
            self.crop_status.configure(text="Cropping...", text_color="#00ff00")
            self.disable_video_buttons()
            input_path = self.crop_input_label.cget("text")
            output_path = self.crop_output_label.cget("text")
            crop_height_str = self.crop_height.get().strip()

            if input_path == "No file selected" or output_path == "No file selected":
                messagebox.showerror("Error", "Please select input and output files")
                return
            if not crop_height_str:
                messagebox.showerror("Error", "Please enter the height to keep.")
                return
            try:
                crop_height = int(crop_height_str)
            except ValueError:
                messagebox.showerror("Error", "Height must be a valid integer.")
                return
            if crop_height <= 0:
                messagebox.showerror("Error", "Height must be a positive integer.")
                return

            def process():
                crop_video_bottom(input_path, output_path, crop_height)
                self.crop_progress.set(1)
                self.crop_status.configure(text="Done!", text_color="#00ff00")
                self.processing = False
                self.enable_video_buttons()
                show_toast(self.root, "Video cropped!")
                messagebox.showinfo("Success", "Video cropped successfully!")

            threading.Thread(target=process).start()

        except Exception as e:
            self.crop_status.configure(text="Error", text_color="#ff0000")
            self.processing = False
            self.enable_video_buttons()
            show_toast(self.root, "Error during cropping", color="#e74c3c")
            messagebox.showerror("Error", str(e))
    
    def process_image(self):
        try:
            if self.processing:
                return
            self.processing = True
            self.image_progress.set(0)
            self.image_status.configure(text="Converting...", text_color="#00ff00")
            self.disable_image_buttons()
            input_path = self.image_input_label.cget("text")
            output_path = self.image_output_label.cget("text")
            output_format = self.format_var.get()

            if input_path == "No file selected" or output_path == "No file selected":
                messagebox.showerror("Error", "Please select input and output files")
                return

            # Ensure output_path extension matches output_format
            ext = os.path.splitext(output_path)[1].lower()
            if output_format == "JPEG" and ext not in [".jpg", ".jpeg"]:
                output_path += ".jpg"
            elif output_format == "PNG" and ext != ".png":
                output_path += ".png"

            def process():
                convert_image(input_path, output_path, output_format)
                self.image_progress.set(1)
                self.image_status.configure(text="Done!", text_color="#00ff00")
                self.processing = False
                self.enable_image_buttons()
                show_toast(self.root, "Image converted!")
                messagebox.showinfo("Success", "Image converted successfully!")

            threading.Thread(target=process).start()

        except Exception as e:
            self.image_status.configure(text="Error", text_color="#ff0000")
            self.processing = False
            self.enable_image_buttons()
            show_toast(self.root, "Error during image conversion", color="#e74c3c")
            messagebox.showerror("Error", str(e))
    
    def rotate_video(self):
        if not self.current_video:
            messagebox.showerror("Error", "Please select a video first")
            return
        
        # Create rotation dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Rotate Video")
        dialog.geometry("300x150")
        
        angle_var = tk.StringVar(value="90")
        ctk.CTkRadioButton(dialog, text="90°", variable=angle_var, value="90").pack(pady=5)
        ctk.CTkRadioButton(dialog, text="180°", variable=angle_var, value="180").pack(pady=5)
        ctk.CTkRadioButton(dialog, text="270°", variable=angle_var, value="270").pack(pady=5)
        
        def apply_rotation():
            angle = int(angle_var.get())
            # Implement video rotation
            dialog.destroy()
        
        ctk.CTkButton(dialog, text="Apply", command=apply_rotation).pack(pady=10)
    
    def adjust_video_speed(self):
        if not self.current_video:
            messagebox.showerror("Error", "Please select a video first")
            return
        
        # Create speed adjustment dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Adjust Video Speed")
        dialog.geometry("300x150")
        
        speed_var = tk.DoubleVar(value=1.0)
        ctk.CTkLabel(dialog, text="Speed Multiplier:").pack(pady=5)
        speed_slider = ctk.CTkSlider(dialog, from_=0.5, to=2.0, variable=speed_var)
        speed_slider.pack(pady=5)
        
        def apply_speed():
            speed = speed_var.get()
            # Implement speed adjustment
            dialog.destroy()
        
        ctk.CTkButton(dialog, text="Apply", command=apply_speed).pack(pady=10)
    
    def extract_audio(self):
        try:
            input_path = self.audio_input_label.cget("text")
            output_path = self.audio_output_label.cget("text")
            format = self.audio_format_var.get().lower()
            volume = self.volume.get()
            
            if input_path == "No file selected" or output_path == "No file selected":
                messagebox.showerror("Error", "Please select input and output files")
                return
            
            extract_audio(input_path, output_path, format, volume)
            messagebox.showinfo("Success", "Audio extracted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def change_theme(self):
        ctk.set_appearance_mode(self.theme_var.get())
    
    def set_default_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_label.configure(text=directory)
            # Save to settings file
            self.save_last_output_dir(directory)

    def disable_video_buttons(self):
        # Disable all video action buttons
        for btn in [self.cut_button, self.rotate_button, self.speed_button, self.crop_button]:
            btn.configure(state="disabled")
    def enable_video_buttons(self):
        for btn in [self.cut_button, self.rotate_button, self.speed_button, self.crop_button]:
            btn.configure(state="normal")
    def disable_image_buttons(self):
        for btn in [self.convert_button]:
            btn.configure(state="disabled")
    def enable_image_buttons(self):
        for btn in [self.convert_button]:
            btn.configure(state="normal")

if __name__ == "__main__":
    try:
        root = TkinterDnD.Tk()
    except Exception as e:
        print(f"Error initializing TkinterDnD: {str(e)}")
        print("Falling back to regular Tk window")
        root = tk.Tk()
    
    app = MediaToolsGUI(root)
    root.mainloop() 