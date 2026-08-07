import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

ACCENT_COLOR = "#3b82f6"
selected_image_paths = []  # Holds one or multiple image paths

def setup_bit_depth_workspace(parent_frame):
    global selected_image_paths
    selected_image_paths = []

    for widget in parent_frame.winfo_children():
        widget.destroy()

    title = ctk.CTkLabel(parent_frame, text="Bit Depth Converter", font=("Arial", 24, "bold"))
    title.pack(pady=(40, 5))

    subtitle = ctk.CTkLabel(parent_frame, text="Convert color depth for single images or batches.", font=("Arial", 13), text_color="gray60")
    subtitle.pack(pady=(0, 20))

    # --- Step 1: File Selection ---
    select_btn = ctk.CTkButton(
        parent_frame, text="Choose Image(s)", height=38, fg_color=ACCENT_COLOR, font=("Arial", 14, "bold"),
        command=lambda: load_images_for_bit_depth(info_label, combo_box, convert_btn)
    )
    select_btn.pack(pady=10)

    info_label = ctk.CTkLabel(parent_frame, text="No images loaded.", font=("Arial", 13), text_color="gray60")
    info_label.pack(pady=10)

    # --- Step 2: Target Bit Depth Selection ---
    combo_label = ctk.CTkLabel(parent_frame, text="Target Bit Depth:", font=("Arial", 14, "bold"))
    combo_label.pack(pady=(20, 5))

    bit_options = [
        "1-Bit (Monochrome / B&W)", "8-Bit (Standard Grayscale)", "8-Bit (Standard RGB Color)",
        "16-Bit (Grayscale High-Depth)", "32-Bit (Float Precision)"
    ]
    
    combo_box = ctk.CTkComboBox(parent_frame, values=bit_options, state="disabled", width=260, height=35)
    combo_box.pack(pady=5)

    # --- Step 3: Convert Action ---
    convert_btn = ctk.CTkButton(
        parent_frame, text="Convert & Save", height=40, width=200, state="disabled", 
        fg_color="#22c55e", hover_color="#15803d", font=("Arial", 14, "bold"),
        command=lambda: process_batch_bit_depth(combo_box.get(), info_label)
    )
    convert_btn.pack(pady=30)


def load_images_for_bit_depth(info_label, combo_box, convert_btn):
    """Opens file browser allowing single or multiple image selection."""
    global selected_image_paths
    
    file_paths = filedialog.askopenfilenames(
        title="Select Image(s)", 
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp")]
    )
    
    if not file_paths:
        return

    selected_image_paths = list(file_paths)
    count = len(selected_image_paths)

    # Single Image: Inspect color mode
    if count == 1:
        source_path = selected_image_paths[0]
        try:
            with Image.open(source_path) as img:
                mode_map = {
                    "1": "1-Bit (Monochrome)", "L": "8-Bit (Grayscale)", "P": "8-Bit (Indexed Color)",
                    "RGB": "8-Bit/Channel (24-bit RGB)", "RGBA": "8-Bit/Channel (32-bit RGBA)",
                    "I;16": "16-Bit (Unsigned Integer)", "I;16L": "16-Bit (Little-Endian)",
                    "I": "32-Bit (Integer)", "F": "32-Bit (Float Precision)"
                }
                detected_depth = mode_map.get(img.mode, f"Unknown Mode ({img.mode})")
                filename = os.path.basename(source_path)
                
                info_label.configure(
                    text=f"Loaded: {filename}\nCurrent Mode: {detected_depth}", 
                    text_color="#60a5fa"
                )
        except Exception as e:
            info_label.configure(text=f"Error reading image: {e}", text_color="#ef4444")
            return
    # Batch Selection: Display total count
    else:
        info_label.configure(
            text=f"Loaded: {count} images ready for batch conversion.",
            text_color="#60a5fa"
        )

    combo_box.configure(state="normal")
    convert_btn.configure(state="normal")


def process_batch_bit_depth(target_selection, info_label):
    """Handles single-file saving or batch export to a folder."""
    global selected_image_paths
    if not selected_image_paths:
        return

    target_mode_map = {
        "1-Bit (Monochrome / B&W)": "1",
        "8-Bit (Standard Grayscale)": "L",
        "8-Bit (Standard RGB Color)": "RGB",
        "16-Bit (Grayscale High-Depth)": "I;16",
        "32-Bit (Float Precision)": "F"
    }
    target_mode = target_mode_map.get(target_selection)
    count = len(selected_image_paths)

    # --- MODE A: SINGLE FILE ---
    if count == 1:
        source_path = selected_image_paths[0]
        folder, full_name = os.path.split(source_path)
        name, ext = os.path.splitext(full_name)

        save_path = filedialog.asksaveasfilename(
            title="Save Converted Image As...",
            initialdir=folder,
            initialfile=f"{name}_converted{ext}",
            filetypes=[("Image Files", f"*{ext}"), ("All Files", "*.*")],
            defaultextension=ext
        )
        if not save_path:
            return

        if convert_single_bit_depth(source_path, save_path, target_mode):
            saved_filename = os.path.basename(save_path)
            info_label.configure(text=f"Success! Saved as:\n{saved_filename}", text_color="#4ade80")
        else:
            info_label.configure(text="Conversion failed.", text_color="#ef4444")

    # --- MODE B: BATCH CONVERSION ---
    else:
        output_folder = filedialog.askdirectory(title="Select Output Directory for Batch")
        if not output_folder:
            return

        success_count = 0
        for source_path in selected_image_paths:
            full_name = os.path.basename(source_path)
            name, ext = os.path.splitext(full_name)
            save_path = os.path.join(output_folder, f"{name}_converted{ext}")

            if convert_single_bit_depth(source_path, save_path, target_mode):
                success_count += 1

        info_label.configure(
            text=f"Batch Complete!\nSuccessfully converted {success_count}/{count} images.",
            text_color="#4ade80"
        )


def convert_single_bit_depth(source_path, save_path, target_mode):
    """Helper function to perform bit depth conversion on a single image."""
    try:
        with Image.open(source_path) as img:
            if target_mode == "1":
                grayscale = img.convert("L")
                converted_img = grayscale.point(lambda p: 255 if p > 128 else 0).convert("1")
            else:
                converted_img = img.convert(target_mode)

            converted_img.save(save_path)
            return True
    except Exception as e:
        print(f"Error converting {source_path}: {e}")
        return False