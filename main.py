import customtkinter as ctk

# --- DESIGN & COLOR PALETTE ---
ctk.set_appearance_mode("Dark")

BG_COLOR = "#18181b"          # Deep background for main workspace
SIDEBAR_COLOR = "#27272a"     # Slightly lighter for the sidebar
ACTIVE_COLOR = "#3f3f46"      # Highlight color for selected buttons
ACCENT_COLOR = "#3b82f6"      # Modern blue for active tools

# --- MAIN WINDOW ---
app = ctk.CTk()
app.title("Media Converter Utility")
app.geometry("850x600")
app.configure(fg_color=BG_COLOR)

# --- INTERACTIVITY LOGIC (FUNCTIONS) ---

def open_image_menu():
    # 1. Highlight the Image button, un-highlight the Video button
    Img_button.configure(fg_color=ACTIVE_COLOR)
    Vid_button.configure(fg_color=SIDEBAR_COLOR)
    
    # 2. Hide the video options, reveal the image options
    video_sub_menu.pack_forget()
    image_sub_menu.pack(fill="x", pady=5)

def open_video_menu():
    # 1. Highlight the Video button, un-highlight the Image button
    Vid_button.configure(fg_color=ACTIVE_COLOR)
    Img_button.configure(fg_color=SIDEBAR_COLOR)
    
    # 2. Hide the image options, reveal the video options
    image_sub_menu.pack_forget()
    video_sub_menu.pack(fill="x", pady=5)

def update_workspace(tool_name, tool_description):
    # This updates the big text on the right side when a sub-option is clicked
    workspace_title.configure(text=tool_name)
    workspace_desc.configure(text=tool_description)

# --- UI LAYOUT: SIDEBAR ---
sidebar = ctk.CTkFrame(app, width=250, corner_radius=0, fg_color=SIDEBAR_COLOR)
sidebar.pack(side="left", fill="y")

sidebar_label = ctk.CTkLabel(sidebar, text="Tools", font=("Arial", 22, "bold"))
sidebar_label.pack(padx=20, pady=25)

# === IMAGE SECTION ===
# Main Image Button
Img_button = ctk.CTkButton(sidebar, text="Image Processing", corner_radius=0, height=40,
                           fg_color=SIDEBAR_COLOR, hover_color=ACTIVE_COLOR, 
                           font=("Arial", 14, "bold"), anchor="w",
                           command=open_image_menu) # Connects to the function above
Img_button.pack(fill="x")

# Hidden Image Sub-Menu
image_sub_menu = ctk.CTkFrame(sidebar, fg_color="transparent")

btn_8bit = ctk.CTkButton(image_sub_menu, text="> 16-bit to 8-bit Depth", fg_color="transparent", 
                         hover_color=ACTIVE_COLOR, anchor="w", text_color="gray70",
                         command=lambda: update_workspace("Depth Converter", "Batch convert 16-bit images to 8-bit for Unity imports."))
btn_8bit.pack(fill="x", padx=20, pady=2)

btn_img_format = ctk.CTkButton(image_sub_menu, text="> Format Converter", fg_color="transparent", 
                               hover_color=ACTIVE_COLOR, anchor="w", text_color="gray70",
                               command=lambda: update_workspace("Format Converter", "Convert standard image types (JPG, PNG, WebP)."))
btn_img_format.pack(fill="x", padx=20, pady=2)


# === VIDEO SECTION ===
# Main Video Button
Vid_button = ctk.CTkButton(sidebar, text="Video Processing", corner_radius=0, height=40,
                           fg_color=SIDEBAR_COLOR, hover_color=ACTIVE_COLOR, 
                           font=("Arial", 14, "bold"), anchor="w",
                           command=open_video_menu) # Connects to the function above
Vid_button.pack(fill="x")

# Hidden Video Sub-Menu
video_sub_menu = ctk.CTkFrame(sidebar, fg_color="transparent")

btn_frames = ctk.CTkButton(video_sub_menu, text="> Extract Frames", fg_color="transparent", 
                           hover_color=ACTIVE_COLOR, anchor="w", text_color="gray70",
                           command=lambda: update_workspace("Frame Extractor", "Extract MP4/MOV into frame sequences for Adobe Animate referencing."))
btn_frames.pack(fill="x", padx=20, pady=2)

btn_gif = ctk.CTkButton(video_sub_menu, text="> Video to GIF", fg_color="transparent", 
                        hover_color=ACTIVE_COLOR, anchor="w", text_color="gray70",
                        command=lambda: update_workspace("GIF Generator", "Convert short video clips into optimized GIFs."))
btn_gif.pack(fill="x", padx=20, pady=2)


# --- UI LAYOUT: MAIN WORKSPACE ---
main_frame = ctk.CTkFrame(app, fg_color=BG_COLOR, corner_radius=0)
main_frame.pack(side="right", fill="both", expand=True)

# These labels will dynamically change based on what button you click!
workspace_title = ctk.CTkLabel(main_frame, text="Select a tool from the sidebar", font=("Arial", 28, "bold"))
workspace_title.pack(pady=(150, 10))

workspace_desc = ctk.CTkLabel(main_frame, text="Your workspace will load here.", font=("Arial", 16), text_color="gray50")
workspace_desc.pack()

# Run the app loop
app.mainloop()