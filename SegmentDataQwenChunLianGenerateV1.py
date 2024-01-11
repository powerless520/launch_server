import os
from PIL import Image, ImageDraw
import random
import dashscope
from dashscope import Generation
from http import HTTPStatus
import json
from dashscope import TextEmbedding
import yaml
import datetime

RESULT_PATH='./result' 
DATA_PATH = './shufa'

def create_path(folder_path):
    if not os.path.exists(folder_path):
        # 如果文件夹不存在，创建文件夹
        os.makedirs(folder_path)
    else:
        # 如果文件夹存在，跳过
        pass

def load_oss_config(config_path='config.yaml'):
    with open(config_path, 'r') as file:
        yaml_config = yaml.safe_load(file)
    return yaml_config.get('oss_config')

class ChunlianGenerator:
    def __init__(self):
        self.image_width = 180
        self.image_height = 180
        self.image_width_h = 150
        self.image_height_h = 150
        self.image_folder = DATA_PATH
        now = datetime.datetime.now()
        self.formatted_time = now.strftime("%Y-%m-%d-%H-%M-%S")
        self.shanglian=None
        self.xialian=None
        self.hengpi=None
        self.custom_text=None
       
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

                        random_one_path = self.select_one_images(char_image_paths)

                        text_image_paths.extend(random_one_path)
        
        return text_image_paths
    

    def make_transparent(self,text_image):
        text_image = text_image.convert("RGBA")
        pixels = text_image.load()
        width, height = text_image.size
        for y in range(height):
            for x in range(width):
                # print(pixels[x, y][3])
                if pixels[x, y][3] == 0:
                    pixels[x, y] = (0, 0, 0, 0)  # 将黑色像素转为透明
        
        return text_image

    def padding(self,text_image):
        white_image = Image.new('RGBA', (self.image_width, self.image_height), color=(0, 0, 0, 0)) 
        draw = ImageDraw.Draw(white_image)
        text_width, text_height = text_image.size
        # 计算居中的位置
        x = (self.image_width - text_width) // 2
        y = (self.image_height - text_height) // 2

        text_image = self.make_transparent(text_image)
        white_image.paste(text_image, (x, y))
        white_image.save('result/test.png')
        return white_image# 保存结果图片

    def create_duilian(self, text_images,save_name):
        ims=[]
        for im in text_images:
            ims.append(self.padding(im))
        text_images = ims

        if save_name=='上联':
            save_path = os.path.join(RESULT_PATH,self.formatted_time+'-'+self.custom_text+'_'+save_name+'_'+self.shanglian+'.png')
        else:
            save_path = os.path.join(RESULT_PATH,self.formatted_time+'-'+self.custom_text+'_'+save_name+'_'+self.xialian+'.png')
        
        
        image_height = self.image_height * len(text_images)
        image_width = self.image_width

        spring_festival_image = Image.new('RGB', (image_width, image_height+30), color=(114, 20, 0))
        draw = ImageDraw.Draw(spring_festival_image)

        # 计算春联图片中每个文字的高度
        text_height = image_height // len(text_images)

        # 在春联图片上贴上文字图片
        for i, text_image in enumerate(text_images):
            # 计算贴上文字图片的位置
            position = (image_width - text_image.width) // 2, i * text_height+100//len(text_images)
            # 将0像素转为透明
            text_image = self.make_transparent(text_image)

            # 贴上文字图片
            spring_festival_image.paste(text_image, position, text_image)

        # 春联图片保存到文件
        spring_festival_image.save(save_path)
        self.save2class(save_name,spring_festival_image)


    def create_hengpi(self, text_images,save_name):
        ims=[]
        for im in text_images:
            ims.append(self.padding(im))
        text_images = ims

        save_path = os.path.join(RESULT_PATH,self.formatted_time+'-'+self.custom_text+'_'+save_name+'_'+self.hengpi+'.png')
        image_width = self.image_width_h * len(text_images) 
        image_height = self.image_height_h 
        spring_festival_image = Image.new('RGB', (100+image_width, 60+image_height), color=(114, 20, 0))
        draw = ImageDraw.Draw(spring_festival_image)

        # 计算春联图片中每个文字的高度
        text_width = image_width // len(text_images)

        # 在春联图片上贴上文字图片
        for i, text_image in enumerate(text_images):
            # 计算贴上文字图片的位置
            position = (30+i * text_width, 30+((image_height - text_image.height) // 2))

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
            self.shanglian_image=image
        if name == '下联':
            self.xailian_image=image
        if name == '横批':
            self.hengpi_image=image
    
    def merg_chunlian(self):
        

        # 读取上联图像
        image1 =  self.shanglian_image

        # 读取下联图像
        image2 = self.xailian_image

        # 读取横批图像
        horizontal_image = self.hengpi_image

        # 创建一个iPhone屏幕大小的画布
        # canvas = Image.new("RGB", (1400, 1300), "white")
        canvas = Image.new("RGBA", (1284, 2778), (0, 0, 0, 0))


        # 计算上联图像的位置
        x1 = 150
        y1 = 350
        x2 = x1 + image1.width
        y2 = y1 + image1.height

        # 计算下联图像的位置
        x3 = 1284 -image2.width-150
        y3 = 350
        x4 = x3 + image2.width
        y4 = y3 + image2.height

        # 计算横批图像的位置
        x5 = int(1284/2-horizontal_image.width/2)
        y5 = 100
        x6 = x5 + horizontal_image.width
        y6 = y5 + horizontal_image.height

        # 在画布上绘制图像
        canvas.paste(image1, (x1, y1, x2, y2))
        canvas.paste(image2, (x3, y3, x4, y4))
        canvas.paste(horizontal_image, (x5, y5, x6, y6))

        # 保存结果图像
        # print()
        save_path = os.path.join(RESULT_PATH,self.formatted_time+'-'+self.custom_text+'-春联'+'-'+self.hengpi+'.png')
        canvas.save(save_path)
        return save_path
        

class LLM():
    def __init__(self,model='qwen-max-1201'):
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
你精通春节对联的各种技巧，如平仄、对仗、意境的把控，具备出色的文学造诣，能根据不同的需求、春节对联使用场景创作高雅、内涵丰富的、富有中国文化底蕴的龙年春节对联。

对联格式要求：上联七个字，下联七个字，横批四个字。除非用户单独提要求，否则请务必按照此格式书写对联。输出时请按下面这种格式输出
{
    "上联":"你写的上联"
    "下联":"你写的下联"
    "横批":"你写的横批"
}

用户输入的主题是：“祝福”，输入的名字是"xxx"
必须要做到上下联的字数限制，上联七个字，下联七个字，横批四个字，把用户的名字藏在对联之中，注意不要连续出现，每个字只出现一次，并且要分开，不能出现在横批上,不要标点符号，同时保证平仄、对仗，文采

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
        


def pipeline(custom_text):
    # try:
        config = load_oss_config()
        dashscope.api_key = config['dashscope.api_key']
        create_path(RESULT_PATH)
        generator = ChunlianGenerator()
        llm = LLM()
        # 获取用户输入的春联文字
        generator.custom_text = custom_text
        for i in range(10):
            try:
                curr_gpt_response = llm.request(custom_text)
                shanglian,xialian,hengpi = llm.parse(curr_gpt_response)
                # print("上联",shanglian)
                # print("下联",xialian)
                # print("横批",hengpi)

                print('len(shanglian)!=len(xialian) ',len(shanglian)!=len(xialian))
                print('custom_text in shanglian+xialian+hengpi',custom_text in shanglian+xialian+hengpi)
                print('len(hengpi)!=4',len(hengpi)!=4)
                print("len(shanglian)>9",len(shanglian)>9)

                if len(shanglian)!=len(xialian) or (custom_text in shanglian+xialian+hengpi) or len(hengpi)!=4 or len(shanglian)>9:
                    continue
                else:
                    generator.shanglian=shanglian
                    generator.xialian=xialian
                    generator.hengpi=hengpi
            
                break
            except Exception as e:
                print("An error occurred:", e)
                continue

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
        

        print("春联图片已生成并保存。")
        return True, generator.merg_chunlian()
    
    # except Exception as e:
    #     print("An error occurred:", e)
    #     return False,None


if __name__ == "__main__":
    config = load_oss_config()
    dashscope.api_key = config['dashscope.api_key']
    create_path(RESULT_PATH)
    generator = ChunlianGenerator()
    llm = LLM()
    # 获取用户输入的春联文字
    custom_text = input("请输入春联的文字内容: ")
    generator.custom_text = custom_text
    for i in range(10):
        try:
            curr_gpt_response = llm.request(custom_text)
            shanglian,xialian,hengpi = llm.parse(curr_gpt_response)
            # print("上联",shanglian)
            # print("下联",xialian)
            # print("横批",hengpi)

            print('len(shanglian)!=len(xialian) ',len(shanglian)!=len(xialian))
            print('custom_text in shanglian+xialian+hengpi',custom_text in shanglian+xialian+hengpi)
            print('len(hengpi)!=4',len(hengpi)!=4)
            print("len(shanglian)>9",len(shanglian)>9)

            if len(shanglian)!=len(xialian) or (custom_text in shanglian+xialian+hengpi) or len(hengpi)!=4 or len(shanglian)>9:
                continue
            else:
                generator.shanglian=shanglian
                generator.xialian=xialian
                generator.hengpi=hengpi
          
            break
        except Exception as e:
            print("An error occurred:", e)
            continue

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
    save_path = generator.merg_chunlian()

    print("春联图片已生成并保存。")



