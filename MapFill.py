import numpy as np
from matplotlib import pyplot as plt
import yaml, csv
from PIL import Image 
import sys



class MapFiller:
    def __init__(self, map_name):
        self.map_name = map_name

        self.resolution = None
        self.origin = None
        self.map_img = None
        self.map_height = None
        self.map_width = None

        self.load_map()

    def load_map(self):
        file_name = 'maps/' + self.map_name + '.yaml'
        with open(file_name) as file:
            documents = yaml.full_load(file)
            yaml_file = dict(documents.items())

        try:
            self.resolution = yaml_file['resolution']
            self.origin = yaml_file['origin']
            map_img_path = 'maps/' + yaml_file['image']
        except Exception as e:
            print(f"Problem loading, check key: {e}")
            raise FileNotFoundError("Problem loading map yaml file")

        self.map_img = np.array(Image.open(map_img_path).transpose(Image.FLIP_TOP_BOTTOM))
        self.map_img = self.map_img.astype(np.float64)
        if len(self.map_img.shape) == 3:
            self.map_img = self.map_img[:, :, 0]

        self.map_img[self.map_img <= 128.] = 1.
        self.map_img[self.map_img > 128.] = 0.

        crop_x = [50, 375]
        crop_y = [200, 320]
        self.map_img = self.map_img.T
        self.map_img = self.map_img[crop_x[0]:crop_x[1], crop_y[0]:crop_y[1]]

        self.map_height = self.map_img.shape[0]
        self.map_width = self.map_img.shape[1]

        self.map_img = boundary_fill(self.map_img, 0, 0)
        self.map_img = boundary_fill(self.map_img, 76, 65)

        
        self.map_img[self.map_img == 0] = 255
        self.map_img[self.map_img < 128] = 0
        img = Image.fromarray(self.map_img.T.astype(np.uint8)).transpose(Image.FLIP_TOP_BOTTOM)
        img.save('maps/' + self.map_name + '_filled.png')

        plt.figure(1)
        plt.imshow(self.map_img.T, origin='lower')

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


if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    map_filler = MapFiller('porto')
