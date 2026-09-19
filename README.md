# LingT2I: On the Limitations of Cross-Lingual Consistency in Multilingual Text-to-Image Generation
[![paper](https://img.shields.io/badge/Paper-ArXiv-B31B1B.svg)](https://arxiv.org/abs/2608.11002)
[![Benchmark](https://img.shields.io/badge/Dataset-LingT2I-orange)](https://huggingface.co/datasets/RISys-Lab/LingT2I)

A benchmark covering 10 widely used
languages with 33K prompts, designed to evaluate cross-lingual
effects in both content generation and text rendering. Building on
this benchmark, we conduct a comprehensive cross-lingual analysis,
uncovering linguistic inequality and language-dependent trade-offs
across evaluation dimensions. 

## Quick Start

### LingT2I Benchmark

Load from [🤗 Hugging Face](https://huggingface.co/datasets/RISys-Lab/LingT2I).

> [!NOTE]
> Legacy JSON is still supported for reproducing earlier experiments. Parquet
> splits from Hugging Face are the default data source.

~~~python
from datasets import load_dataset

ds_cg = load_dataset(
    "RISys-Lab/LingT2I",
    split="content_generation",
)
ds_tr = load_dataset(
    "RISys-Lab/LingT2I",
    split="text_rendering",
)

sample_cg = ds_cg[0]
sample_tr = ds_tr[0]

print(sample_cg["prompt"])
print(sample_cg["dimension"], sample_cg["lang"])

print(sample_tr["prompt"])
print(sample_tr["render_text"])
print(sample_tr["condition_image"])
~~~

The benchmark contains two tasks:

- **content_generation** evaluates cross-lingual consistency for multilingual
  text-to-image prompts.
- **text_rendering** evaluates multilingual rendering with render text, layout
  metadata, and an embedded condition image.

Content-generation scoring uses
**lingt2i/evaluation/metaclip2_score.py**. Text-rendering evaluation uses
**lingt2i/evaluation/ocr.py**.

## Setup

### Installation

~~~bash
conda create -n lingt2i python=3.10 -y
conda activate lingt2i
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
pip install -r requirements.txt
~~~

For VLM-based evaluation, deploy an OpenAI-compatible endpoint with vLLM:

~~~bash
pip install accelerate
pip install 'vllm>=0.7.2'

vllm serve Qwen/Qwen2.5-VL-7B-Instruct \
  --port 8000 \
  --device cuda \
  --host 0.0.0.0 \
  --dtype bfloat16 \
  --limit-mm-per-prompt image=5,video=5
~~~

## Getting Started

### Content Generation

Set up a YAML file in **configs/**:

~~~yaml
name: "lingt2i-content"
dataset_name: "RISys-Lab/LingT2I"
split: "content_generation"
start_idx: 0
end_idx: 30000
output_dir: "outputs/content_generation"

generation:
  models: ["zimage"]
~~~

Run the shared content-generation pipeline:

~~~bash
python -m lingt2i.generation.content \
  --config configs/content_generation.yaml
~~~

For the multilingual FLUX adapter:

~~~bash
python -m lingt2i.generation.pea
~~~

### Text Rendering Generation

Prompt-only text-rendering models:

~~~bash
python -m lingt2i.generation.flux --start_idx 0 --end_idx 10
python -m lingt2i.generation.qwen --start_idx 0 --end_idx 10
python -m lingt2i.generation.seedream --start_idx 0 --end_idx 10
python -m lingt2i.generation.nano --start_idx 0 --end_idx 10
python -m lingt2i.generation.imagen4 --start_idx 0 --end_idx 10
~~~

Placement-aware text-rendering models:

~~~bash
python -m lingt2i.generation.anytext --max_samples 10
python -m lingt2i.generation.anytext2
python -m lingt2i.generation.easytext --max_samples 10
~~~

AnyText, AnyText2, and EasyText implementations are kept under
**lingt2i/third_party/**, while benchmark entry points remain under
**lingt2i/generation/**.

### Content Evaluation

Use MetaCLIP2 to evaluate multilingual content alignment:

~~~bash
python -m lingt2i.evaluation.metaclip2_score \
  --image_folder outputs/content_generation/zimage \
  --dataset_name RISys-Lab/LingT2I \
  --split content_generation \
  --out_csv results/metaclip2_zimage.csv
~~~

### Text Rendering Evaluation

Run OCR and text-rendering metrics:

~~~bash
python -m lingt2i.evaluation.ocr \
  --model_path outputs/text_rendering/EasyText \
  --dataset_name RISys-Lab/LingT2I \
  --split text_rendering \
  --ocr_mode gemini \
  --use_position \
  --output_file results.json
~~~

The OCR output contains:

- Character-level normalized edit distance.
- Token-level normalized edit distance.
- Exact sentence accuracy.
- Word accuracy.
- A combined average score.

Additional evaluation modules include:

- **demographic_bias.py** for demographic representation.
- **cultural_bias.py** for culture-specific elements and bias.
- **nsfw.py** for multilingual safety.
- **trig_score.py** for multilingual TRIG dimension scoring.
- **summary.py** for compact per-language OCR summaries.

## Repository Structure

- **configs/**: experiment and model-path configuration.
- **lingt2i/data.py**: Hugging Face and legacy JSON data loaders.
- **lingt2i/generation/**: content-generation and text-rendering entry points.
- **lingt2i/evaluation/**: content, OCR, bias, cultural, and safety evaluation.
- **lingt2i/models/**: the copied text-to-image model layer shared with TRIG.
- **lingt2i/analysis/**: dataset and result analysis helpers.
- **lingt2i/tools/**: data-preparation and X2I projection utilities.
- **lingt2i/third_party/**: AnyText, AnyText2, and EasyText implementations.
- **assets/fonts/**: multilingual font resources.

## Acknowledgement

Many thanks to the great works in multilingual image generation, including
[FLUX](https://huggingface.co/black-forest-labs/FLUX.1-dev),
[Qwen-Image](https://huggingface.co/Qwen/Qwen-Image),
[AnyText](https://github.com/tyxsspa/AnyText),
[AnyText2](https://github.com/tyxsspa/AnyText2), and
[EasyText](https://github.com/HiDream-ai/EasyText).

## Citation

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.

The LingT2I BibTeX entry will be added when the paper is released.

```bibtex
@misc{zhang2026limitationscrosslingualconsistencymultilingual,
      title={On the Limitations of Cross-Lingual Consistency in Multilingual Text-to-image Generation}, 
      author={Sicheng Zhang and Zhonghao Yan and Binzhu Xie and Shi Qiu and Muzammal Naseer and Naveed Akhtar and Mubarak Shah},
      year={2026},
      eprint={2608.11002},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2608.11002}, 
}
```
