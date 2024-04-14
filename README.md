# App Icon Generator

## 描述
这个项目提供了一个简单的图形界面，用于创建符合iOS和Android规范的应用图标。它还支持生成特定尺寸（例如1024x500像素）的图像，用于应用商店的横幅或特色图像。

## 功能
- 生成多种尺寸的iOS图标。
- 生成符合各种Android密度的图标（mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi）。
- 生成特别尺寸的图像（例如1024x500像素），图像内容居中，周围填充白色背景。

## 如何使用
1. 确保已安装Python和必要的库（PIL, numpy, opencv-python）。
2. 运行GUI，通过图形界面选择一张图片。
3. 指定输出目录，程序将自动生成所需尺寸的图标并保存。

## 安装
安装必要的Python库：
```bash
pip install Pillow numpy opencv-python opencv-contrib-python
```

## 運行

```bash
python app_icon_generator.py
```
