import numpy as np
from matplotlib import pyplot as plt
import yaml, csv
from PIL import Image 
import sys



def MapFiller(map_name, pts, crop_x, crop_y):

    file_name = 'maps/' + map_name + '.yaml'
    with open(file_name) as file:
        documents = yaml.full_load(file)
        yaml_file = dict(documents.items())

    try:
        resolution = yaml_file['resolution']
        origin = yaml_file['origin']
        map_img_path = 'maps/' + yaml_file['image']
    except Exception as e:
        print(f"Problem loading, check key: {e}")
        raise FileNotFoundError("Problem loading map yaml file")

    map_img = np.array(Image.open(map_img_path).transpose(Image.FLIP_TOP_BOTTOM))
    map_img = map_img.astype(np.float64)
    if len(map_img.shape) == 3:
        map_img = map_img[:, :, 0]

    map_img[map_img <= 128.] = 1.
    map_img[map_img > 128.] = 0.


    map_img = map_img.T
    map_img = map_img[crop_x[0]:crop_x[1], crop_y[0]:crop_y[1]]

    for pt in pts:
        map_img = boundary_fill(map_img, pt[0], pt[1])
    
    map_img[map_img == 0] = 255
    map_img[map_img < 128] = 0
    img = Image.fromarray(map_img.T.astype(np.uint8)).transpose(Image.FLIP_TOP_BOTTOM)

    img.save('maps/' + map_name + '_filled.png')

    plt.figure(1)
    plt.imshow(map_img.T, origin='lower')

    plt.show()

def view_map(map_name):
    file_name = 'maps/' + map_name + '.yaml'
    with open(file_name) as file:
        documents = yaml.full_load(file)
        yaml_file = dict(documents.items())
    map_img_path = 'maps/' + yaml_file['image']
    map_img = np.array(Image.open(map_img_path).transpose(Image.FLIP_TOP_BOTTOM))
    map_img = map_img.astype(np.float64)
    if len(map_img.shape) == 3:
        map_img = map_img[:, :, 0]

    map_img[map_img <= 128.] = 1.
    map_img[map_img > 128.] = 0.

    plt.figure(1)
    plt.imshow(map_img, origin='lower')

    plt.show()


def boundary_fill(map_img, i, j, fill=2, boundary=1):
    if map_img[i, j] != boundary and map_img[i, j] != fill:
        map_img[i, j] = fill
        if i > 0:
            boundary_fill(map_img, i - 1, j, fill, boundary)
        if i < map_img.shape[0] - 1:
            boundary_fill(map_img, i + 1, j, fill, boundary)
        if j > 0:
            boundary_fill(map_img, i, j - 1, fill, boundary)
        if j < map_img.shape[1] - 1:
            boundary_fill(map_img, i, j + 1, fill, boundary)

    return map_img

def run_porto():
    crop_x = [50, 375]
    crop_y = [200, 320]
    pts = [[0, 0],
            [76, 65]]

    MapFiller('porto', pts, crop_x, crop_y)

def run_torino():
    view_map("torino")
    crop_y = [120, 580]
    crop_x = [230, 460]
    pts = [[0, 0]]

    MapFiller('torino', pts, crop_x, crop_y)


def run_berlin():
    view_map("berlin")

    crop_x = [80, 490]
    crop_y = [0, -1]
    pts = [[0, 0]]

    MapFiller('berlin', pts, crop_x, crop_y)


if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    # run_porto()
    # run_torino()
    run_berlin()

