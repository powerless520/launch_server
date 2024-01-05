import os
import cv2
import numpy as np
import glob
from PIL import Image
import traceback
import requests
          

def segment_calligraphy(image_path):
    # 读取图像
    # os.path.basename(image_path)
    # save_path = os.path.basename(os.path.dirname(image_path))
    
    # save_path = os.path.join(r'C:\Users\acb\Desktop\clear',save_path)

    image_basename = os.path.basename(image_path)
    image_dirname = os.path.basename(os.path.dirname(image_path))
    save_path = os.path.join(r'C:\Users\acb\Desktop\clear', image_dirname)

    # 检查文件夹是否存在
    if not os.path.exists(save_path):
        # 创建文件夹
        os.makedirs(save_path)
        # print("文件夹已创建")
    else:
        # print("文件夹已存在")
        pass



    # image = cv2.imread(image_path)

    # 灰度化
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 读取图片
        
    try:
        response = requests.post(
        'https://picupapi.tukeli.net/api/v1/matting?mattingType=6&crop=true',
        files={'file': open(image_path, 'rb'),},
        headers={'APIKEY': "输入key"},    
        )
        with open(save_path+'/'+image_basename.replace('jpg','png'), 'wb') as out:
            out.write(response.content)
    except Exception as e:
        error_message = f"Error processing image: {image_path}\n"
        error_message += f"Error message: {str(e)}\n"
        error_message += f"Stack trace:\n{traceback.format_exc()}\n"
        with open(r"C:\Users\acb\Desktop\bugtxt.txt", 'a') as bug_file:
            bug_file.write(error_message)


    print('Done '+save_path)




# 调用分割函数
img_lists = glob.glob(r'C:\Users\acb\Documents\WeChat Files\j1611074199\FileStorage\File\2024-01\SaveImages\SaveImages\*\*.jpg')
for img in img_lists:
    segment_calligraphy(img)
    break