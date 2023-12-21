# pip install Pillow
# pip install transformers
#
# This example uses pure transformers syntax for batching
# For a simpler pipeline example, see image_to_text_pipeline.py
#

import numpy
import torch
from PIL import Image, ImageOps, UnidentifiedImageError
from transformers import Blip2ForConditionalGeneration, Blip2Processor

from dql.query import C, DatasetQuery, Object, udf
from dql.sql.types import String

model = "Salesforce/blip2-opt-2.7b"
source = "s3://ldb-public/remote/data-lakes/dogs-and-cats/"

if torch.backends.mps.is_available():
    device = "mps"
elif torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"


def load_image(raw):
    try:
        img = Image.open(raw)
        img.load()
        img = ImageOps.fit(img, (500, 500))
    except UnidentifiedImageError:
        return None
    return img


@udf(
    params=(Object(load_image),),  # Columns consumed by the UDF.
    output={
        "desc": String,
        "error": String,
    },  # Signals being returned by the UDF.
    batch=64,
    method="describe",
)
class BLIP2describe:
    def __init__(self):
        self.processor = Blip2Processor.from_pretrained(model)
        self.model = Blip2ForConditionalGeneration.from_pretrained(
            model, torch_dtype=torch.float16
        )

        self.model.to(device)

    def describe(self, imgs):
        images = numpy.squeeze(numpy.asarray(imgs))
        inputs = self.processor(images=images, return_tensors="pt").to(
            device, torch.float16
        )

        generated_ids = self.model.generate(**inputs, max_new_tokens=300)
        generated_text = self.processor.batch_decode(
            generated_ids, skip_special_tokens=True
        )
        return [(desc.strip(), "") for desc in generated_text]


if __name__ == "__main__":
    results = (
        DatasetQuery(
            source,
            client_config={"aws_anon": True},
        )
        .filter(C.name.glob("cat*.jpg"))
        .limit(100)
        .add_signals(BLIP2describe, processes=False)
        .select("source", "parent", "name", "desc", "error")
        .results()
    )
    print(*results, sep="\n")
