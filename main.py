import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

# --- DESIGN & COLOR PALETTE --- #
ctk.set_appearance_mode("Dark")

BG_COLOR = "#18181b"      # Deep background for main workspace
SIDEBAR_COLOR = "#27272a"  # Lighter for the sidebar
ACTIVE_COLOR = "#3f3f46"   # Highlight color for selected buttons
ACCENT_COLOR = "#3b82f6"   # Blue highlight

# --- MAIN WINDOW ---
app = ctk.CTk()
app.title("Media Converter Utility")
app.geometry("850x600")
app.configure(fg_color=BG_COLOR)

# --- GLOBAL APP STATE ---
selected_image_path = None


# --- INTERACTIVITY LOGIC (SIDEBAR TOGGLES) --- #

def open_image_menu():
    Img_button.configure(fg_color=ACTIVE_COLOR)
    Vid_button.configure(fg_color=SIDEBAR_COLOR)
    video_sub_menu.pack_forget()
    image_sub_menu.pack(fill="x", pady=5)

def open_video_menu():
    Vid_button.configure(fg_color=ACTIVE_COLOR)
    Img_button.configure(fg_color=SIDEBAR_COLOR)
    image_sub_menu.pack_forget()
    video_sub_menu.pack(fill="x", pady=5)

def show_placeholder_workspace(tool_name, tool_description):
    """Clears workspace and shows placeholder text for tools not implemented yet."""
    for widget in main_frame.winfo_children():
        widget.destroy()

    title = ctk.CTkLabel(main_frame, text=tool_name, font=("Arial", 28, "bold"))
    title.pack(pady=(150, 10))

    desc = ctk.CTkLabel(main_frame, text=tool_description, font=("Arial", 16), text_color="gray50")
    desc.pack()


# --- WORKSPACE TOOL 1: BIT DEPTH CONVERTER --- #

def setup_bit_depth_workspace(parent_frame):
    """Dynamically builds the Bit Depth Converter interface in the workspace."""
    global selected_image_path
    selected_image_path = None  # Reset state when loading tool

    # Clear previous workspace widgets
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Title
    title = ctk.CTkLabel(parent_frame, text="Bit Depth Converter", font=("Arial", 24, "bold"))
    title.pack(pady=(40, 5))

    subtitle = ctk.CTkLabel(parent_frame, text="Detect and re-encode color & image precision modes.", font=("Arial", 13), text_color="gray60")
    subtitle.pack(pady=(0, 20))

    # --- Step 1: File Selection ---
    select_btn = ctk.CTkButton(
        parent_frame, 
        text="Choose Image", 
        height=38,
        fg_color=ACCENT_COLOR,
        font=("Arial", 14, "bold"),
        command=lambda: load_and_inspect_image(info_label, combo_box, convert_btn)
    )
    select_btn.pack(pady=10)

    # Info display box
    info_label = ctk.CTkLabel(parent_frame, text="No image loaded.", font=("Arial", 13), text_color="gray60")
    info_label.pack(pady=10)

    # --- Step 2: Target Depth Selection ---
    combo_label = ctk.CTkLabel(parent_frame, text="Target Bit Depth:", font=("Arial", 14, "bold"))
    combo_label.pack(pady=(20, 5))

    bit_options = [
        "1-Bit (Monochrome / B&W)",
        "8-Bit (Standard Grayscale)",
        "8-Bit (Standard RGB Color)",
        "16-Bit (Grayscale High-Depth)",
        "32-Bit (Float Precision)"
    ]
    
    combo_box = ctk.CTkComboBox(parent_frame, values=bit_options, state="disabled", width=260, height=35)
    combo_box.pack(pady=5)

    # --- Step 3: Convert Action ---
    convert_btn = ctk.CTkButton(
        parent_frame, 
        text="Convert & Save", 
        height=40,
        width=200,
        state="disabled", 
        fg_color="#22c55e", 
        hover_color="#15803d",
        font=("Arial", 14, "bold"),
        command=lambda: process_conversion(combo_box.get(), info_label)
    )
    convert_btn.pack(pady=30)


def load_and_inspect_image(info_label, combo_box, convert_btn):
    """Opens file browser, reads header, and enables dynamic controls."""
    global selected_image_path
    
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp")]
    )
    
    if not file_path:
        return

    selected_image_path = file_path
    
    try:
        with Image.open(file_path) as img:
            mode_map = {
                "1": "1-Bit (Monochrome)",
                "L": "8-Bit (Grayscale)",
                "P": "8-Bit (Indexed Color)",
                "RGB": "8-Bit/Channel (24-bit RGB)",
                "RGBA": "8-Bit/Channel (32-bit RGBA)",
                "I;16": "16-Bit (Unsigned Integer)",
                "I;16L": "16-Bit (Little-Endian)",
                "I": "32-Bit (Integer)",
                "F": "32-Bit (Float Precision)"
            }
            detected_depth = mode_map.get(img.mode, f"Unknown Mode ({img.mode})")
            filename = os.path.basename(file_path)
            
            info_label.configure(
                text=f"Loaded: {filename}\nCurrent Mode: {detected_depth}",
                text_color="#60a5fa"
            )
            combo_box.configure(state="normal")
            convert_btn.configure(state="normal")
            
    except Exception as e:
        info_label.configure(text=f"Error reading image: {e}", text_color="#ef4444")


