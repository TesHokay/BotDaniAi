import math
import os
import tempfile
from typing import List

from PIL import Image, ImageOps
from aiogram import Bot


async def build_collage(bot: Bot, file_ids: List[str]) -> str:
    """Download photos by file_id, make collage and return file path."""
    tmpdir = tempfile.mkdtemp()
    paths = []
    for idx, fid in enumerate(file_ids):
        path = os.path.join(tmpdir, f"{idx}.jpg")
        await bot.download(fid, destination=path)
        paths.append(path)
    images = [Image.open(p) for p in paths]
    cols = math.ceil(math.sqrt(len(images)))
    rows = math.ceil(len(images) / cols)
    width = max(img.width for img in images)
    height = max(img.height for img in images)
    collage = Image.new("RGB", (cols * width, rows * height), color="white")
    for i, img in enumerate(images):
        img = ImageOps.contain(img, (width, height))
        x = (i % cols) * width
        y = (i // cols) * height
        collage.paste(img, (x, y))
    out_path = os.path.join(tmpdir, "collage.jpg")
    collage.save(out_path, format="JPEG")
    for p in paths:
        os.remove(p)
    return out_path
