import customtkinter as ctk

# Set modern dark theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Initialize app window
app = ctk.CTk()
app.title("Media Converter Utility")
app.geometry("500x400")

# Header Label
title_label = ctk.CTkLabel(app, text="File Utility Blueprint", font=("Arial", 20, "bold"))
title_label.pack(padx=20, pady=20)

# Run the app loop
app.mainloop()