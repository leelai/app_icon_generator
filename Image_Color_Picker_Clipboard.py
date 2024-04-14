
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def open_image():
    # Let user select an image file
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    
    # Load the selected image
    image = Image.open(filepath)

    # Resize image to fit the window if it's too large
    max_width = root.winfo_screenwidth() // 2  # Adjust this factor as needed
    max_height = root.winfo_screenheight() // 2  # Adjust this factor as needed

    if image.width > max_width or image.height > max_height:
        image = image.resize((max_width, max_height), Image.Resampling.LANCZOS)

    image_tk = ImageTk.PhotoImage(image)

    # Display the image on the label widget
    label_image.config(image=image_tk)
    label_image.image = image_tk  # keep a reference!
    label_image.pack_configure()

    # Update the click event with the new image
    label_image.bind('<Button-1>', lambda event, img=image: show_rgb(event, img))

def show_rgb(event, img):
    # Get the color of the pixel at the click position
    pixel = img.getpixel((event.x, event.y))
    if img.mode == 'RGBA':
        r, g, b, a = pixel
    else:
        r, g, b = pixel
        a = 255  # Assume fully opaque for non-RGBA images

    # Display the ARGB values in 0xAARRGGBB format
    argb_str = f"0x{a:02X}{r:02X}{g:02X}{b:02X}"
    label_rgb.config(text=argb_str)
    copy_to_clipboard(argb_str)

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Now it stays on the clipboard after the window is closed

# Create the main window
root = tk.Tk()
root.title("Image Color Picker")

# Label to display the image
label_image = tk.Label(root)
label_image.pack()

# Label to display the RGB values
label_rgb = tk.Label(root, text='ARGB: (None)')
label_rgb.pack()

# Button to open an image
button_open = tk.Button(root, text='Open Image', command=open_image)
button_open.pack()

# Start the GUI application
root.mainloop()
