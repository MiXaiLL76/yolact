import argparse
import numpy as np
import cv2
from PIL import Image
import os
import uuid
import json
from tqdm import tqdm

parser = argparse.ArgumentParser(
    description='Yolact Training Script')
parser.add_argument('--W', default=550, type=int, help='W')
parser.add_argument('--H', default=550, type=int, help='W')
parser.add_argument('--count', default=25, type=int, help='кол-во файлов')

parser.add_argument('--dataset', default='dataset', type=str,help='Папка датасета')

parser.set_defaults(keep_latest=False, log=True, log_gpu=False, interrupt=True, autoscale=True)
args = parser.parse_args()


if __name__ == '__main__':
    W = args.W
    H = args.H
    dataset_dir = args.dataset
    dataset_count = args.count



    os.makedirs(dataset_dir, exist_ok=True)

    min_wh  = min([W,H]) // 7
    max_wh  = min([W,H]) // 5
    max_pos = min([W,H])

    for img_id in tqdm(range(dataset_count)):
        bg = (np.sin(np.random.rand(H,W,3))*256).astype(np.uint8)

        empty_bg = np.zeros((H,W)).astype(np.uint8)
        annotations = []

        i = 0
        while i < int(np.random.rand(1)[0] * 5) + 1:
            cx, cy  = np.int0(np.random.rand(2)*max_pos)
            r       = np.int0(np.random.rand(1)*(max_wh-min_wh))[0] + min_wh
            h,w = r*2,r*2

            rect = np.int0([cy-h//2, cy+h//2, cx-w//2, cx+w//2])
            rect[rect < 0] = 0
            rect[rect >= min([W,H])] = min([W,H])-1
            a,b,c,d = rect
            if empty_bg[a:b, c:d].max() != 0:
                continue

            i += 1

            img = np.zeros((H,W)).astype(np.uint8)

            if np.random.rand(1)[0] > 0.5:
                category_id = 1
                cv2.circle(img,(cx,cy),r,255,-1)
                cv2.circle(empty_bg,(cx,cy),r,255,-1)
            else:
                category_id = 2
                cv2.rectangle(img, (cx-w//2, cy-h//2, w, h), 255, -1)
                cv2.rectangle(empty_bg, (cx-w//2, cy-h//2, w, h), 255, -1)

            contours,_ = cv2.findContours(img, 1, 2)
            cnt = contours[0]
            area = int(cv2.contourArea(cnt))
            segmentation = [[int(x) for x in cnt.ravel().tolist()]]
            x,y,w,h = cv2.boundingRect(cnt)

            annotations.append({
                'segmentation': segmentation,
                'area': area,
                'bbox': [int(x), int(y), int(w), int(h)],
                'iscrowd': 0,
                'id': len(annotations)+1,
                'image_id': 1,
                'category_id': category_id
            })

        for ann in annotations:
            color = tuple ([int(x*255) for x in np.random.rand(3)])
            cv2.drawContours(bg,[np.array(ann['segmentation']).reshape(-1,1,2)],0,color,-1)

        name = str(uuid.uuid1()).split('-')[0]
        all_coco = {'info': {'year': 2021,
        'version': '1.0',
        'description': 'build with dataset_builder',
        'contributor': 'MiXaiLL76',
        'url': 'https://t.me/mixaill76',
        'date_created': '2021-01-06 16:22:20'},
        'images': [{
                "id": 1,
                "width": W,
                "height": H,
                "file_name": f"{name}.png",
                "license": 1,
                "date_captured": "",
            }],
        'annotations': annotations,
        'licenses': [{'id': 1, 'name': 'Unknown', 'url': ''}],
        'categories': [{'name': 'circle', 'id': 1}, {'name': 'box', 'id': 2}]
        }
        
        Image.fromarray(bg).save(os.path.join(dataset_dir, f"{name}.png"), "PNG")
        with open(os.path.join(dataset_dir, f"{name}_coco.json"), 'w', encoding='utf-8') as io:
            io.write(json.dumps(all_coco))
