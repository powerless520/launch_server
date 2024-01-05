import os
from modelscope.pipelines import pipeline
import cv2
import gradio as gr
import numpy as np
import re
from gradio.components import Component
from util import check_channels, resize_image, save_images
import json
os.environ["CUDA_VISIBLE_DEVICES"]="2"
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


def check_overlap_polygon(rect_pts1, rect_pts2):
    poly1 = cv2.convexHull(rect_pts1)
    poly2 = cv2.convexHull(rect_pts2)
    rect1 = cv2.boundingRect(poly1)
    rect2 = cv2.boundingRect(poly2)
    if rect1[0] + rect1[2] >= rect2[0] and rect2[0] + rect2[2] >= rect1[0] and rect1[1] + rect1[3] >= rect2[1] and rect2[1] + rect2[3] >= rect1[1]:
        return True
    return False



def process(mode, prompt, ref_img, ori_img, img_count, seed):
  
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
    strength = 1
    cfg_scale = 9
    eta = 0
    w, h = 768, 768
    ddim_steps = 25

    a_prompt = 'best quality, extremely detailed,4k, HD, supper legible text,  clear text edges,  clear strokes, neat writing, no watermarks'
    n_prompt = 'low-res, bad anatomy, extra digit, fewer digits, cropped, worst quality, low quality, watermark, unreadable text, messy words, distorted text, disorganized writing, advertising picture'
    params = {
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
    return results



block = gr.Blocks().queue()


with block:

    with gr.Row(variant='compact'):
        ref_img = gr.Image(label='参考图', source='upload',height=600)
        ori_img = gr.Image(visible=False)
        result_gallery = gr.Gallery(label='结果', show_label=True, preview=True, columns=2, allow_preview=True, height=600)


    def upload_ref(x):
        return [gr.Image(type="numpy", brush_radius=30, tool='sketch'),
                gr.Image(value=x)]

    def clear_ref(x):
        return gr.Image(source='upload', tool=None)
    ref_img.upload(upload_ref, ref_img, [ref_img, ori_img])
    ref_img.clear(clear_ref, ref_img, ref_img)

    with gr.Row():
        gr.Markdown("")
        run_edit = gr.Button(value="运行", scale=0.3, elem_classes='run')
        gr.Markdown("")
    with gr.Row(variant='compact'):
       
        prompt = gr.Textbox(label="提示词")
        img_count = gr.Slider(label="图片数", minimum=1, maximum=12, value=4, step=1)
        seed = gr.Slider(label="Seed(种子数)", minimum=-1, maximum=99999999, step=1, randomize=False, value=-1)
               
    gr.Examples(
        [
            ['精美的书法作品，上面写着“志” “存” “高” ”远“', "example_images/ref10.jpg", "example_images/edit10.png", 4, 98053044],
            ['一个表情包，小猪说 "下班"', "example_images/ref2.jpg", "example_images/edit2.png", 2, 43304008],
            ['一个中国古代铜钱，上面写着"乾" "隆"', "example_images/ref12.png", "example_images/edit12.png", 4, 89159482],
            ['一个漫画，上面写着" "', "example_images/ref14.png", "example_images/edit14.png", 4, 94081527],
            ['一个黄色标志牌，上边写着"不要" 和 "大意"', "example_images/ref3.jpg", "example_images/edit3.png", 2, 64010349],
            ['一个青铜鼎，上面写着"  "和"  "', "example_images/ref4.jpg", "example_images/edit4.png", 4, 71139289],
            ['一个建筑物前面的字母标牌， 上面写着 " "', "example_images/ref5.jpg", "example_images/edit5.png", 4, 50416289],
        ],
        [prompt, ori_img, ref_img, img_count, seed],
        examples_per_page=8,
    )
    
    ips = [prompt, ref_img, ori_img, img_count ,seed]
    run_edit.click(fn=process, inputs=[gr.State('edit')] + ips, outputs=[result_gallery])

# block.launch(
#     server_name='0.0.0.0' if os.getenv('GRADIO_LISTEN', '') != '' else "127.0.0.1",
#     share=False,
#     root_path=f"/{os.getenv('GRADIO_PROXY_PATH')}" if os.getenv('GRADIO_PROXY_PATH') else ""
# )
block.launch(server_name='0.0.0.0',server_port=8188)
