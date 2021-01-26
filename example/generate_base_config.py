import json
import pandas as pd
from tqdm import tqdm
import argparse
from yolact.data.config import Config

parser = argparse.ArgumentParser(
    description='Yolact Training Script')

parser.add_argument('--train', default='dataset/train', type=str,help='Папка train датасета')
parser.add_argument('--val', default='dataset/val', type=str,help='Папка val датасета')
parser.add_argument('--out_cfg', default='dataset/cfg.json', type=str,help='Файл конфига')

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
    categories = []
    for file in tqdm(get_files(args.train, "*.json")):
        with open(file, encoding='utf-8') as io:
            coco = json.loads(io.read())

        for cat in coco['categories']:
            categories.append(cat)
    
    categories = [{'name': row['name'], 'id': int(index)} for index, row in pd.DataFrame(categories).groupby("id").first().iterrows()]

    COCO_CLASSES = tuple([cat['name'] for cat in categories])
    print(f"COCO_CLASSES = {COCO_CLASSES}")

    COCO_LABEL_MAP = {int(i+1):cat['id'] for i, cat in enumerate(categories)}
    print(f"COCO_LABEL_MAP = {COCO_LABEL_MAP}")

    out_cfg = {
        'name': 'yolact_base',

        # Dataset stuff
        'dataset': dict(Config({
            'name': 'Base Dataset',

            # Training images and annotations
            'train_images': args.train,
            'train_info':   args.train+'/all_coco.json',

            # Validation images and annotations.
            'valid_images': args.val,
            'valid_info':   args.val+'/all_coco.json',

            # Whether or not to load GT. If this is False, eval.py quantitative evaluation won't work.
            'has_gt': True,

            # A list of names for each of you classes.
            'class_names': COCO_CLASSES,

            # COCO class ids aren't sequential, so this is a bandage fix. If your ids aren't sequential,
            # provide a map from category_id -> index in class_names + 1 (the +1 is there because it's 1-indexed).
            # If not specified, this just assumes category ids start at 1 and increase sequentially.
            'label_map': COCO_LABEL_MAP
        })),
        'num_classes': len(COCO_CLASSES) + 1,

        # Image Size
        'max_size': 550,
        
        # Training params
        'lr_steps': (280000, 600000, 700000, 750000),
        'max_iter': 2000,

        # The maximum number of detections for evaluation
        'max_num_detections': 100,
    }

    with open(args.out_cfg, 'w', encoding='utf-8') as io:
        io.write(json.dumps(out_cfg))