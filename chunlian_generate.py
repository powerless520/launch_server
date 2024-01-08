import os
from PIL import Image, ImageDraw
import random


class ChunlianGenerator:
    def __init__(self):
        self.image_width = 155
        self.image_height = 135
        self.image_folder = (
            r'C:\Users\acb\Desktop\SaveImages\SaveImages'
        )
        self.save_path = (r'C:\Users\acb\Desktop\spring_festival.png')

    def select_random_images(self, image_paths, num_images):
        folder_paths = [os.path.join(self.image_folder, folder_name) for folder_name in os.listdir(self.image_folder) if
                        os.path.isdir(os.path.join(self.image_folder, folder_name))]

        return random.sample(image_paths, num_images)

    def select_one_images(self, image_paths):
        folder_paths = [os.path.join(self.image_folder, folder_name) for folder_name in os.listdir(self.image_folder) if
                        os.path.isdir(os.path.join(self.image_folder, folder_name))]

        return random.sample(image_paths, 1)

    def find_image_paths_for_text(self, text):
        text = text.lower()
        text_image_paths = []

        for charText in text:
            for folder_name in os.listdir(self.image_folder):
                if charText in folder_name:
                    char_folder_path = os.path.join(self.image_folder, folder_name)
                    if os.path.isdir(char_folder_path):
                        char_image_paths = [os.path.join(char_folder_path, filename) for filename in
                                            os.listdir(char_folder_path) if
                                            filename.lower().endswith(('.png', '.jpg', '.jpeg'))]

                        random_one_path = generator.select_one_images(char_image_paths)

                        text_image_paths.extend(random_one_path)

        return text_image_paths

    def create_chunlian(self, text_images):
        # 创建空白春联图片
        self.image_height = self.image_height*len(text_images)
        spring_festival_image = Image.new('RGB', (self.image_width, self.image_height), color=(135, 13, 8))
        draw = ImageDraw.Draw(spring_festival_image)

        # 计算春联图片中每个文字的高度
        text_height = self.image_height // len(text_images)

        # 在春联图片上贴上文字图片
        for i, text_image in enumerate(text_images):
            # 计算贴上文字图片的位置
            position = ((self.image_width - text_image.width) // 2, i * text_height)

            # 将0像素转为透明
            text_image = text_image.convert("RGBA")
            pixels = text_image.load()
            width, height = text_image.size
            for y in range(height):
                for x in range(width):
                    # print(pixels[x, y][3])
                    if pixels[x, y][3] == 0:
                        pixels[x, y] = (0, 0, 0, 0)  # 将黑色像素转为透明
                    # else:
                    #     pixels[x, y] = (20, 20, 20, 255)  # 将非黑色像素改为黄色 (255, 255, 0)
                    # # else:
                    #     pixels[x, y] = (20, 20, 20)

            # 贴上文字图片
            spring_festival_image.paste(text_image, position, text_image)

        # 春联图片保存到文件
        spring_festival_image.save(self.save_path)


if __name__ == "__main__":
    generator = ChunlianGenerator()

    # 获取用户输入的春联文字
    custom_text = input("请输入春联的文字内容: ")

    matchText = generator.find_image_paths_for_text(custom_text)

    # 从文件夹中随机选择8张图片
    # random_image_paths = generator.select_random_images(matchText, len(custom_text))

    # 加载选中的图片
    text_images = [Image.open(image_path) for image_path in matchText]

    # 在终端显示用户输入的春联文字
    print("春联文字内容: ", custom_text)

    # 创建春联图片
    generator.create_chunlian(text_images)

    print("春联图片已生成并保存。")
