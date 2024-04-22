import customtkinter as ctk

# Function to display an error
def display_error(window, for_what, posx, posy, anchor, time=None, start_animation=None, end_animation=None, animation_time=None):
    error_frame = ctk.CTkFrame(window, width=400, height=75, fg_color="#ff0000", bg_color="transparent", corner_radius=10, border_width=5, border_color="#ff0100")
    error_frame.place(relx=posx, rely=posy, anchor=f"{anchor}")
    error_label = ctk.CTkLabel(error_frame, width=350, height=25, fg_color="transparent", text=f"{for_what}")
    error_label.place(relx=posx, rely=posy, anchor=f"{anchor}")
    