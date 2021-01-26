import json
import pandas as pd
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(
    description='Yolact Training Script')

parser.add_argument('--dataset', default='dataset', type=str,help='Папка датасета')
parser.add_argument('--out_file', default='all_coco.json', type=str,help='Папка датасета')

parser.set_defaults(keep_latest=False, log=True, log_gpu=False, interrupt=True, autoscale=True)
args = parser.parse_args()


def get_files(path, extensions):
    from pathlib import Path
    if type(extensions) is str:
        extensions = [extensions]
    
    all_files = []
    for ext in extensions:
        all_files.extend(Path(path).rglob(ext))
        
    for i in range(len(all_files)):
        all_files[i] = str(all_files[i])
        
    return all_files


if __name__ == '__main__':
    all_coco = {'info': {'year': 2021,
    'version': '1.0',
    'description': 'build with build_coco_from_mask function',
    'contributor': 'MiXaiLL76',
    'url': 'https://t.me/mixaill76',
    'date_created': '2021-01-06 16:22:20'},
    'images': [],
    'annotations': [],
    'licenses': [{'id': 1, 'name': 'Unknown', 'url': ''}],
    'categories': [],
    }

    categories = []
    for file in tqdm(get_files(args.dataset, "*.json")):
        with open(file, encoding='utf-8') as io:
            coco = json.loads(io.read())
            
        img_old = {}
        for img in coco['images']:
            img_id = len(all_coco['images'])+1
            img_old[int(img['id'])] = img_id
            
            img.update({"id":img_id})
            
            all_coco['images'].append(img)
        
        for ann in coco['annotations']:
            ann.update({
                "image_id":img_old[int(ann['image_id'])],
                "id"      : len(all_coco['annotations']) + 1,
    #             "segmentation" : [ann['segmentation']],
    #             "category_id" : 1
            })
            all_coco['annotations'].append(ann)
            
        for cat in coco['categories']:
            categories.append(cat)
            
        
    all_coco['categories'] = [{'name': row['name'], 'id': int(index)} for index, row in pd.DataFrame(categories).groupby("id").first().iterrows()]

    with open(args.out_file, 'w') as io:
        io.write(json.dumps(all_coco))