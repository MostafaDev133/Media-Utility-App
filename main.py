import customtkinter as ctk
# --- CUSTOM MODULES --- #
from tools.bit_depth import setup_bit_depth_workspace
from tools.format_converter import setup_format_converter_workspace
from tools.frame_extractor import setup_frame_extractor_workspace
# --- DESIGN & COLOR PALETTE --- #
ctk.set_appearance_mode("Dark")

BG_COLOR = "#18181b"
SIDEBAR_COLOR = "#27272a"
ACTIVE_COLOR = "#3f3f46"

# --- MAIN WINDOW --- #
app = ctk.CTk()
app.title("Media Converter Utility")
app.geometry("850x600")
app.configure(fg_color=BG_COLOR)

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
    for widget in main_frame.winfo_children():
        widget.destroy()
    title = ctk.CTkLabel(main_frame, text=tool_name, font=("Arial", 28, "bold"))
    title.pack(pady=(150, 10))
    desc = ctk.CTkLabel(main_frame, text=tool_description, font=("Arial", 16), text_color="gray50")
    desc.pack()

# --- UI LAYOUT: SIDEBAR --- #
sidebar = ctk.CTkFrame(app, width=280, corner_radius=0, fg_color=SIDEBAR_COLOR)
sidebar.pack(side="left", fill="y")

sidebar_label = ctk.CTkLabel(sidebar, text="Tools", font=("Arial", 22, "bold"))
sidebar_label.pack(padx=20, pady=25)

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

sub_menu_container = ctk.CTkFrame(sidebar, fg_color="transparent", height=150)
sub_menu_container.pack(fill="x", padx=15, pady=15)
sub_menu_container.pack_propagate(False) 

# --- IMAGE SUB-MENU --- #
image_sub_menu = ctk.CTkFrame(sub_menu_container, fg_color="transparent")
image_sub_menu.pack(fill="x", pady=5)

btn_bit_depth = ctk.CTkButton(
    image_sub_menu, text="> Bit Depth Converter", fg_color="transparent", 
    hover_color=ACTIVE_COLOR, anchor="w", text_color="gray70",
    command=lambda: setup_bit_depth_workspace(main_frame)  # USING MODULE
)
btn_bit_depth.pack(fill="x", pady=2)

btn_img_format = ctk.CTkButton(
    image_sub_menu, text="> Format Converter", fg_color="transparent", 
    hover_color=ACTIVE_COLOR, anchor="w", text_color="gray70",
    command=lambda: setup_format_converter_workspace(main_frame)  # USING MODULE
)
btn_img_format.pack(fill="x", pady=2)

# --- VIDEO SUB-MENU --- #
video_sub_menu = ctk.CTkFrame(sub_menu_container, fg_color="transparent")

btn_frames = ctk.CTkButton(
    video_sub_menu, text="> Extract Frames", fg_color="transparent", 
    hover_color=ACTIVE_COLOR, anchor="w", text_color="gray70",
    command=lambda: setup_frame_extractor_workspace(main_frame)
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

show_placeholder_workspace("Select a Tool", "Choose a tool from the sidebar to get started.")

app.mainloop()