def process_conversion(target_selection, info_label):
    """Converts pixel array and prompts user for custom save location and filename."""
    global selected_image_path
    if not selected_image_path:
        return

    # Extract original directory, name, and extension
    folder, full_name = os.path.split(selected_image_path)
    name, ext = os.path.splitext(full_name)

    # 1 & 2. Open Save File Dialog (Fixes custom location, custom naming, and overwrite warnings)
    save_path = filedialog.asksaveasfilename(
        title="Save Converted Image As...",
        initialdir=folder,
        initialfile=f"{name}_converted{ext}",
        filetypes=[("Image Files", f"*{ext}"), ("All Files", "*.*")],
        defaultextension=ext
    )

    if not save_path:
        return  # User closed/canceled the save popup

    target_mode_map = {
        "1-Bit (Monochrome / B&W)": "1",
        "8-Bit (Standard Grayscale)": "L",
        "8-Bit (Standard RGB Color)": "RGB",
        "16-Bit (Grayscale High-Depth)": "I;16",
        "32-Bit (Float Precision)": "F"
    }

    target_mode = target_mode_map.get(target_selection)

    try:
        with Image.open(selected_image_path) as img:
            # 3. Handle 1-Bit conversion with hard thresholding (no optical gray dithering)
            if target_mode == "1":
                grayscale = img.convert("L")
                converted_img = grayscale.point(lambda p: 255 if p > 128 else 0).convert("1")
            else:
                converted_img = img.convert(target_mode)
            
            converted_img.save(save_path)
            
            saved_filename = os.path.basename(save_path)
            info_label.configure(text=f"Success! Saved as:\n{saved_filename}", text_color="#4ade80")
            
    except Exception as e:
        info_label.configure(text=f"Conversion Error: {e}", text_color="#ef4444")

# --- UI LAYOUT: SIDEBAR --- #

sidebar = ctk.CTkFrame(app, width=280, corner_radius=0, fg_color=SIDEBAR_COLOR)
sidebar.pack(side="left", fill="y")

sidebar_label = ctk.CTkLabel(sidebar, text="Tools", font=("Arial", 22, "bold"))
sidebar_label.pack(padx=20, pady=25)

# Main Toggle Buttons (Side-by-Side)
toggle_container = ctk.CTkFrame(sidebar, fg_color="transparent")
toggle_container.pack(fill="x", padx=15, pady=5)

Img_button = ctk.CTkButton(
    toggle_container, text="Image", corner_radius=6, height=35,
    fg_color=ACTIVE_COLOR, hover_color=ACTIVE_COLOR, 
    font=("Arial", 14, "bold"), command=open_image_menu
)
Img_button.pack(side="left", fill="x", expand=True, padx=(0, 5))

Vid_button = ctk.CTkButton(
    toggle_container, text="Video", corner_radius=6, height=35,
    fg_color=SIDEBAR_COLOR, hover_color=ACTIVE_COLOR, 
    font=("Arial", 14, "bold"), command=open_video_menu
)
Vid_button.pack(side="left", fill="x", expand=True, padx=(5, 0))

# Sub-menu Container (Anti-jump box)
sub_menu_container = ctk.CTkFrame(sidebar, fg_color="transparent", height=150)
sub_menu_container.pack(fill="x", padx=15, pady=15)
sub_menu_container.pack_propagate(False) 

# --- IMAGE SUB-MENU ---
image_sub_menu = ctk.CTkFrame(sub_menu_container, fg_color="transparent")
image_sub_menu.pack(fill="x", pady=5)  # Default open menu

btn_bit_depth = ctk.CTkButton(
    image_sub_menu, text="> Bit Depth Converter", fg_color="transparent", 
    hover_color=ACTIVE_COLOR, anchor="w", text_color="gray70",
    command=lambda: setup_bit_depth_workspace(main_frame)  # <--- WIRED HERE!
)
btn_bit_depth.pack(fill="x", pady=2)

btn_img_format = ctk.CTkButton(
    image_sub_menu, text="> Format Converter", fg_color="transparent", 
    hover_color=ACTIVE_COLOR, anchor="w", text_color="gray70",
    command=lambda: show_placeholder_workspace("Format Converter", "Convert standard image formats (PNG, JPG, WebP).")
)
btn_img_format.pack(fill="x", pady=2)

# --- VIDEO SUB-MENU ---
video_sub_menu = ctk.CTkFrame(sub_menu_container, fg_color="transparent")

btn_frames = ctk.CTkButton(
    video_sub_menu, text="> Extract Frames", fg_color="transparent", 
    hover_color=ACTIVE_COLOR, anchor="w", text_color="gray70",
    command=lambda: show_placeholder_workspace("Frame Extractor", "Extract frame sequences from MP4/MOV videos.")
)
btn_frames.pack(fill="x", pady=2)

btn_gif = ctk.CTkButton(
    video_sub_menu, text="> Video to GIF", fg_color="transparent", 
    hover_color=ACTIVE_COLOR, anchor="w", text_color="gray70",
    command=lambda: show_placeholder_workspace("GIF Generator", "Convert video clips into optimized GIFs.")
)
btn_gif.pack(fill="x", pady=2)


# --- UI LAYOUT: MAIN WORKSPACE --- #

main_frame = ctk.CTkFrame(app, fg_color=BG_COLOR, corner_radius=0)
main_frame.pack(side="right", fill="both", expand=True)

# Initial Screen Setup
show_placeholder_workspace("Select a Tool", "Choose a tool from the sidebar to get started.")

# Run main application loop
app.mainloop()