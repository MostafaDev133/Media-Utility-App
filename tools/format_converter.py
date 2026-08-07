import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

ACCENT_COLOR = "#3b82f6"
selected_image_paths = []  # Changed to a list to hold multiple files

def setup_format_converter_workspace(parent_frame):
    global selected_image_paths
    selected_image_paths = []

    for widget in parent_frame.winfo_children():
        widget.destroy()

    title = ctk.CTkLabel(parent_frame, text="Format Converter", font=("Arial", 24, "bold"))
    title.pack(pady=(40, 5))

    subtitle = ctk.CTkLabel(parent_frame, text="Convert single images or entire batches.", font=("Arial", 13), text_color="gray60")
    subtitle.pack(pady=(0, 20))

    # --- Step 1: File Selection ---
    select_btn = ctk.CTkButton(
        parent_frame, text="Choose Image(s)", height=38, fg_color=ACCENT_COLOR, font=("Arial", 14, "bold"),
        command=lambda: load_images_for_format(info_label, combo_box, convert_btn)
    )
    select_btn.pack(pady=10)

    info_label = ctk.CTkLabel(parent_frame, text="No images loaded.", font=("Arial", 13), text_color="gray60")
    info_label.pack(pady=10)

    # --- Step 2: Target Format Selection ---
    combo_label = ctk.CTkLabel(parent_frame, text="Target Format:", font=("Arial", 14, "bold"))
    combo_label.pack(pady=(20, 5))

    format_options = [".PNG", ".JPG", ".WEBP", ".BMP", ".TIFF", ".ICO"]
    combo_box = ctk.CTkComboBox(parent_frame, values=format_options, state="disabled", width=260, height=35)
    combo_box.pack(pady=5)

    # --- Step 3: Convert Action ---
    convert_btn = ctk.CTkButton(
        parent_frame, text="Convert & Save", height=40, width=200, state="disabled", 
        fg_color="#22c55e", hover_color="#15803d", font=("Arial", 14, "bold"),
        command=lambda: process_batch_conversion(combo_box.get(), info_label)
    )
    convert_btn.pack(pady=30)


def load_images_for_format(info_label, combo_box, convert_btn):
    """Opens file browser allowing multiple file selections."""
    global selected_image_paths
    
    # Note askopenfilenames (PLURAL)
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp *.webp *.ico")]
    )
    
    if not file_paths:
        return

    selected_image_paths = list(file_paths)
    count = len(selected_image_paths)
    
    if count == 1:
        filename = os.path.basename(selected_image_paths[0])
        _, ext = os.path.splitext(filename)
        info_label.configure(
            text=f"Loaded: {filename}\nCurrent Format: {ext.upper()}",
            text_color="#60a5fa"
        )
    else:
        info_label.configure(
            text=f"Loaded: {count} images ready for batch conversion.",
            text_color="#60a5fa"
        )

    combo_box.configure(state="normal")
    convert_btn.configure(state="normal")


def process_batch_conversion(target_format, info_label):
    """Handles both single-file saving and multi-file batch export."""
    global selected_image_paths
    if not selected_image_paths:
        return

    target_ext = target_format.lower()
    count = len(selected_image_paths)

    # --- MODE A: SINGLE FILE CONVERSION ---
    if count == 1:
        source_path = selected_image_paths[0]
        folder, full_name = os.path.split(source_path)
        name, _ = os.path.splitext(full_name)

        save_path = filedialog.asksaveasfilename(
            title="Save Converted Image As...",
            initialdir=folder,
            initialfile=f"{name}_converted{target_ext}",
            filetypes=[(f"{target_format} Image", f"*{target_ext}"), ("All Files", "*.*")],
            defaultextension=target_ext
        )

        if not save_path:
            return

        convert_single_image(source_path, save_path, target_ext)
        saved_filename = os.path.basename(save_path)
        info_label.configure(text=f"Success! Saved as:\n{saved_filename}", text_color="#4ade80")

    # --- MODE B: BATCH CONVERSION ---
    else:
        # Ask user for a folder destination rather than a single filename
        output_folder = filedialog.askdirectory(title="Select Output Directory for Batch")
        if not output_folder:
            return

        success_count = 0
        for source_path in selected_image_paths:
            full_name = os.path.basename(source_path)
            name, _ = os.path.splitext(full_name)
            save_path = os.path.join(output_folder, f"{name}_converted{target_ext}")
            
            if convert_single_image(source_path, save_path, target_ext):
                success_count += 1

        info_label.configure(
            text=f"Batch Complete!\nSuccessfully converted {success_count}/{count} images.",
            text_color="#4ade80"
        )


def convert_single_image(source_path, save_path, target_ext):
    """Helper function to convert a single image and handle transparency safety."""
    try:
        with Image.open(source_path) as img:
            if target_ext in [".jpg", ".jpeg", ".bmp"] and img.mode in ("RGBA", "P", "LA"):
                img_to_save = img.convert("RGB")
            else:
                img_to_save = img
            
            img_to_save.save(save_path)
            return True
    except Exception as e:
        print(f"Error converting {source_path}: {e}")
        return False