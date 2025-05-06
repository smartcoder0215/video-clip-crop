import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from video_clipper import clip_video, crop_video_bottom
from image_converter import convert_image

class MediaToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Tools")
        self.root.geometry("600x500")
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)
        
        # Create tabs
        self.video_tab = ttk.Frame(self.notebook)
        self.image_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.video_tab, text="Video Tools")
        self.notebook.add(self.image_tab, text="Image Tools")
        
        self.setup_video_tab()
        self.setup_image_tab()
    
    def setup_video_tab(self):
        # Video clip section
        clip_frame = ttk.LabelFrame(self.video_tab, text="Cut Video", padding=10)
        clip_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(clip_frame, text="Select Input Video", command=self.select_video_input).pack(fill="x", pady=5)
        self.video_input_label = ttk.Label(clip_frame, text="No file selected")
        self.video_input_label.pack(fill="x")
        
        ttk.Button(clip_frame, text="Select Output Location", command=self.select_video_output).pack(fill="x", pady=5)
        self.video_output_label = ttk.Label(clip_frame, text="No file selected")
        self.video_output_label.pack(fill="x")
        
        time_frame = ttk.Frame(clip_frame)
        time_frame.pack(fill="x", pady=5)
        
        ttk.Label(time_frame, text="Start Time (seconds):").pack(side="left")
        self.start_time = ttk.Entry(time_frame, width=10)
        self.start_time.pack(side="left", padx=5)
        
        ttk.Label(time_frame, text="End Time (seconds):").pack(side="left", padx=5)
        self.end_time = ttk.Entry(time_frame, width=10)
        self.end_time.pack(side="left")
        
        ttk.Button(clip_frame, text="Cut Video", command=self.process_video_clip).pack(fill="x", pady=5)
        
        # Video crop section
        crop_frame = ttk.LabelFrame(self.video_tab, text="Crop Video Bottom", padding=10)
        crop_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(crop_frame, text="Select Input Video", command=self.select_crop_input).pack(fill="x", pady=5)
        self.crop_input_label = ttk.Label(crop_frame, text="No file selected")
        self.crop_input_label.pack(fill="x")
        
        ttk.Button(crop_frame, text="Select Output Location", command=self.select_crop_output).pack(fill="x", pady=5)
        self.crop_output_label = ttk.Label(crop_frame, text="No file selected")
        self.crop_output_label.pack(fill="x")
        
        height_frame = ttk.Frame(crop_frame)
        height_frame.pack(fill="x", pady=5)
        
        ttk.Label(height_frame, text="Height to keep (pixels):").pack(side="left")
        self.crop_height = ttk.Entry(height_frame, width=10)
        self.crop_height.pack(side="left", padx=5)
        
        ttk.Button(crop_frame, text="Crop Video", command=self.process_video_crop).pack(fill="x", pady=5)
    
    def setup_image_tab(self):
        # Image conversion section
        convert_frame = ttk.LabelFrame(self.image_tab, text="Convert Image", padding=10)
        convert_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(convert_frame, text="Select Input Image", command=self.select_image_input).pack(fill="x", pady=5)
        self.image_input_label = ttk.Label(convert_frame, text="No file selected")
        self.image_input_label.pack(fill="x")
        
        ttk.Button(convert_frame, text="Select Output Location", command=self.select_image_output).pack(fill="x", pady=5)
        self.image_output_label = ttk.Label(convert_frame, text="No file selected")
        self.image_output_label.pack(fill="x")
        
        format_frame = ttk.Frame(convert_frame)
        format_frame.pack(fill="x", pady=5)
        
        self.format_var = tk.StringVar(value="PNG")
        ttk.Radiobutton(format_frame, text="PNG", variable=self.format_var, value="PNG").pack(side="left", padx=5)
        ttk.Radiobutton(format_frame, text="JPEG", variable=self.format_var, value="JPEG").pack(side="left")
        
        ttk.Button(convert_frame, text="Convert Image", command=self.process_image).pack(fill="x", pady=5)
    
    def select_video_input(self):
        filename = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if filename:
            self.video_input_label.config(text=filename)
    
    def select_video_output(self):
        filename = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if filename:
            self.video_output_label.config(text=filename)
    
    def select_crop_input(self):
        filename = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if filename:
            self.crop_input_label.config(text=filename)
    
    def select_crop_output(self):
        filename = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if filename:
            self.crop_output_label.config(text=filename)
    
    def select_image_input(self):
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.webp *.png *.jpg *.jpeg")])
        if filename:
            self.image_input_label.config(text=filename)
    
    def select_image_output(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if filename:
            self.image_output_label.config(text=filename)
    
    def process_video_clip(self):
        try:
            input_path = self.video_input_label.cget("text")
            output_path = self.video_output_label.cget("text")
            start_time = float(self.start_time.get())
            end_time = float(self.end_time.get())
            
            if input_path == "No file selected" or output_path == "No file selected":
                messagebox.showerror("Error", "Please select input and output files")
                return
            
            clip_video(input_path, output_path, start_time, end_time)
            messagebox.showinfo("Success", "Video clip created successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def process_video_crop(self):
        try:
            input_path = self.crop_input_label.cget("text")
            output_path = self.crop_output_label.cget("text")
            crop_height = int(self.crop_height.get())
            
            if input_path == "No file selected" or output_path == "No file selected":
                messagebox.showerror("Error", "Please select input and output files")
                return
            
            crop_video_bottom(input_path, output_path, crop_height)
            messagebox.showinfo("Success", "Video cropped successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def process_image(self):
        try:
            input_path = self.image_input_label.cget("text")
            output_path = self.image_output_label.cget("text")
            output_format = self.format_var.get()
            
            if input_path == "No file selected" or output_path == "No file selected":
                messagebox.showerror("Error", "Please select input and output files")
                return
            
            convert_image(input_path, output_path, output_format)
            messagebox.showinfo("Success", "Image converted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaToolsGUI(root)
    root.mainloop() 