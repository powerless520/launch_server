import cv2
import numpy as np

def segment_calligraphy(image_path):
    # 读取图像
    image = cv2.imread(image_path)

    # 灰度化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 降噪处理
    blurred = cv2.GaussianBlur(binary, (3, 3), 0)

    # 边缘检测
    edges = cv2.Canny(blurred, 100, 200)

    # 边缘平滑处理
    smoothed_edges = cv2.blur(edges, (3, 3))

    # 轮廓检测
    contours, _ = cv2.findContours(smoothed_edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 分割字符
    character_images = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if w > 10 and h > 10:  # 过滤小的轮廓
            character = binary[y:y+h, x:x+w]
            character_images.append(character)


    # 显示分割结果
    for i, character_image in enumerate(character_images):
        # cv2.imshow(f"Character {i+1}", character_image)
        cv2.imwrite(f"/Users/yuelongjin/Desktop/clear/Character {i+1}.png",character_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

# 调用分割函数
segment_calligraphy('/Users/yuelongjin/Desktop/org/18902-4yEkga.jpg')