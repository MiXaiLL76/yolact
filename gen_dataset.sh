#/bin/bash


python3 example/generate_dataset.py --count 50 --dataset dataset/train
python3 example/generate_one_dataset_file.py --dataset dataset/train --out_file dataset/train/all_coco.json

python3 example/generate_dataset.py --count 10 --dataset dataset/val
python3 example/generate_one_dataset_file.py --dataset dataset/val --out_file dataset/val/all_coco.json
