import customtkinter as ctk
from tkinter import filedialog
import os
import cv2
from PIL import Image

def frames_to_video_area(main_frame):
    # Clear the workspace
    for widget in main_frame.winfo_children(): 
        widget.destroy()

    # --- STATE VARIABLES ---
    selected_files = []

    # --- LOGIC FUNCTIONS ---
    def select_frames():
        nonlocal selected_files
        files = filedialog.askopenfilenames(
            title="Select Image Frames",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if files:
            # Sort files alphanumerically so they animate in the correct order
            selected_files = sorted(list(files))
            lbl_status.configure(
                text=f"{len(selected_files)} frames selected.", 
                text_color="white"
            )

    def generate_output():
        if not selected_files:
            lbl_status.configure(text="Error: Please select frames first!", text_color="#ff6b6b")
            return
        
        # Get FPS and Format from UI
        try:
            fps = int(fps_entry.get())
        except ValueError:
            lbl_status.configure(text="Error: FPS must be a number!", text_color="#ff6b6b")
            return

        output_format = format_var.get()
        
        # Ask user where to save
        extensions = [(f"{output_format} File", f"*.{output_format.lower()}")]
        save_path = filedialog.asksaveasfilename(
            title="Save Output As",
            defaultextension=f".{output_format.lower()}",
            filetypes=extensions
        )
        
        if not save_path:
            return

        # Update UI to show processing state
        lbl_status.configure(text="Processing... Please wait.", text_color="#ffd93d")
        main_frame.winfo_toplevel().update()

        try:
            if output_format == "GIF":
                # --- PILLOW: GENERATE GIF ---
                frames = [Image.open(f).convert("RGBA") for f in selected_files]
                duration_ms = int(1000 / fps) # Convert FPS to milliseconds per frame
                frames[0].save(
                    save_path, format="GIF", append_images=frames[1:],
                    save_all=True, duration=duration_ms, loop=0
                )
            else:
                # --- OPENCV: GENERATE VIDEO (MP4/AVI) ---
                first_frame = cv2.imread(selected_files[0])
                height, width, _ = first_frame.shape
                
                # Set up the video writer based on format
                if output_format == "MP4":
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                else: # AVI
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    
                video = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
                
                for f in selected_files:
                    img = cv2.imread(f)
                    # Safety check: resize image if it doesn't match the first frame's size
                    if img.shape[0] != height or img.shape[1] != width:
                        img = cv2.resize(img, (width, height))
                    video.write(img)
                    
                video.release()
                
            # Success Message
            filename = os.path.basename(save_path)
            lbl_status.configure(text=f"Success! Saved: {filename}", text_color="#4ade80")
            
        except Exception as e:
            lbl_status.configure(text=f"Error: {str(e)}", text_color="#ff6b6b")

    # --- UI LAYOUT ---
    title = ctk.CTkLabel(main_frame, text="Frames to Video / GIF", font=("Arial", 28, "bold"))
    title.pack(pady=(50, 10))

    desc = ctk.CTkLabel(main_frame, text="Compile an image sequence into an animation.", font=("Arial", 16), text_color="gray50")
    desc.pack(pady=(0, 30))

    # Button to select files
    btn_select = ctk.CTkButton(main_frame, text="Select Frames", font=("Arial", 14, "bold"), command=select_frames, height=40)
    btn_select.pack(pady=10)

    # Configuration Container
    config_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    config_frame.pack(pady=20)

    # FPS Setting
    ctk.CTkLabel(config_frame, text="FPS:", font=("Arial", 14)).pack(side="left", padx=5)
    fps_entry = ctk.CTkEntry(config_frame, width=60, justify="center")
    fps_entry.insert(0, "24") # Default FPS
    fps_entry.pack(side="left", padx=(0, 20))

    # Format Setting
    ctk.CTkLabel(config_frame, text="Format:", font=("Arial", 14)).pack(side="left", padx=5)
    format_var = ctk.StringVar(value="MP4")
    format_menu = ctk.CTkOptionMenu(config_frame, variable=format_var, values=["MP4", "AVI", "GIF"], width=100)
    format_menu.pack(side="left")

    # Generate Button
    btn_generate = ctk.CTkButton(main_frame, text="Generate Output", fg_color="#4338ca", hover_color="#3730a3", font=("Arial", 14, "bold"), command=generate_output, height=40)
    btn_generate.pack(pady=20)

    # Status Label
    lbl_status = ctk.CTkLabel(main_frame, text="No frames selected.", font=("Arial", 14), text_color="gray50")
    lbl_status.pack(pady=10)