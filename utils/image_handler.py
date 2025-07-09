import os
import pandas as pd
from duckduckgo_search import ddg_images
from PIL import Image
from rembg import remove
import requests
from io import BytesIO
import zipfile

def process_csv_and_images(csv_path):
    df = pd.read_csv(csv_path)
    output_dir = "/tmp/plant_images"
    os.makedirs(output_dir, exist_ok=True)

    for index, row in df.iterrows():
        name = str(row['Название']).strip()
        results = ddg_images(f"{name} растение в горшке", max_results=5)

        for res in results:
            try:
                response = requests.get(res["image"], timeout=10)
                image = Image.open(BytesIO(response.content))
                if image.width >= 1000 and image.height >= 1000:
                    no_bg = remove(image)
                    plant_dir = os.path.join(output_dir, name.replace(" ", "_"))
                    os.makedirs(plant_dir, exist_ok=True)
                    img_path = os.path.join(plant_dir, f"{name.replace(' ', '_')}.png")
                    no_bg.save(img_path)
                    break
            except Exception:
                continue

    archive_path = "/tmp/plant_archive.zip"
    with zipfile.ZipFile(archive_path, 'w') as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, output_dir)
                zipf.write(full_path, arcname)

    return archive_path
