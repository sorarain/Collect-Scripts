import sys
import os
sys.path.append("/root/RouteGraph")
sys.path.append(os.path.join(os.path.abspath("."),"build"))
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import torch
import numpy as np
import time
import tqdm
import logging
import json

import dreamplace.configure as configure
import Params
import PlaceDB
import NonLinearPlace
import Timer
PARAM_PATH = 'test/'
DATASET_NAME = "dac2012"
RESULTS_DIR = 'results'

logging.root.name = 'DREAMPlace'
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)-7s] %(name)s - %(message)s',
                    stream=sys.stdout)

netlist_names = [
    # 'superblue1',
    # 'superblue2',
    # 'superblue3',
    # 'superblue4',
    # 'superblue5',
    # 'superblue6',
    # 'superblue7',
    # 'superblue9',
    # 'superblue10',#fail
    # 'superblue11',
    # 'superblue12',
    # 'superblue14',
    # 'superblue15',
    # 'superblue16',
    # 'superblue18',
    'superblue19',
]


d = []

for netlist_name in netlist_names:
    param_path = os.path.join(PARAM_PATH, DATASET_NAME, f"{netlist_name}.json")
    params = Params.Params()
    params.load(param_path)

    params.__dict__["timing_opt_flag"] = 0

    params.__dict__["congestion predict epoch"] = 100000
    params.__dict__["routability_opt_flag"] = 1
    params.__dict__["collect"] = 1
    params.__dict__["adjust_nctugr_area_flag"] = 1
    placedb = PlaceDB.PlaceDB()
    placedb(params)
    timer = None
    print(f"init placer")
    placer = NonLinearPlace.NonLinearPlace(params, placedb, timer)

    metrics = placer(params, placedb)

    SAVE_DIR = "./collect"
    common_dir = os.path.join(SAVE_DIR,params.design_name(),"common")
    with open(os.path.join(common_dir,"route_info.json"),"w") as f:
        xl=placedb.routing_grid_xl
        yl=placedb.routing_grid_yl
        xh=placedb.routing_grid_xh
        yh=placedb.routing_grid_yh
        num_bins_x=placedb.num_routing_grids_x
        num_bins_y=placedb.num_routing_grids_y
        bin_size_x = (xh - xl) / num_bins_x
        bin_size_y = (yh - yl) / num_bins_y
        json.dump({"xl":xl,
                    "yl":yl,
                    "xh":xh,
                    "yh":yh,
                    "num_bins_x":num_bins_x,
                    "num_bins_y":num_bins_y,
                    "bin_size_x":bin_size_x,
                    "bin_size_y":bin_size_y,},f)
    with open(os.path.join(common_dir,"layout_info.json"),"w") as f:
        xl=placedb.xl
        yl=placedb.yl
        xh=placedb.xh
        yh=placedb.yh
        num_bins_x=placedb.num_bins_x
        num_bins_y=placedb.num_bins_y
        bin_size_x = placedb.bin_size_x
        bin_size_y = placedb.bin_size_y
        json.dump({"xl":xl,
                    "yl":yl,
                    "xh":xh,
                    "yh":yh,
                    "num_bins_x":num_bins_x,
                    "num_bins_y":num_bins_y,
                    "bin_size_x":bin_size_x,
                    "bin_size_y":bin_size_y,},f)
