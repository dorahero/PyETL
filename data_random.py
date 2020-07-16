import os
import random
import glob
import shutil

if not os.path.exists('yolo_data'):
    os.mkdir('yolo_data')
if not os.path.exists('yolo_data/test'):
    os.mkdir('yolo_data/test')
    os.mkdir('yolo_data/test/images')
    os.mkdir('yolo_data/test/labels')
if not os.path.exists('yolo_data/train'):
    os.mkdir('yolo_data/train')
    os.mkdir('yolo_data/train/images')
    os.mkdir('yolo_data/train/labels')
if not os.path.exists('yolo_data/valid'):
    os.mkdir('yolo_data/valid')
    os.mkdir('yolo_data/valid/images')
    os.mkdir('yolo_data/valid/labels')
count = 0

def batch_rename(path):
    global count
    path_list = glob.glob(path + '/*.jpg')
    print(path_list)
    for fname in path_list:
        new_jname = str(count) + '.jpg'
        new_tname = str(count) + '.txt'
        # print(os.path.join(path, fname))
        os.rename(fname, os.path.join(path, new_jname))
        os.rename('.' + fname.split('.')[1] + '.txt', os.path.join(path, new_tname))
        # print(fname.split('.')[1])
        count = count + 1
def data_label(path):
    length = len(path)//5
    for i, p in enumerate(path):
        if i < length*3:
            shutil.move(p, './yolo_data/train/images')
            shutil.move('.' + p.split('.')[1] + '.txt', './yolo_data/train/labels')
        elif i < length*4:
            shutil.move(p, './yolo_data/test/images')
            shutil.move('.' + p.split('.')[1] + '.txt', './yolo_data/test/labels')
        else:
            shutil.move(p, './yolo_data/valid/images')
            shutil.move('.' + p.split('.')[1] + '.txt', './yolo_data/valid/labels')

test = glob.glob('./data_original/*/*.txt')
for t in test:
    print(t)
    with open(t, 'r', encoding='utf-8') as f:
        cont = f.read()
    print(cont)
    if len(cont) == 0:
        os.remove(t)
        os.remove('.' + t.split('.')[1] + '.jpg')
p_list = glob.glob('./data_original/*')
# print(p_list)
for path in p_list:
    batch_rename(path)
with open('./logcount.txt', 'w', encoding='utf-8') as f:
    f.write(str(count))
all_list = glob.glob('./data_original/*/*.jpg')
random.shuffle(all_list)
# print(all_list)
# print(len(all_list)//5)
data_label(all_list)

