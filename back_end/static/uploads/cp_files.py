import shutil
import os
from pathlib import Path


json_dir = "/var/www/html/dlmb.disanso.vn/static/uploads/tt4_post_process"
anno_dir = "/var/www/html/dlmb.disanso.vn/static/uploads/tt4"
json_file_path_List = list(Path(json_dir).glob("*.json"))
for index, json_file_path in enumerate(json_file_path_List):
    try:
        print(index)
        json_stem = json_file_path.stem
        json_name = json_file_path.name
        anno_file_path = Path(anno_dir) / f"{json_stem}/{json_name}"
        if os.path.isfile(anno_file_path):
            shutil.copy(json_file_path, anno_file_path)
    except Exception as e:
        print(json_file_path.name)

