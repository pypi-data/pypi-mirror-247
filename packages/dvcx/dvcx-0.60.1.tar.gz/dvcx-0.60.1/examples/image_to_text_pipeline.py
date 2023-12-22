# pip install Pillow
# pip install transformers
# pip install torch
#
# HuggingFace pipeline example (one sample at a time)
# for pure transformers example in faster batch mode see blip2_image_desc.py
#

import re

import torch
from PIL import Image, UnidentifiedImageError
from transformers import pipeline

from dql.query import C, DatasetQuery, Object, udf
from dql.sql.types import String

# HuggingFace pipeline for captioning was tested on these models:

model = (
    "Salesforce/blip2-opt-2.7b"  # (medium, medium quality) - supports cuda, cpu, mps
)
# model = "Salesforce/blip-image-captioning-base" # (fast, low quality) - cuda, cpu, mps

# LLAVA models need prompt, e.g. : "USER: <image>\nDescribe this picture\nASSISTANT:"
# llava_prompt = "USER: <image>\nDescribe this picture\nASSISTANT:"
# model = "llava-hf/llava-1.5-7b-hf"   # (slow, high quality) - supports cuda, gpu
# model = "llava-hf/bakLlava-v1-hf"    # (slow, high quality) - supports cuda, cpu

source = "s3://ldb-public/remote/data-lakes/dogs-and-cats/"


def load_image(raw):
    try:
        img = Image.open(raw)
        img.load()
        # preserve native resolutions or resize:
        # img = ImageOps.fit(img, (500, 500))
    except UnidentifiedImageError:
        return None
    return img


@udf(
    params=(Object(load_image),),  # Columns consumed by the UDF.
    output={
        "desc": String,
        "error": String,
    },  # Signals being returned by the UDF.
    method="describe",
)
class PIPEdescribe:
    def __init__(self, model=None, device="cpu", max_new_tokens=200, prompt=None):
        self.pipe = pipeline("image-to-text", model=model, device=device)
        self.max_new_tokens = max_new_tokens
        self.prompt = prompt

    def describe(self, img):
        if img is None:
            return ("", "Image format not recognized")

        outputs = self.pipe(
            img,
            prompt=self.prompt,
            generate_kwargs={"max_new_tokens": self.max_new_tokens},
        )
        desc = re.sub(
            "^.*ASSISTANT: ", "", outputs[0]["generated_text"], flags=re.DOTALL
        )
        return (desc.strip(), "")


if __name__ == "__main__":
    if torch.backends.mps.is_available():
        device = "mps"
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    results = (
        DatasetQuery(
            source,
            client_config={"aws_anon": True},
        )
        .filter(C.name.glob("cat*.jpg"))
        .limit(1)
        .add_signals(
            PIPEdescribe(device="cpu", model=model, prompt=None), processes=False
        )
        .select("source", "parent", "name", "desc", "error")
        .results()
    )
    print(*results, sep="\n")
