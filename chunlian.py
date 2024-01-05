import os
from PIL import Image, ImageDraw

# 设置春联图片的宽度和高度
image_width = 500
image_height = 1000

# 获取文字图片文件夹中的所有图片文件
image_folder = r'C:\Users\acb\Desktop\clear\2024-01-04-不'
text_images = []
for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(image_folder, filename)
        text_image = Image.open(image_path)
        text_images.append(text_image)

# 创建空白春联图片
spring_festival_image = Image.new('RGB', (image_width, image_height), color=(163, 0, 0))
draw = ImageDraw.Draw(spring_festival_image)

# 计算春联图片中每个文字的高度
text_height = image_height // len(text_images)

# 在春联图片上贴上文字图片
for i, text_image in enumerate(text_images):
    # 计算贴上文字图片的位置
    position = ((image_width - text_image.width) // 2, i * text_height)
    
    # 将0像素转为透明
    text_image = text_image.convert("RGBA")
    pixels = text_image.load()
    width, height = text_image.size
    for y in range(height):
        for x in range(width):
            # print(pixels[x, y][3])
            if pixels[x, y][3] == 0:
                pixels[x, y] = (0, 0, 0, 0)  # 将黑色像素转为透明
            else:
                pixels[x, y] = (20, 20, 20, 255)  # 将非黑色像素改为黄色 (255, 255, 0)
            # else:
            #     pixels[x, y] = (20, 20, 20) 
    
    # 贴上文字图片
    spring_festival_image.paste(text_image, position, text_image)

# 春联图片保存到文件
spring_festival_image.save(r'C:\Users\acb\Desktop\clear\spring_festival.png')