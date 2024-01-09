import os
from PIL import Image, ImageDraw
import random
import dashscope
from dashscope import Generation
from http import HTTPStatus
import json
from dashscope import TextEmbedding
dashscope.api_key = "输入key"

class ChunlianGenerator:
    def __init__(self):
        self.image_width = 155
        self.image_height = 135
        self.image_folder = (

            r'C:\Users\acb\Desktop\SaveImages\SaveImages'
        )
       

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

    def create_duilian(self, text_images,save_name):

        save_path = 'C:/Users/acb/Desktop/'+ save_name +'.png'
        image_height = self.image_height * len(text_images)
        image_width = self.image_width
        spring_festival_image = Image.new('RGB', (image_width, image_height), color=(135, 13, 8))
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
                    # else:
                    #     pixels[x, y] = (20, 20, 20, 255)  # 将非黑色像素改为黄色 (255, 255, 0)
                    # # else:
                    #     pixels[x, y] = (20, 20, 20)

            # 贴上文字图片
            spring_festival_image.paste(text_image, position, text_image)

        # 春联图片保存到文件
        spring_festival_image.save(save_path)
        self.save2class(save_name,spring_festival_image)


    def create_hengpi(self, text_images,save_name):

        save_path = 'C:/Users/acb/Desktop/'+ save_name +'.png'
        image_width = self.image_width * len(text_images)
        image_height = self.image_height
        spring_festival_image = Image.new('RGB', (image_width, image_height), color=(135, 13, 8))
        draw = ImageDraw.Draw(spring_festival_image)

        # 计算春联图片中每个文字的高度
        text_width = image_width // len(text_images)

        # 在春联图片上贴上文字图片
        for i, text_image in enumerate(text_images):
            # 计算贴上文字图片的位置
            position = (i * text_width, (image_height - text_image.height) // 2)

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
        spring_festival_image.save(save_path)
        self.save2class(save_name,spring_festival_image)

    def save2class(self,name,image):
        if name == '上联':
            self.shanglian=image
        if name == '下联':
            self.xailian=image
        if name == '横批':
            self.hengpi=image
    
    def merg_chunlian(self):
        

        # 读取上联图像
        image1 =  self.shanglian

        # 读取下联图像
        image2 =self.xailian

        # 读取横批图像
        horizontal_image = self.hengpi

        # 创建一个iPhone屏幕大小的画布
        canvas = Image.new("RGB", (1400, 1300), "white")

        # 计算上联图像的位置
        x1 = 150
        y1 = 200
        x2 = x1 + image1.width
        y2 = y1 + image1.height

        # 计算下联图像的位置
        x3 = 1400 -image2.width-150
        y3 = 200
        x4 = x3 + image2.width
        y4 = y3 + image2.height

        # 计算横批图像的位置
        x5 = int(1400/2-horizontal_image.width/2)
        y5 = 100
        x6 = x5 + horizontal_image.width
        y6 = y5 + horizontal_image.height

        # 在画布上绘制图像
        canvas.paste(image1, (x1, y1, x2, y2))
        canvas.paste(image2, (x3, y3, x4, y4))
        canvas.paste(horizontal_image, (x5, y5, x6, y6))

        # 保存结果图像
        canvas.save(r"C:\Users\acb\Desktop\result.png")

class LLM():
    def __init__(self,model='qwen-turbo'):
        '''
        qwen-turbo
        qwen-plus
        qwen-max
        qwen-max-1201
        qwen-max-longcontext
        '''
        self.top_p=0.8
        self.model = model
    def request(self,input):
        self.input = input
        self.prompt = self.cangtoushi(input)
        response = Generation.call(
                    model=self.model,
                    top_p = self.top_p,
                    prompt = self.prompt
                    )
        if response.status_code == HTTPStatus.OK:
            # print(json.dumps(response.output, indent=4, ensure_ascii=False))
            # print(json.dumps(response.usage, indent=4, ensure_ascii=False))
            curr_gpt_response = response.output['text']
            print(curr_gpt_response)
            return curr_gpt_response
        else:
            print('Code: %d, status: %s, message: %s' % (response.status_code, response.code, response.message))
        
    def cangtoushi(self,input):
        prompt = '''
角色：你是一位春节对联大师，你的任务是根据用需求为用户书写对仗工整、富有意境、具备深厚中国文化底蕴、符合春节对联使用场景、符合春节对联格式要求并且包含龙年元素的春节对联。

能力：
你精通中国传统节日文化提别是各地的春节文化习俗、龙年相关的传统和习俗。
你精通中国的四书五经、唐诗宋词以及各种对联名作的书写技巧、典故运用和表现手法。
你对中国传统对联的历史、春节对联历史、春节文化和艺术有深入的研究和理解。
你精通中国风水学及中国风水学在春节对联和贴联中的应用。
你精通春节对联的各种技巧，如平仄、对仗、意境的把控，具备出色的文学造诣，能根据不同的需求、春节对联使用场景创作高雅、内涵丰富的、富有中国文化底蕴的龙年春节对联。
你对春节对联在不同场合的使用有丰富的知识和经验，熟悉传统和现代的对联贴法，能够指导人们正确地张贴春节对联。

对联格式要求：上联七个字，下联七个字，横批四个字。除非用户单独提要求，否则请务必按照此格式书写对联。输出时请按下面这种格式输出
{
    "上联":"你写的上联"
    "下联":"你写的下联"
    "横批":"你写的横批"
}

处理流程：
(1) 信息收集：给用户书写春节对联前，务必首先了解他们的具体需求，如春节对联的使用场合、场地、主题、风格等。如果用的的需求为包含足够的信息，请务必充分发挥你作为沟通大师和需求收集大师的能力，根据你掌握的春节对联风水学知识、春节对联的贴联知识和贴联技巧判断需要用户提供哪些信息，并引导用户提供足够你书写高雅、内涵丰富的、富有中国文化底蕴的春节对联的信息。
(2) 写龙年春节对联：收集完信息后，充分理解用户需求和春节对
联使用场地、场合，充分借鉴和应用四书五经、唐诗宋词以及各种对联名作的书写技巧、典故运用和表现手法，充分调动你掌握的中国传统文化、春节文化知识，充分发挥你的文学造诣书写对仗工整、富有意境、具备深厚中国文化底蕴、符合春节对联使用场景、符合春节对联格式要求的龙年春节对联。
(3) 贴对联指导：书写完对联后，为用户提供贴心的贴对联的指导。

用户输入的主题是：表达爱意，输入的名字是"xxx"，用户输入的姓名必须分开，对联中必须包含姓名，注意不要很直白的表达用户的意思，对联格式要求：上联七个字，下联七个字，横批四个字。除非用户单独提要求，否则请务必按照此格式书写对联。
''' 
        target_location = prompt.find("xxx")
        target_length = len("xxx")
        # 在目标位置插入文本
        modified_text = prompt[:target_location] + input + prompt[target_location+target_length:]
        return modified_text
        
    def parse(self,curr_gpt_response):
        end_index = curr_gpt_response.rfind('}') + 1
        start_index = curr_gpt_response.find('{')
        curr_gpt_response = curr_gpt_response[start_index:end_index]
        # print(curr_gpt_response)
        shanglian = json.loads(curr_gpt_response)["上联"]
        xialian = json.loads(curr_gpt_response)["下联"]
        hengpi = json.loads(curr_gpt_response)["横批"]
        return shanglian,xialian,hengpi
        



if __name__ == "__main__":
    generator = ChunlianGenerator()
    llm = LLM()
    # 获取用户输入的春联文字
    custom_text = input("请输入春联的文字内容: ")
    for i in range(5):
        try:
            curr_gpt_response = llm.request(custom_text)
            shanglian,xialian,hengpi = llm.parse(curr_gpt_response)
            print("上联",shanglian)
            print("下联",xialian)
            print("横批",hengpi)
            break
        except Exception as e:
            print("An error occurred:", e)
            continue
    
    text_images = []

    shanglian = generator.find_image_paths_for_text(shanglian)
    xialian = generator.find_image_paths_for_text(xialian)
    hengpi = generator.find_image_paths_for_text(hengpi)

    # 加载选中的图片
    shanglian_image = [Image.open(image_path) for image_path in shanglian]
    xialian_image = [Image.open(image_path) for image_path in xialian]
    hengpi_image = [Image.open(image_path) for image_path in hengpi]


    # 创建上联图片
    generator.create_duilian(shanglian_image,"上联")
    generator.create_duilian(xialian_image,"下联")
    generator.create_hengpi(hengpi_image,"横批")
    generator.merg_chunlian()

    print("春联图片已生成并保存。")



