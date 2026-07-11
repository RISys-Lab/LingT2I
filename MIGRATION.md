# Extraction map

This file records how the LingT2I code was separated from TRIG.

| Original TRIG location | LingT2I location | Role |
| --- | --- | --- |
| trig_multilingual/data.py | lingt2i/data.py | Dataset access |
| trig_multilingual/generation/ | lingt2i/generation/ | Generation entry points |
| trig_multilingual/evaluation/trig_ml_ocr.py | lingt2i/evaluation/ocr.py | Text-rendering OCR |
| trig_multilingual/evaluation/trig_ml_bias.py | lingt2i/evaluation/demographic_bias.py | Bias evaluation |
| trig_multilingual/evaluation/trig_ml_cultural_bias.py | lingt2i/evaluation/cultural_bias.py | Cultural evaluation |
| trig_multilingual/evaluation/trig_ml_nsfw.py | lingt2i/evaluation/nsfw.py | Safety evaluation |
| trig_multilingual/eval_ocr/ | lingt2i/evaluation/ocr_support/ | OCR implementation and dictionaries |
| trig_multilingual/AnyText* | third_party/AnyText* | Vendored baselines |
| trig_multilingual/EasyText/ | third_party/EasyText/ | Vendored baseline |
| trig_multilingual/font/ | assets/fonts/ | Font resources |
| trig_multilingual/tools/ | lingt2i/tools/ | Dataset/model utilities |
| trig/metrics/metaclip2_score.py | lingt2i/evaluation/metaclip2_score.py | Content similarity |
| trig/metrics/trig_api_ml.py | lingt2i/evaluation/trig_score.py | Multilingual TRIG score |
| trig/models/base.py | lingt2i/models/base.py | Shared model base |
| trig/models/text_to_image_models.py | lingt2i/models/text_to_image.py | Shared T2I adapters |
| config/gen.yaml | configs/content_generation.yaml | Content generation config |

Old one-off scripts that still encode legacy JSON layouts or experiment paths
are retained under lingt2i/evaluation/legacy or lingt2i/analysis. The local
rebuttal directory and Python bytecode caches were not extracted.
