import os
from PIL import Image

folder = "media/products_images"

for file in os.listdir(folder):
    path = os.path.join(folder, file)

    if not os.path.isfile(path):
        continue

    name, ext = os.path.splitext(file)

    ext = ext.lower()

    if ext in [".png", ".jpeg", ".jpg"]:

        img = Image.open(path).convert("RGB")

        new_path = os.path.join(folder, name + ".JPG")

        img.save(new_path, "JPEG", quality=90)

        if new_path != path:
            os.remove(path)

        print("✔", file, "→", name + ".jpg")
