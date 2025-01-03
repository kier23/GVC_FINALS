import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import glob


def get_system_fonts():
    font_paths = glob.glob("C:/Windows/Fonts/*.ttf")
    fonts = {}

    for font_path in font_paths:
        font_name = os.path.splitext(os.path.basename(font_path))[0]
        fonts[font_name] = font_path

    return fonts


def create_logo(initials, icon_path=None, canvas_size=(500, 500), bg_color=(255, 255, 255), text_color=(0, 0, 0), font_path=None):
    canvas = np.ones((canvas_size[1], canvas_size[0], 3), dtype="uint8") * np.array(bg_color, dtype="uint8")

    text_y = 0
    if font_path:
        try:
            pil_image = Image.fromarray(canvas)
            draw = ImageDraw.Draw(pil_image)
            font = ImageFont.truetype(font_path, size=100)

            text_bbox = draw.textbbox((0, 0), initials, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

            text_x = (canvas_size[0] - text_width) // 2
            text_y = (canvas_size[1] - text_height) // 2

            draw.text((text_x, text_y), initials, font=font, fill=text_color)
            canvas = np.array(pil_image)
        except Exception as e:
            print(f"Error loading font: {e}")
    else:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 4
        font_thickness = 5
        text_size = cv2.getTextSize(initials, font, font_scale, font_thickness)[0]
        text_x = (canvas_size[0] - text_size[0]) // 2
        text_y = (canvas_size[1] + text_size[1]) // 2
        cv2.putText(canvas, initials, (text_x, text_y), font, font_scale, text_color, font_thickness)

    if icon_path:
        try:
            icon = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)
            if icon is None:
                raise ValueError(f"Could not load the icon from {icon_path}")
            icon = cv2.resize(icon, (100, 100))
            icon_x = (canvas_size[0] - icon.shape[1]) // 2
            icon_y = max(0, text_y - 200)

            if icon.shape[2] == 4: 
                alpha = icon[:, :, 3] / 255.0
                for c in range(3):
                    canvas[icon_y:icon_y + icon.shape[0], icon_x:icon_x + icon.shape[1], c] = (
                    alpha * icon[:, :, c] + (1 - alpha) * canvas[icon_y:icon_y + icon.shape[0], icon_x:icon_x + icon.shape[1], c]
                    )
            else: 
                canvas[icon_y:icon_y + icon.shape[0], icon_x:icon_x + icon.shape[1]] = icon
        except Exception as e:
            print(f"Error loading icon: {e}")


    return canvas


def display_logo(initials, icon_path, font_path, bg_color, text_color):
    logo = create_logo(initials, icon_path, bg_color=bg_color, text_color=text_color, font_path=font_path)
    cv2.imshow("Generated Logo", logo)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def open_icon_file():
    icon_path = filedialog.askopenfilename(title="Select Icon File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    return icon_path


def capture_icon():
    import cv2
    from tkinter import messagebox

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open the camera.")
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture frame from the camera.")
            break
        frame = cv2.flip(frame, 1)
        cv2.imshow("Capture Icon (Press 's' to save, 'q' to quit)", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            icon_path = "captured_icon.png"
            cv2.imwrite(icon_path, frame)
            messagebox.showinfo("Success", f"Icon saved as {icon_path}")
            break
        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    return icon_path if key == ord("s") else None

def on_generate_logo():
    initials = initials_entry.get().strip()
    if not initials:
        messagebox.showerror("Input Error", "Please enter initials for the logo.")
        return

    if icon_option.get() == "Select Image":
        icon_path = icon_path_var.get()
        if icon_path == "None":
            icon_path = None
    elif icon_option.get() == "Capture Image":
        icon_path = capture_icon()

    font_name = font_combobox.get()
    font_path = fonts_dict.get(font_name, None)

    bg_color = color_mapping.get(bg_color_combobox.get(), (255, 255, 255))
    text_color = color_mapping.get(text_color_combobox.get(), (0, 0, 0))

    display_logo(initials, icon_path, font_path, bg_color, text_color)


color_mapping = {
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (0, 255, 255),
    "Cyan": (255, 255, 0),
    "Magenta": (255, 0, 255),
    "Gray": (128, 128, 128),
}

root = tk.Tk()
root.title("Logo Maker")

tk.Label(root, text="Enter initials for logo:").pack(pady=10)
initials_entry = tk.Entry(root, width=30)
initials_entry.pack(pady=10)

fonts_dict = get_system_fonts()
fonts_list = list(fonts_dict.keys())

tk.Label(root, text="Select Font:").pack(pady=10)
font_combobox = ttk.Combobox(root, values=fonts_list)
font_combobox.set("Arial")
font_combobox.pack(pady=5)

tk.Label(root, text="Select Icon Source:").pack(pady=10)
icon_option = tk.StringVar(value="Select Image")
select_image_radio = tk.Radiobutton(root, text="Select Image", variable=icon_option, value="Select Image")
select_image_radio.pack()
capture_image_radio = tk.Radiobutton(root, text="Capture Image", variable=icon_option, value="Capture Image")
capture_image_radio.pack()

icon_path_var = tk.StringVar(value="None")
icon_button = tk.Button(root, text="Choose Icon", command=lambda: icon_path_var.set(open_icon_file()))
icon_button.pack(pady=5)

tk.Label(root, text="Select Background Color:").pack(pady=10)
bg_color_combobox = ttk.Combobox(root, values=list(color_mapping.keys()))
bg_color_combobox.set("White")
bg_color_combobox.pack(pady=5)

tk.Label(root, text="Select Text Color:").pack(pady=10)
text_color_combobox = ttk.Combobox(root, values=list(color_mapping.keys()))
text_color_combobox.set("Black")
text_color_combobox.pack(pady=5)

generate_button = tk.Button(root, text="Generate Logo", command=on_generate_logo)
generate_button.pack(pady=20)

root.mainloop()
