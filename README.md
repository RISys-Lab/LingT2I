# LingT2I

Generation and evaluation code for **LingT2I: On the Limitations of
Cross-Lingual Consistency in Multilingual Text-to-Image Generation**.

LingT2I is the multilingual benchmark that was originally developed inside
the TRIG repository. This repository keeps LingT2I-specific code together and
contains local copies of the small amount of TRIG infrastructure it still
shares. The two projects therefore do not depend on each other's checkout.

## Dataset

The default dataset is
[RISys-Lab/TRIG-Multilingual](https://huggingface.co/datasets/RISys-Lab/TRIG-Multilingual).
It contains two public splits:

- **content_generation**: multilingual prompts used to measure cross-lingual
  content consistency.
- **text_rendering**: multilingual text-rendering prompts with render text,
  layout metadata, and an embedded condition image.

Example:

    from datasets import load_dataset

    content = load_dataset(
        "RISys-Lab/TRIG-Multilingual",
        split="content_generation",
    )
    rendering = load_dataset(
        "RISys-Lab/TRIG-Multilingual",
        split="text_rendering",
    )

Legacy JSON inputs remain supported by the data helpers for reproducing older
experiments.

## Repository layout

- **configs/**: content-generation and local model-path configuration.
- **lingt2i/data.py**: shared Hugging Face and legacy JSON loaders.
- **lingt2i/generation/**: content-generation and text-rendering entry points.
- **lingt2i/evaluation/**: MetaCLIP2, OCR, bias, cultural-bias, safety, and
  result-summary code.
- **lingt2i/evaluation/ocr_support/**: OCR recognizer modules and language
  dictionaries.
- **lingt2i/models/**: a copied subset of the TRIG text-to-image model layer.
- **lingt2i/analysis/**: dataset and result statistics.
- **lingt2i/tools/**: text-rendering preparation and X2I projection utilities.
- **third_party/**: vendored AnyText, AnyText2, and EasyText adapters.
- **assets/fonts/**: multilingual font resources.
- **lingt2i/evaluation/legacy/**: older JSON/path-based scripts retained for
  experiment provenance, but kept out of the primary pipeline.

Large rebuttal material, generated images, model weights, and machine-local
caches are intentionally excluded.

## Content generation

The former TRIG task name t2i_ml is represented directly by the
content_generation split here.

Configuration:

    name: "lingt2i-content"
    dataset_name: "RISys-Lab/TRIG-Multilingual"
    split: "content_generation"
    start_idx: 0
    end_idx: 30000
    generation:
      models: ["zimage"]

Entry point:

    python -m lingt2i.generation.content \
      --config configs/content_generation.yaml

The multilingual FLUX adapter also has a dedicated entry point:

    python -m lingt2i.generation.pea

## Text rendering

Prompt-only model entry points:

    python -m lingt2i.generation.flux --start_idx 0 --end_idx 10
    python -m lingt2i.generation.qwen --start_idx 0 --end_idx 10
    python -m lingt2i.generation.seedream --start_idx 0 --end_idx 10
    python -m lingt2i.generation.nano --start_idx 0 --end_idx 10
    python -m lingt2i.generation.imagen4 --start_idx 0 --end_idx 10

Placement-aware model entry points:

    python -m lingt2i.generation.anytext --max_samples 10
    python -m lingt2i.generation.anytext2
    python -m lingt2i.generation.easytext --max_samples 10

AnyText, AnyText2, and EasyText implementation code lives under third_party;
the benchmark-facing launchers remain under lingt2i/generation.

## Evaluation

Content similarity with MetaCLIP2:

    python -m lingt2i.evaluation.metaclip2_score \
      --image_folder outputs/content_generation/zimage \
      --dataset_name RISys-Lab/TRIG-Multilingual \
      --split content_generation \
      --out_csv results/metaclip2_zimage.csv

Text-rendering OCR:

    python -m lingt2i.evaluation.ocr \
      --model_path outputs/text_rendering/EasyText \
      --dataset_name RISys-Lab/TRIG-Multilingual \
      --split text_rendering \
      --ocr_mode gemini \
      --use_position \
      --output_file results.json

OCR results include character NED, token NED, exact sentence accuracy, word
accuracy, and a combined average score. Use lingt2i/evaluation/summary.py to
produce compact per-language summaries.

Additional evaluation modules:

- **demographic_bias.py**: demographic representation analysis.
- **cultural_bias.py**: culture-specific element and bias analysis.
- **nsfw.py**: multilingual safety analysis.
- **trig_score.py**: the multilingual TRIG dimension score retained from the
  shared evaluation toolkit.

## Relationship to TRIG

TRIG remains the repository for the ICCV 2025 trade-off benchmark covering
text-to-image, image editing, and subject-driven generation. LingT2I is a
separate multilingual follow-up benchmark. Shared data-loading, model, and
metric logic is copied into this repository so future changes can evolve
independently.
