import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

ACCENT_COLOR = "#3b82f6"
selected_image_path = None

def setup_bit_depth_workspace(parent_frame):
    global selected_image_path
    selected_image_path = None

    for widget in parent_frame.winfo_children():
        widget.destroy()

    title = ctk.CTkLabel(parent_frame, text="Bit Depth Converter", font=("Arial", 24, "bold"))
    title.pack(pady=(40, 5))

    subtitle = ctk.CTkLabel(parent_frame, text="Detect and re-encode color & image precision modes.", font=("Arial", 13), text_color="gray60")
    subtitle.pack(pady=(0, 20))

    select_btn = ctk.CTkButton(
        parent_frame, text="Choose Image", height=38, fg_color=ACCENT_COLOR, font=("Arial", 14, "bold"),
        command=lambda: load_and_inspect_image(info_label, combo_box, convert_btn)
    )
    select_btn.pack(pady=10)

    info_label = ctk.CTkLabel(parent_frame, text="No image loaded.", font=("Arial", 13), text_color="gray60")
    info_label.pack(pady=10)

    combo_label = ctk.CTkLabel(parent_frame, text="Target Bit Depth:", font=("Arial", 14, "bold"))
    combo_label.pack(pady=(20, 5))

    bit_options = [
        "1-Bit (Monochrome / B&W)", "8-Bit (Standard Grayscale)", "8-Bit (Standard RGB Color)",
        "16-Bit (Grayscale High-Depth)", "32-Bit (Float Precision)"
    ]
    
    combo_box = ctk.CTkComboBox(parent_frame, values=bit_options, state="disabled", width=260, height=35)
    combo_box.pack(pady=5)

    convert_btn = ctk.CTkButton(
        parent_frame, text="Convert & Save", height=40, width=200, state="disabled", 
        fg_color="#22c55e", hover_color="#15803d", font=("Arial", 14, "bold"),
        command=lambda: process_conversion(combo_box.get(), info_label)
    )
    convert_btn.pack(pady=30)

def load_and_inspect_image(info_label, combo_box, convert_btn):
    global selected_image_path
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp")])
    if not file_path:
        return
    selected_image_path = file_path
    try:
        with Image.open(file_path) as img:
            mode_map = {
                "1": "1-Bit (Monochrome)", "L": "8-Bit (Grayscale)", "P": "8-Bit (Indexed Color)",
                "RGB": "8-Bit/Channel (24-bit RGB)", "RGBA": "8-Bit/Channel (32-bit RGBA)",
                "I;16": "16-Bit (Unsigned Integer)", "I;16L": "16-Bit (Little-Endian)",
                "I": "32-Bit (Integer)", "F": "32-Bit (Float Precision)"
            }
            detected_depth = mode_map.get(img.mode, f"Unknown Mode ({img.mode})")
            filename = os.path.basename(file_path)
            
            info_label.configure(text=f"Loaded: {filename}\nCurrent Mode: {detected_depth}", text_color="#60a5fa")
            combo_box.configure(state="normal")
            convert_btn.configure(state="normal")
    except Exception as e:
        info_label.configure(text=f"Error reading image: {e}", text_color="#ef4444")

def process_conversion(target_selection, info_label):
    global selected_image_path
    if not selected_image_path:
        return

    folder, full_name = os.path.split(selected_image_path)
    name, ext = os.path.splitext(full_name)

    save_path = filedialog.asksaveasfilename(
        title="Save Converted Image As...", initialdir=folder, initialfile=f"{name}_converted{ext}",
        filetypes=[("Image Files", f"*{ext}"), ("All Files", "*.*")], defaultextension=ext
    )
    if not save_path:
        return

    target_mode_map = {
        "1-Bit (Monochrome / B&W)": "1", "8-Bit (Standard Grayscale)": "L",
        "8-Bit (Standard RGB Color)": "RGB", "16-Bit (Grayscale High-Depth)": "I;16", "32-Bit (Float Precision)": "F"
    }
    target_mode = target_mode_map.get(target_selection)

    try:
        with Image.open(selected_image_path) as img:
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