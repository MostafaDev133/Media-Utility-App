import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import cv2
import os

ACCENT_COLOR = "#3b82f6"
selected_video_path = None

def video_to_gif_area(parent_frame):
    global selected_video_path
    selected_video_path = None

    for widget in parent_frame.winfo_children():
        widget.destroy()

    title = ctk.CTkLabel(parent_frame, text="Video to GIF Converter", font=("Arial", 24, "bold"))
    title.pack(pady=(25, 5))

    subtitle = ctk.CTkLabel(
        parent_frame, 
        text="Convert video clips into animated GIFs with size and speed controls.", 
        font=("Arial", 13), 
        text_color="gray60"
    )
    subtitle.pack(pady=(0, 15))

    # --- Step 1: File Selection ---
    select_btn = ctk.CTkButton(
        parent_frame, text="Choose Video File", height=38, fg_color=ACCENT_COLOR, font=("Arial", 14, "bold"),
        command=lambda: load_video_for_gif(info_label, fps_combo, scale_combo, convert_btn)
    )
    select_btn.pack(pady=10)

    info_label = ctk.CTkLabel(parent_frame, text="No video loaded.", font=("Arial", 13), text_color="gray60")
    info_label.pack(pady=5)

    # --- Step 2: Customization Settings ---
    settings_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    settings_frame.pack(pady=15)

    # Output Frame Rate (Lower FPS = Smaller File Size)
    fps_label = ctk.CTkLabel(settings_frame, text="Target Framerate:", font=("Arial", 13, "bold"))
    fps_label.grid(row=0, column=0, padx=10, pady=8, sticky="e")

    fps_options = ["10 FPS (Recommended)", "15 FPS (Smooth)", "24 FPS (Cinematic)", "5 FPS (Compact)"]
    fps_combo = ctk.CTkComboBox(settings_frame, values=fps_options, state="disabled", width=220, height=32)
    fps_combo.grid(row=0, column=1, padx=10, pady=8)

    # Resolution Scaling (Downscaling drastically reduces GIF MB size)
    scale_label = ctk.CTkLabel(settings_frame, text="Resolution Scale:", font=("Arial", 13, "bold"))
    scale_label.grid(row=1, column=0, padx=10, pady=8, sticky="e")

    scale_options = ["50% Width (Optimized)", "75% Width", "100% (Original Size)", "25% Width (Thumbnail)"]
    scale_combo = ctk.CTkComboBox(settings_frame, values=scale_options, state="disabled", width=220, height=32)
    scale_combo.grid(row=1, column=1, padx=10, pady=8)

    # --- Step 3: Convert Action ---
    convert_btn = ctk.CTkButton(
        parent_frame, text="Generate GIF", height=40, width=220, state="disabled", 
        fg_color="#22c55e", hover_color="#15803d", font=("Arial", 14, "bold"),
        command=lambda: process_gif_conversion(fps_combo.get(), scale_combo.get(), info_label)
    )
    convert_btn.pack(pady=20)


def load_video_for_gif(info_label, fps_combo, scale_combo, convert_btn):
    """Inspects video parameters (resolution, duration, original FPS)."""
    global selected_video_path
    
    file_path = filedialog.askopenfilename(
        title="Select Video for GIF",
        filetypes=[("Video Files", "*.mp4 *.mov *.avi *.mkv *.webm")]
    )
    
    if not file_path:
        return

    selected_video_path = file_path
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        info_label.configure(text="Error loading video file.", text_color="#ef4444")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / fps if fps > 0 else 0
    cap.release()

    filename = os.path.basename(file_path)
    info_label.configure(
        text=f"Loaded: {filename}\nRes: {width}x{height} | Duration: {duration_sec:.1f}s | FPS: {int(fps)}",
        text_color="#60a5fa"
    )

    fps_combo.configure(state="normal")
    scale_combo.configure(state="normal")
    convert_btn.configure(state="normal")


def process_gif_conversion(fps_selection, scale_selection, info_label):
    """Reads video frames, resizes them, and encodes into an animated GIF."""
    global selected_video_path
    if not selected_video_path:
        return

    # Parse target FPS
    if "10 FPS" in fps_selection:
        target_fps = 10
    elif "15 FPS" in fps_selection:
        target_fps = 15
    elif "24 FPS" in fps_selection:
        target_fps = 24
    else:
        target_fps = 5

    # Parse scale percentage
    if "50%" in scale_selection:
        scale_factor = 0.5
    elif "75%" in scale_selection:
        scale_factor = 0.75
    elif "25%" in scale_selection:
        scale_factor = 0.25
    else:
        scale_factor = 1.0

    folder, full_name = os.path.split(selected_video_path)
    name, _ = os.path.splitext(full_name)

    save_path = filedialog.asksaveasfilename(
        title="Save Animated GIF As...",
        initialdir=folder,
        initialfile=f"{name}_animated.gif",
        filetypes=[("GIF Image", "*.gif")],
        defaultextension=".gif"
    )
    if not save_path:
        return

    info_label.configure(text="Processing frames... Please wait.", text_color="#eab308")
    info_label.update()

    cap = cv2.VideoCapture(selected_video_path)
    if not cap.isOpened():
        info_label.configure(text="Failed to open video.", text_color="#ef4444")
        return

    orig_fps = cap.get(cv2.CAP_PROP_FPS)
    step = max(1, int(orig_fps / target_fps))

    frames = []
    current_frame = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if current_frame % step == 0:
            # Resize image if scaling applied
            if scale_factor != 1.0:
                h, w = frame.shape[:2]
                new_w = max(1, int(w * scale_factor))
                new_h = max(1, int(h * scale_factor))
                frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

            # Convert BGR (OpenCV) to RGB (Pillow)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame)
            
            # Palette optimization to keep file sizes lean
            pil_img = pil_img.convert("P", palette=Image.ADAPTIVE)
            frames.append(pil_img)

        current_frame += 1

    cap.release()

    if not frames:
        info_label.configure(text="No frames captured.", text_color="#ef4444")
        return

    # Save sequence as an animated GIF
    try:
        frame_duration = int(1000 / target_fps)  # Duration in milliseconds
        frames[0].save(
            save_path,
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=frame_duration,
            loop=0
        )
        saved_filename = os.path.basename(save_path)
        info_label.configure(
            text=f"Success! Created GIF:\n{saved_filename} ({len(frames)} frames)",
            text_color="#4ade80"
        )
    except Exception as e:
        info_label.configure(text=f"GIF Encoding Error: {e}", text_color="#ef4444")