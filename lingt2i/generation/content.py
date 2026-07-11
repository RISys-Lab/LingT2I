"""Shared TRIG generation flow specialized for LingT2I content prompts."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import requests
import yaml
from datasets import load_dataset
from tqdm import tqdm

from lingt2i.data import CONTENT_GENERATION_SPLIT, DEFAULT_DATASET
from lingt2i.models import import_model


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class ContentGenerator:
    """Generate the LingT2I content_generation split with one model."""

    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        with self.config_path.open("r", encoding="utf-8") as handle:
            self.config = yaml.safe_load(handle)

        self.dataset_name = self.config.get("dataset_name", DEFAULT_DATASET)
        self.split = self.config.get("split", CONTENT_GENERATION_SPLIT)
        self.start_idx = self.config.get("start_idx", 0) or 0
        self.end_idx = self.config.get("end_idx")
        self.model_names = self.config["generation"]["models"]
        self.output_root = Path(
            self.config.get("output_dir", PROJECT_ROOT / "outputs" / self.split)
        )

    def load_prompts(self):
        dataset = load_dataset(self.dataset_name, split=self.split)
        end_idx = len(dataset) if self.end_idx is None else min(self.end_idx, len(dataset))
        return dataset.select(range(self.start_idx, end_idx))

    @staticmethod
    def save_image(image: Any, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(image, str):
            response = requests.get(image, timeout=60)
            response.raise_for_status()
            output_path.write_bytes(response.content)
        else:
            image.save(output_path)

    def generate(self) -> None:
        prompts = self.load_prompts()
        for model_name in self.model_names:
            model = import_model(model_name)()
            model_output = self.output_root / model_name
            existing = {path.stem for path in model_output.glob("*.png")}

            for sample in tqdm(prompts, desc=model_name):
                data_id = str(sample["data_id"])
                if data_id in existing:
                    continue
                image = model.generate(sample["prompt"])
                self.save_image(image, model_output / f"{data_id}.png")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default=str(PROJECT_ROOT / "configs" / "content_generation.yaml"),
    )
    args = parser.parse_args()
    ContentGenerator(args.config).generate()


if __name__ == "__main__":
    main()
