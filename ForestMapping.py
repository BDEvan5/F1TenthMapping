import yaml 
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image
import csv
import casadi as ca 
from scipy import ndimage 
import io

import toy_auto_race.Utils.LibFunctions as lib


class ForestPreMap:
    def __init__(self, map_name, sim_conf):
        self.map_name = map_name
        self.max_v = sim_conf.max_v

        self.wpts = None
        self.vs = None 

        self.cline = None 
        self.nvecs = None 
        self.widths = None   

    def run_generation(self):
        self.load_yaml_file()
        self.generate_pts()
        self.save_map_std()
        self.save_map_opti()


    def load_yaml_file(self):
        file_name = 'maps/' + self.map_name + '.yaml'
        with open(file_name) as file:
            documents = yaml.full_load(file)
            yaml_file = dict(documents.items())

        try:
            self.resolution = yaml_file['resolution']
            self.n_obs = yaml_file['n_obs']
            self.obs_size = yaml_file['obs_size']
            self.start_pose = np.array(yaml_file['start_pose'])
            self.forest_length = yaml_file['forest_length']
            self.forest_width = yaml_file['forest_width']
            self.obstacle_buffer = yaml_file['obstacle_buffer']
            self.end_y = yaml_file['end_y']
        except Exception as e:
            print(e)
            raise io.FileIO("Problem loading map yaml file")

    def generate_pts(self):
        """
        Generates the points required for the files
        """
        n_pts = 50
        ys = np.linspace(self.start_pose[1], self.end_y, n_pts)
        xs = np.ones_like(ys) * self.start_pose[0]
        self.cline = np.concatenate([xs[:, None], ys[:, None]], axis=-1)

        self.widths = np.ones_like(self.cline) * self.forest_width / 2
        ones =  np.ones_like(xs)
        zeros = np.ones_like(ys)
        self.nvecs = np.concatenate([ones[:, None], zeros[:, None]], axis=-1)

        self.wpts = np.copy(self.cline)
        self.vs = self.max_v * np.ones_like(xs)

    def save_map_std(self):
        filename = 'maps/' + self.map_name + '_std.csv'

        track = np.concatenate([self.cline, self.nvecs, self.widths], axis=-1)

        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(track)

        print(f"Track Saved in File: {filename}")

    def save_map_opti(self):
        filename = 'maps/' + self.map_name + '_opti.csv'

        dss, ths = convert_pts_s_th(self.wpts)
        ss = np.cumsum(dss)
        # ss = np.insert(ss, 0, 0)
        ks = np.zeros_like(ths[:, None]) #TODO: add the curvature

        track = np.concatenate([ss[:, None], self.wpts[:-1], ths[:, None], ks, self.vs[:-1, None]], axis=-1)

        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(track)

        print(f"Track Saved in File: {filename}")



def run_forest_gen():
    fname = "config_test"
    sim_conf = lib.load_conf(fname)
    map_name = "forest2"

    pre_map = ForestPreMap(map_name, sim_conf)
    pre_map.run_generation()


def make_forest_img():
    length = 25
    width = 2
    resolution = 0.05
    name = "forest2.pgm"

    border = 20

    w = int(width / resolution) + 2 * border
    l = int(length / resolution) + 2 * border

    img = np.ones((l, w), dtype=np.uint8) * 255
    img[0:border, :] = 0
    img[-border:, :] = 0
    img[:, 0:border] = 0
    img[:, -border:] = 0

    img = Image.fromarray(img)
    img.save(name)



if __name__ == "__main__":
    run_pre_map()
    # run_forest_gen()

    # make_forest_img()
