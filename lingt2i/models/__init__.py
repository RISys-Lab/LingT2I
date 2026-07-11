"""Text-to-image model registry copied from the shared TRIG infrastructure."""

import importlib

from .base import BaseModel


AVAILABLE_MODELS = {
    "base": "base.BaseModel",
    "dalle3": "text_to_image.DALLE3Model",
    "sdxl": "text_to_image.SDXLModel",
    "sd15": "text_to_image.SD15Model",
    "pixart_sigma": "text_to_image.PixartSigmaModel",
    "sana": "text_to_image.SanaModel",
    "sd35": "text_to_image.SD35Model",
    "flux": "text_to_image.FLUXModel",
    "zimage": "text_to_image.ZImageModel",
    "janus": "text_to_image.JanusProModel",
    "janus_flow": "text_to_image.JanusFlowModel",
    "qwen_image": "text_to_image.QwenImageModel",
    "hunyuan": "text_to_image.HunyuanModel",
    "altdiffusion": "text_to_image.AltDiffusionModel",
    "peadiffusion": "text_to_image.PEADiffusionModel",
    "mulan": "text_to_image.MuLanModel",
    "x2i": "text_to_image.X2IModel",
}


def import_model(model_name: str):
    """Resolve a LingT2I content-generation model by its config name."""
    if model_name not in AVAILABLE_MODELS:
        available = ", ".join(sorted(AVAILABLE_MODELS))
        raise ValueError(f"Unknown model {model_name!r}. Available models: {available}")

    module_name, class_name = AVAILABLE_MODELS[model_name].rsplit(".", 1)
    module = importlib.import_module(f"{__name__}.{module_name}")
    return getattr(module, class_name)


__all__ = ["AVAILABLE_MODELS", "BaseModel", "import_model"]
