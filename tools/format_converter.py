import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

ACCENT_COLOR = "#3b82f6"
selected_image_path = None

def setup_format_converter_workspace(parent_frame):
    global selected_image_path
    selected_image_path = None

    for widget in parent_frame.winfo_children():
        widget.destroy()

    title = ctk.CTkLabel(parent_frame, text="Format Converter", font=("Arial", 24, "bold"))
    title.pack(pady=(40, 5))

    subtitle = ctk.CTkLabel(parent_frame, text="Convert images between standard formats.", font=("Arial", 13), text_color="gray60")
    subtitle.pack(pady=(0, 20))

    select_btn = ctk.CTkButton(
        parent_frame, text="Choose Image", height=38, fg_color=ACCENT_COLOR, font=("Arial", 14, "bold"),
        command=lambda: load_image_for_format(info_label, combo_box, convert_btn)
    )
    select_btn.pack(pady=10)

    info_label = ctk.CTkLabel(parent_frame, text="No image loaded.", font=("Arial", 13), text_color="gray60")
    info_label.pack(pady=10)

    combo_label = ctk.CTkLabel(parent_frame, text="Target Format:", font=("Arial", 14, "bold"))
    combo_label.pack(pady=(20, 5))

    format_options = [".PNG", ".JPG", ".WEBP", ".BMP", ".TIFF", ".ICO"]
    combo_box = ctk.CTkComboBox(parent_frame, values=format_options, state="disabled", width=260, height=35)
    combo_box.pack(pady=5)

    convert_btn = ctk.CTkButton(
        parent_frame, text="Convert & Save", height=40, width=200, state="disabled", 
        fg_color="#22c55e", hover_color="#15803d", font=("Arial", 14, "bold"),
        command=lambda: process_format_conversion(combo_box.get(), info_label)
    )
    convert_btn.pack(pady=30)

def load_image_for_format(info_label, combo_box, convert_btn):
    global selected_image_path
    file_path = filedialog.askopenfilename(
        title="Select Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp *.webp *.ico")]
    )
    if not file_path:
        return
    selected_image_path = file_path
    filename = os.path.basename(file_path)
    _, ext = os.path.splitext(filename)
            
    info_label.configure(text=f"Loaded: {filename}\nCurrent Format: {ext.upper()}", text_color="#60a5fa")
    combo_box.configure(state="normal")
    convert_btn.configure(state="normal")

def process_format_conversion(target_format, info_label):
    global selected_image_path
    if not selected_image_path:
        return

    folder, full_name = os.path.split(selected_image_path)
    name, _ = os.path.splitext(full_name)
    target_ext = target_format.lower()

    save_path = filedialog.asksaveasfilename(
        title="Save Converted Image As...", initialdir=folder, initialfile=f"{name}_converted{target_ext}",
        filetypes=[(f"{target_format} Image", f"*{target_ext}"), ("All Files", "*.*")], defaultextension=target_ext
    )
    if not save_path:
        return

    try:
        with Image.open(selected_image_path) as img:
            if target_ext in [".jpg", ".jpeg", ".bmp"] and img.mode in ("RGBA", "P", "LA"):
                img_to_save = img.convert("RGB")
            else:
                img_to_save = img
            
            img_to_save.save(save_path)
            saved_filename = os.path.basename(save_path)
            info_label.configure(text=f"Success! Saved as:\n{saved_filename}", text_color="#4ade80")
    except Exception as e:
        info_label.configure(text=f"Conversion Error: {e}", text_color="#ef4444")