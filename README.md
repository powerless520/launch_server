# AnyText: Multilingual Visual Text Generation And Editing

<a href='https://arxiv.org/abs/2311.03054'><img src='https://img.shields.io/badge/Paper-Arxiv-red'></a> <a href='https://github.com/tyxsspa/AnyText'><img src='https://img.shields.io/badge/Code-Github-green'></a> <a href='https://modelscope.cn/studios/damo/studio_anytext'><img src='https://img.shields.io/badge/Demo-ModelScope-lightblue'></a> 

![sample](docs/sample.jpg "sample")

## 📌News
[2023.12.28] - Online demo is available [here](https://modelscope.cn/studios/damo/studio_anytext/summary)!  
[2023.12.27] - 🧨We released the latest checkpoint(v1.1) and inference code, check on [modelscope](https://modelscope.cn/models/damo/cv_anytext_text_generation_editing/summary) in Chinese.  
[2023.12.05] - The paper is available at [here](https://arxiv.org/abs/2311.03054).  

## 💡Methodology
AnyText comprises a diffusion pipeline with two primary elements: an auxiliary latent module and a text embedding module. The former uses inputs like text glyph, position, and masked image to generate latent features for text generation or editing. The latter employs an OCR model for encoding stroke data as embeddings, which blend with image caption embeddings from the tokenizer to generate texts that seamlessly integrate with the background. We employed text-control diffusion loss and text perceptual loss for training to further enhance writing accuracy.

![framework](docs/framework.jpg "framework")

## 🛠Installation
```bash
# Install git (skip if already done)
conda install -c anaconda git
# Clone anytext code
git clone https://github.com/tyxsspa/AnyText.git
cd AnyText
# Prepare a font file; Arial Unicode MS is recommended, **you need to download it on your own**
mv your/path/to/arialuni.ttf ./font/Arial_Unicode.ttf
# Create a new environment and install packages as follows:
conda env create -f environment.yaml
conda activate anytext
```

## 🔮Inference
**[Recommend]**： We release a [demo](https://modelscope.cn/studios/damo/studio_anytext/summary) on ModelScope!

AnyText include two modes: Text Generation and Text Editing. Running the simple code below to perform inference in both modes and verify whether the environment is correctly installed.
```bash
python inference.py
```
If you have advanced GPU (with at least 20G memory), it is recommended to deploy our demo as below, which includes usage instruction, user interface and abundant examples.
```bash
python demo.py
```
![demo](docs/demo.jpg "demo")
**Please note** that when executing inference for the first time, the model files will be downloaded to: `~/.cache/modelscope/hub`. If you need to modify the download directory, you can manually specify the environment variable: `MODELSCOPE_CACHE`.

## 🌄Gallery
![gallery](docs/gallery.png "gallery")


## 📈Evaluation
We use Sentence Accuracy (Sen. ACC) and Normalized Edit Distance (NED) to evaluate the accuracy of generated text, and use the FID metric to assess the quality of generated images. Compared to existing methods, AnyText has a significant advantage in both Chinese and English text generation.
![eval](docs/eval.jpg "eval")

## ⏰TODOs
- [x] Release the model and inference code
- [x] Provide publicly accessible demo link
- [ ] Release tools for merging weights from community models or LoRAs
- [ ] Release AnyText-benchmark dataset and evaluation code
- [ ] Release AnyWord-3M dataset and training code

## Citation
```
@article{tuo2023anytext,
      title={AnyText: Multilingual Visual Text Generation And Editing}, 
      author={Yuxiang Tuo and Wangmeng Xiang and Jun-Yan He and Yifeng Geng and Xuansong Xie},
      year={2023},
      eprint={2311.03054},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

