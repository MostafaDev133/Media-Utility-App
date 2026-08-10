import customtkinter as ctk
from tkinter import filedialog
import cv2
import os

ACCENT_COLOR = "#3b82f6"
selected_video_path = None

def frame_extractor_area(parent_frame):
    global selected_video_path
    selected_video_path = None

    for widget in parent_frame.winfo_children():
        widget.destroy()

    title = ctk.CTkLabel(parent_frame, text="Frame Extractor", font=("Arial", 24, "bold"))
    title.pack(pady=(30, 5))

    subtitle = ctk.CTkLabel(parent_frame, text="Extract image sequences from MP4, MOV, or AVI files.", font=("Arial", 13), text_color="gray60")
    subtitle.pack(pady=(0, 15))

    # --- Step 1: File Selection ---
    select_btn = ctk.CTkButton(
        parent_frame, text="Choose Video File", height=38, fg_color=ACCENT_COLOR, font=("Arial", 14, "bold"),
        command=lambda: load_video_file(info_label, rate_combo, format_combo, extract_btn)
    )
    select_btn.pack(pady=10)

    info_label = ctk.CTkLabel(parent_frame, text="No video loaded.", font=("Arial", 13), text_color="gray60")
    info_label.pack(pady=5)

    # --- Step 2: Extraction Settings Container ---
    settings_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    settings_frame.pack(pady=15)

    # Rate Selection
    rate_label = ctk.CTkLabel(settings_frame, text="Extraction Rate:", font=("Arial", 13, "bold"))
    rate_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

    rate_options = ["Every Frame (All)", "1 Frame per Second", "2 Frames per Second", "Every 10th Frame", "Every 30th Frame"]
    rate_combo = ctk.CTkComboBox(settings_frame, values=rate_options, state="disabled", width=200, height=32)
    rate_combo.grid(row=0, column=1, padx=10, pady=5)

    # Output Image Format Selection
    format_label = ctk.CTkLabel(settings_frame, text="Frame Format:", font=("Arial", 13, "bold"))
    format_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    format_options = [".PNG", ".JPG"]
    format_combo = ctk.CTkComboBox(settings_frame, values=format_options, state="disabled", width=200, height=32)
    format_combo.grid(row=1, column=1, padx=10, pady=5)

    # --- Step 3: Extract Action ---
    extract_btn = ctk.CTkButton(
        parent_frame, text="Extract & Save Frames", height=40, width=220, state="disabled", 
        fg_color="#22c55e", hover_color="#15803d", font=("Arial", 14, "bold"),
        command=lambda: process_frame_extraction(rate_combo.get(), format_combo.get(), info_label)
    )
    extract_btn.pack(pady=20)


def load_video_file(info_label, rate_combo, format_combo, extract_btn):
    """Inspects video metadata (FPS, Total Frames, Duration)."""
    global selected_video_path
    
    file_path = filedialog.askopenfilename(
        title="Select Video",
        filetypes=[("Video Files", "*.mp4 *.mov *.avi *.mkv *.webm")]
    )
    
    if not file_path:
        return

    selected_video_path = file_path
    
    # Read Video Metadata
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        info_label.configure(text="Error loading video file.", text_color="#ef4444")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / fps if fps > 0 else 0
    cap.release()

    filename = os.path.basename(file_path)
    info_label.configure(
        text=f"Loaded: {filename}\nDuration: {duration_sec:.1f}s | FPS: {int(fps)} | Frames: {total_frames}",
        text_color="#60a5fa"
    )

    rate_combo.configure(state="normal")
    format_combo.configure(state="normal")
    extract_btn.configure(state="normal")


def process_frame_extraction(rate_selection, format_selection, info_label):
    """Reads video frames and exports selected intervals to a folder."""
    global selected_video_path
    if not selected_video_path:
        return

    output_folder = filedialog.askdirectory(title="Select Output Folder for Frames")
    if not output_folder:
        return

    cap = cv2.VideoCapture(selected_video_path)
    if not cap.isOpened():
        info_label.configure(text="Failed to open video stream.", text_color="#ef4444")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    target_ext = format_selection.lower()

    # Determine frame step interval
    if rate_selection == "1 Frame per Second":
        step = max(1, int(fps))
    elif rate_selection == "2 Frames per Second":
        step = max(1, int(fps / 2))
    elif rate_selection == "Every 10th Frame":
        step = 10
    elif rate_selection == "Every 30th Frame":
        step = 30
    else:  # "Every Frame (All)"
        step = 1

    current_frame = 0
    saved_count = 0
    base_name = os.path.splitext(os.path.basename(selected_video_path))[0]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if current_frame % step == 0:
            saved_count += 1
            frame_filename = f"{base_name}_frame_{saved_count:04d}{target_ext}"
            save_path = os.path.join(output_folder, frame_filename)
            cv2.imwrite(save_path, frame)

        current_frame += 1

    cap.release()
    info_label.configure(
        text=f"Extraction Complete!\nSaved {saved_count} frames to output directory.",
        text_color="#4ade80"
    )