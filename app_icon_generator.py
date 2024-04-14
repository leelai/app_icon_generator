from tkinter import Tk, filedialog, Button
from PIL import Image
import os
import cv2
import numpy as np
from cv2 import dnn_superres

def enhance_image_with_superres(input_image):
    sr = dnn_superres.DnnSuperResImpl_create()
    model_path = "ESPCN_x4.pb"
    sr.readModel(model_path)
    sr.setModel("espcn", 4)

    if input_image.shape[2] == 4:
        input_image = cv2.cvtColor(input_image, cv2.COLOR_BGRA2BGR)
    
    enhanced_image = sr.upsample(input_image)
    return enhanced_image

def create_app_icons(input_image_path, output_folder):
    ios_sizes = [1024, 76, 152, 167, 83, 40, 80, 29, 58, 20, 40, 60, 120, 180, 87, 512]
    android_sizes = {
        'mipmap-mdpi': 48,
        'mipmap-hdpi': 72,
        'mipmap-xhdpi': 96,
        'mipmap-xxhdpi': 144,
        'mipmap-xxxhdpi': 192
    }
    
    image = Image.open(input_image_path)
    image = image.convert("RGBA")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    max_size = max(ios_sizes + list(android_sizes.values()))
    if image.width < max_size or image.height < max_size:
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGRA)
        enhanced_cv_image = enhance_image_with_superres(open_cv_image)
        image = Image.fromarray(cv2.cvtColor(enhanced_cv_image, cv2.COLOR_BGRA2RGBA))
    
    # Create icons for iOS
    for size in ios_sizes:
        resized_image = image.resize((size, size), Image.LANCZOS)
        output_path = os.path.join(output_folder, f"icon_{size}x{size}.png")
        resized_image.save(output_path, "PNG")
    
    # Create icons for Android
    for folder, size in android_sizes.items():
        resized_image = image.resize((size, size), Image.LANCZOS)
        android_path = os.path.join(output_folder, folder)
        if not os.path.exists(android_path):
            os.makedirs(android_path)
        output_path = os.path.join(android_path, "ic_launcher.png")
        resized_image.save(output_path, "PNG")
    
    # 创建特别尺寸的图像
    create_special_image(image, output_folder, 1024, 500)
    
    print(f"Icons created in {output_folder}")

def create_special_image(image, output_folder, target_width, target_height):
    # 计算新图像的尺寸，保持原始比例
    original_width, original_height = image.size
    ratio = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)

    # 调整图像大小
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    # 创建一个白色背景的新图像
    new_image = Image.new("RGBA", (target_width, target_height), (255, 255, 255, 255))
    # 将调整后的图像粘贴到中心
    top_left_x = (target_width - new_width) // 2
    top_left_y = (target_height - new_height) // 2
    new_image.paste(resized_image, (top_left_x, top_left_y))

    # 保存新图像
    output_path = os.path.join(output_folder, f"special_{target_width}x{target_height}.png")
    new_image.save(output_path, "PNG")

    print(f"Special image created at {output_path}")


def select_image():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path:
        create_app_icons(file_path, "output")
    root.destroy()

gui = Tk()
gui.title("Select Image for App Icon Creation")
open_file_button = Button(gui, text="Open File", command=select_image)
open_file_button.pack()
gui.mainloop()
