# frontend.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from dataclasses import dataclass
from typing import Optional
import os
from backend import VideoProcessor, ProcessingStatus

class VideoAmplifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Audio Amplifier")
        self.root.geometry("600x400")
        
        # Initialize backend
        self.processor = VideoProcessor()
        self.processor.register_status_callback(self._on_status_update)
        
        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.amplification_factor = tk.DoubleVar(value=2.0)
        
        # Create GUI elements
        self.create_widgets()
        
    def _on_status_update(self, status: ProcessingStatus):
        """Handle status updates from the backend"""
        self.root.after(0, self._update_gui_status, status)
    
    def _update_gui_status(self, status: ProcessingStatus):
        """Update GUI elements based on processing status"""
        if status.is_processing:
            self.process_button.state(['disabled'])
            self.progress_bar['value'] = status.progress
            self.status_label.config(text=status.status_message)
        else:
            self.process_button.state(['!disabled'])
            
            if status.progress == 100:
                messagebox.showinfo("Success", "Video processing completed successfully!")
                # Reset progress bar and status label
                self.progress_bar['value'] = 0
                self.status_label.config(text="Ready")
            elif status.error_message:
                messagebox.showerror("Error", f"Error processing video: {status.error_message}")
                # Reset progress bar and status label on error as well
                self.progress_bar['value'] = 0
                self.status_label.config(text="Ready")
        
    def create_widgets(self):
        # Input file section
        input_frame = ttk.LabelFrame(self.root, text="Input Video", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Entry(input_frame, textvariable=self.input_path, width=50).pack(side="left", padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_input).pack(side="left")
        
        # Output file section
        output_frame = ttk.LabelFrame(self.root, text="Output Location", padding=10)
        output_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).pack(side="left", padx=5)
        ttk.Button(output_frame, text="Browse", command=self.browse_output).pack(side="left")
        
        # Amplification factor section
        amp_frame = ttk.LabelFrame(self.root, text="Amplification Settings", padding=10)
        amp_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(amp_frame, text="Amplification Factor:").pack(side="left")
        ttk.Entry(amp_frame, textvariable=self.amplification_factor, width=10).pack(side="left", padx=5)
        
        # Progress section
        self.progress_frame = ttk.LabelFrame(self.root, text="Progress", padding=10)
        self.progress_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(fill="x", padx=5)
        
        self.status_label = ttk.Label(self.progress_frame, text="Ready")
        self.status_label.pack(fill="x", padx=5)
        
        # Process button
        self.process_button = ttk.Button(self.root, text="Process Video", command=self.process_video)
        self.process_button.pack(pady=20)
    
    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")]
        )
        if filename:
            self.input_path.set(filename)
            # Always generate a new output path
            directory = os.path.dirname(filename)
            basename = os.path.basename(filename)
            name, ext = os.path.splitext(basename)
            self.output_path.set(os.path.join(directory, f"{name}_amplified{ext}"))
    
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Amplified Video As",
            filetypes=[("Video files", "*.mp4"), ("All files", "*.*")],
            defaultextension=".mp4"
        )
        if filename:
            self.output_path.set(filename)
    
    def process_video(self):
        if not self.input_path.get() or not self.output_path.get():
            messagebox.showerror("Error", "Please select input and output files")
            return
        
        try:
            amp_factor = float(self.amplification_factor.get())
            if amp_factor <= 0:
                raise ValueError("Amplification factor must be positive")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid amplification factor: {str(e)}")
            return
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self._process_video_thread)
        thread.start()
    
    def _process_video_thread(self):
        self.processor.amplify_audio(
            self.input_path.get(),
            self.output_path.get(),
            self.amplification_factor.get()
        )

