'''
AnyText: Multilingual Visual Text Generation And Editing
Paper: https://arxiv.org/abs/2311.03054
Code: https://github.com/tyxsspa/AnyText
Copyright (c) Alibaba, Inc. and its affiliates.
'''
import os
from modelscope.pipelines import pipeline
import cv2
import gradio as gr
import numpy as np
import re
from gradio.components import Component
from util import check_channels, resize_image, save_images
import json

BBOX_MAX_NUM = 8
img_save_folder = 'SaveImages'
load_model = True
if load_model:
    inference = pipeline('my-anytext-task', model='damo/cv_anytext_text_generation_editing', model_revision='v1.1.0')


def count_lines(prompt):
    prompt = prompt.replace('“', '"')
    prompt = prompt.replace('”', '"')
    p = '"(.*?)"'
    strs = re.findall(p, prompt)
    if len(strs) == 0:
        strs = [' ']
    return len(strs)


def generate_rectangles(w, h, n, max_trys=200):
    img = np.zeros((h, w, 1), dtype=np.uint8)
    rectangles = []
    attempts = 0
    n_pass = 0
    low_edge = int(max(w, h)*0.3 if n <= 3 else max(w, h)*0.2)  # ~150, ~100
    while attempts < max_trys:
        rect_w = min(np.random.randint(max((w*0.5)//n, low_edge), w), int(w*0.8))
        ratio = np.random.uniform(4, 10)
        rect_h = max(low_edge, int(rect_w/ratio))
        rect_h = min(rect_h, int(h*0.8))
        # gen rotate angle
        rotation_angle = 0
        rand_value = np.random.rand()
        if rand_value < 0.7:
            pass
        elif rand_value < 0.8:
            rotation_angle = np.random.randint(0, 40)
        elif rand_value < 0.9:
            rotation_angle = np.random.randint(140, 180)
        else:
            rotation_angle = np.random.randint(85, 95)
        # rand position
        x = np.random.randint(0, w - rect_w)
        y = np.random.randint(0, h - rect_h)
        # get vertex
        rect_pts = cv2.boxPoints(((rect_w/2, rect_h/2), (rect_w, rect_h), rotation_angle))
        rect_pts = np.int32(rect_pts)
        # move
        rect_pts += (x, y)
        # check boarder
        if np.any(rect_pts < 0) or np.any(rect_pts[:, 0] >= w) or np.any(rect_pts[:, 1] >= h):
            attempts += 1
            continue
        # check overlap
        if any(check_overlap_polygon(rect_pts, rp) for rp in rectangles):
            attempts += 1
            continue
        n_pass += 1
        cv2.fillPoly(img, [rect_pts], 255)
        rectangles.append(rect_pts)
        if n_pass == n:
            break
    print("attempts:", attempts)
    if len(rectangles) != n:
        raise gr.Error(f'Failed in auto generate positions after {attempts} attempts, try again!')
    return img


def check_overlap_polygon(rect_pts1, rect_pts2):
    poly1 = cv2.convexHull(rect_pts1)
    poly2 = cv2.convexHull(rect_pts2)
    rect1 = cv2.boundingRect(poly1)
    rect2 = cv2.boundingRect(poly2)
    if rect1[0] + rect1[2] >= rect2[0] and rect2[0] + rect2[2] >= rect1[0] and rect1[1] + rect1[3] >= rect2[1] and rect2[1] + rect2[3] >= rect1[1]:
        return True
    return False


def draw_rects(width, height, rects):
    img = np.zeros((height, width, 1), dtype=np.uint8)
    for rect in rects:
        x1 = int(rect[0] * width)
        y1 = int(rect[1] * height)
        w = int(rect[2] * width)
        h = int(rect[3] * height)
        x2 = x1 + w
        y2 = y1 + h
        cv2.rectangle(img, (x1, y1), (x2, y2), 255, -1)
    return img


def process(mode, prompt, show_debug, ref_img, ori_img, img_count, ddim_steps, w, h, strength, cfg_scale, seed, eta, a_prompt, n_prompt):
    n_lines = count_lines(prompt)
    # Text Generation
    if None:
        # # create pos_imgs
        # if pos_radio == 'Manual-draw(手绘)':
        #     if draw_img is not None:
        #         pos_imgs = 255 - draw_img['image']
        #         if 'mask' in draw_img:
        #             pos_imgs = pos_imgs.astype(np.float32) + draw_img['mask'][..., 0:3].astype(np.float32)
        #             pos_imgs = pos_imgs.clip(0, 255).astype(np.uint8)
        #     else:
        #         pos_imgs = np.zeros((w, h, 1))
        # elif pos_radio == 'Manual-rect(拖框)':
        #     rect_check = rect_list[:BBOX_MAX_NUM]
        #     rect_xywh = rect_list[BBOX_MAX_NUM:]
        #     checked_rects = []
        #     for idx, c in enumerate(rect_check):
        #         if c:
        #             _xywh = rect_xywh[4*idx:4*(idx+1)]
        #             checked_rects += [_xywh]
        #     pos_imgs = draw_rects(w, h, checked_rects)
        # elif pos_radio == 'Auto-rand(随机)':
        #     pos_imgs = generate_rectangles(w, h, n_lines, max_trys=500)
        pass
    # Text Editing
    elif mode == 'edit':
        revise_pos = False  # disable pos revise in edit mode
        if ref_img is None or ori_img is None:
            raise gr.Error('No reference image, please upload one for edit!')
        edit_image = ori_img.clip(1, 255)  # for mask reason
        edit_image = check_channels(edit_image)
        edit_image = resize_image(edit_image, max_length=768)
        h, w = edit_image.shape[:2]
        if isinstance(ref_img, dict) and 'mask' in ref_img and ref_img['mask'].mean() > 0:
            pos_imgs = 255 - edit_image
            edit_mask = cv2.resize(ref_img['mask'][..., 0:3], (w, h))
            pos_imgs = pos_imgs.astype(np.float32) + edit_mask.astype(np.float32)
            pos_imgs = pos_imgs.clip(0, 255).astype(np.uint8)
        else:
            if isinstance(ref_img, dict) and 'image' in ref_img:
                ref_img = ref_img['image']
            pos_imgs = 255 - ref_img  # example input ref_img is used as pos
    cv2.imwrite('pos_imgs.png', 255-pos_imgs[..., ::-1])
    params = {
        # "sort_priority": sort_radio,
        "show_debug": show_debug,
        "revise_pos": revise_pos,
        "image_count": img_count,
        "ddim_steps": ddim_steps,
        "image_width": w,
        "image_height": h,
        "strength": strength,
        "cfg_scale": cfg_scale,
        "eta": eta,
        "a_prompt": a_prompt,
        "n_prompt": n_prompt
    }
    input_data = {
        "prompt": prompt,
        "seed": seed,
        "draw_pos": pos_imgs,
        "ori_image": ori_img,
    }
    results, rtn_code, rtn_warning, debug_info = inference(input_data, mode=mode, **params)
    if rtn_code >= 0:
        save_images(results, img_save_folder)
        print(f'Done, result images are saved in: {img_save_folder}')
        if rtn_warning:
            gr.Warning(rtn_warning)
    else:
        raise gr.Error(rtn_warning)
    return results, gr.Markdown(debug_info, visible=show_debug)


def create_canvas(w=512, h=512, c=3, line=5):
    image = np.full((h, w, c), 200, dtype=np.uint8)
    for i in range(h):
        if i % (w//line) == 0:
            image[i, :, :] = 150
    for j in range(w):
        if j % (w//line) == 0:
            image[:, j, :] = 150
    image[h//2-8:h//2+8, w//2-8:w//2+8, :] = [200, 0, 0]
    return image


def resize_w(w, img1, img2):
    if isinstance(img2, dict):
        img2 = img2['image']
    return [cv2.resize(img1, (w, img1.shape[0])), cv2.resize(img2, (w, img2.shape[0]))]


def resize_h(h, img1, img2):
    if isinstance(img2, dict):
        img2 = img2['image']
    return [cv2.resize(img1, (img1.shape[1], h)), cv2.resize(img2, (img2.shape[1], h))]


is_t2i = 'true'
block = gr.Blocks(css='style.css', theme=gr.themes.Soft()).queue()

with open('javascript/bboxHint.js', 'r') as file:
    value = file.read()
escaped_value = json.dumps(value)

with block:
    block.load(fn=None,
               _js=f"""() => {{
               const script = document.createElement("script");
               const text =  document.createTextNode({escaped_value});
               script.appendChild(text);
               document.head.appendChild(script);
               }}""")
    gr.HTML('<div style="text-align: center; margin: 20px auto;"> \
            <img id="banner" src="file/example_images/banner.png" alt="anytext"> <br>  \
            [<a href="https://arxiv.org/abs/2311.03054" style="color:blue; font-size:18px;">arXiv</a>] \
            [<a href="https://github.com/tyxsspa/AnyText" style="color:blue; font-size:18px;">Code</a>] \
            [<a href="https://modelscope.cn/models/damo/cv_anytext_text_generation_editing/summary" style="color:blue; font-size:18px;">ModelScope</a>]\
            version: 1.1.0 </div>')
    show_debug=False
    strength =1.0
    cfg_scale =9.0
    eta=0
    with gr.Row(variant='compact'):
        with gr.Column():
            
            with gr.Accordion('🛠Parameters(参数)', open=False):
                with gr.Row(variant='compact'):
                    img_count = gr.Slider(label="Image Count(图片数)", minimum=1, maximum=12, value=4, step=1)
                    ddim_steps = gr.Slider(label="Steps(步数)", minimum=1, maximum=100, value=20, step=1)
                with gr.Row(variant='compact'):
                    image_width = gr.Slider(label="Image Width(宽度)", minimum=256, maximum=768, value=512, step=64)
                    image_height = gr.Slider(label="Image Height(高度)", minimum=256, maximum=768, value=512, step=64)
                # with gr.Row(variant='compact'):
                #     strength = gr.Slider(label="Strength(控制力度)", minimum=0.0, maximum=2.0, value=1.0, step=0.01)
                #     cfg_scale = gr.Slider(label="CFG-Scale(CFG强度)", minimum=0.1, maximum=30.0, value=9.0, step=0.1)
                with gr.Row(variant='compact'):
                    seed = gr.Slider(label="Seed(种子数)", minimum=-1, maximum=99999999, step=1, randomize=False, value=-1)
                    # eta = gr.Number(label="eta (DDIM)", value=0.0)
                a_prompt = gr.Textbox(label="Added Prompt(附加提示词)", value='best quality, extremely detailed,4k, HD, supper legible text,  clear text edges,  clear strokes, neat writing, no watermarks')
                n_prompt = gr.Textbox(label="Negative Prompt(负向提示词)", value='low-res, bad anatomy, extra digit, fewer digits, cropped, worst quality, low quality, watermark, unreadable text, messy words, distorted text, disorganized writing, advertising picture')
            prompt = gr.Textbox(label="Prompt(提示词)")
            with gr.Tabs() as tab_modes:

                with gr.Tab("涂一涂") as mode_edit:
                    with gr.Row(variant='compact'):
                        ref_img = gr.Image(source='upload')
                        ori_img = gr.Image(label='Ori(原图)')

                    def upload_ref(x):
                        return [gr.Image(type="numpy", brush_radius=20, tool='sketch'),
                                gr.Image(value=x)]

                    def clear_ref(x):
                        return gr.Image(source='upload', tool=None)
                    ref_img.upload(upload_ref, ref_img, [ref_img, ori_img])
                    ref_img.clear(clear_ref, ref_img, ref_img)
                    with gr.Row():
                        gr.Markdown("")
                        run_edit = gr.Button(value="运行", scale=0.3, elem_classes='run')
                        gr.Markdown("")
                    gr.Examples(
                        [
                            ['精美的书法作品，上面写着“志” “存” “高” ”远“', "example_images/ref10.jpg", "example_images/edit10.png", 4, 98053044],
                            ['一个表情包，小猪说 "下班"', "example_images/ref2.jpg", "example_images/edit2.png", 2, 43304008],
                            ['Characters written in chalk on the blackboard that says "DADDY"', "example_images/ref8.jpg", "example_images/edit8.png", 4, 73556391],
                            ['一个中国古代铜钱，上面写着"乾" "隆"', "example_images/ref12.png", "example_images/edit12.png", 4, 89159482],
                            ['黑板上写着"Here"', "example_images/ref11.jpg", "example_images/edit11.png", 2, 15353513],
                            ['A letter picture that says "THER"', "example_images/ref6.jpg", "example_images/edit6.png", 4, 72321415],
                            ['一堆水果, 中间写着“UIT”', "example_images/ref13.jpg", "example_images/edit13.png", 4, 54263567],
                            ['一个漫画，上面写着" "', "example_images/ref14.png", "example_images/edit14.png", 4, 94081527],
                            ['一个黄色标志牌，上边写着"不要" 和 "大意"', "example_images/ref3.jpg", "example_images/edit3.png", 2, 64010349],
                            ['A cake with colorful characters that reads "EVERYDAY"', "example_images/ref7.jpg", "example_images/edit7.png", 4, 8943410],
                            ['一个青铜鼎，上面写着"  "和"  "', "example_images/ref4.jpg", "example_images/edit4.png", 4, 71139289],
                            ['一个建筑物前面的字母标牌， 上面写着 " "', "example_images/ref5.jpg", "example_images/edit5.png", 4, 50416289],
                        ],
                        [prompt, ori_img, ref_img, img_count, seed],
                        examples_per_page=5,
                    )
        
        with gr.Column():
            result_gallery = gr.Gallery(label='Result(结果)', show_label=True, preview=True, columns=2, allow_preview=True, height=600)
            result_info = gr.Markdown('', visible=False)
    ips = [prompt,show_debug, ref_img, ori_img, img_count, ddim_steps, image_width, image_height, strength, cfg_scale, seed, eta, a_prompt, n_prompt]
    # run_gen.click(fn=process, inputs=[gr.State('gen')] + ips, outputs=[result_gallery, result_info])
    run_edit.click(fn=process, inputs=[gr.State('edit')] + ips, outputs=[result_gallery, result_info])

block.launch(
    #server_name='0.0.0.0' if os.getenv('GRADIO_LISTEN', '') != '' else "127.0.0.1",
    server_name='0.0.0.0',
    server_port=8188,
    share=False,
    root_path=f"/{os.getenv('GRADIO_PROXY_PATH')}" if os.getenv('GRADIO_PROXY_PATH') else ""
)
# block.launch(server_name='0.0.0.0')
