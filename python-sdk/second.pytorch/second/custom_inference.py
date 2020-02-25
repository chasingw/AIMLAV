import numpy as np
import matplotlib.pyplot as plt
import pickle
from pathlib import Path
import random
import matplotlib.image as mpimg

import torch
from google.protobuf import text_format
from second.utils import simplevis
from second.pytorch.train import build_network
from second.protos import pipeline_pb2
from second.utils import config_tool

def read_config_file(config_path):
    config = pipeline_pb2.TrainEvalPipelineConfig()
    with open(config_path, "r") as f:
        proto_str = f.read()
        text_format.Merge(proto_str, config)
    input_cfg = config.eval_input_reader
    model_cfg = config.model.second
    # added a new method to fix error
    config_tool.change_detection_range_v2(model_cfg, [-50, -50, 50, 50])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return input_cfg, model_cfg, device



def build_net_v2(ckpt_path, model_cfg, device):
#     returns the targer assigner, voxel generator
    net = build_network(model_cfg).to(device).eval()
    net.load_state_dict(torch.load(ckpt_path))
    return net.target_assigner, net.voxel_generator, device, net



def generate_anchors(voxel_generator, target_assigner, model_cfg, device):    
    grid_size = voxel_generator.grid_size
    feature_map_size = grid_size[:2] // config_tool.get_downsample_factor(model_cfg)
    feature_map_size = [*feature_map_size, 1][::-1]
    
    anchors = target_assigner.generate_anchors(feature_map_size)["anchors"]
    anchors = torch.tensor(anchors, dtype=torch.float32, device=device)
    anchors = anchors.view(1, -1, 7)
    
    return anchors

def read_kitti_info_file(input_cfg):    
    info_path = input_cfg.dataset.kitti_info_path
    root_path = Path(input_cfg.dataset.kitti_root_path)
    with open(info_path, 'rb') as f:
        infos = pickle.load(f)
    return infos, root_path

def load_point_cloud(infos, info_index, root_path):
    info = infos['infos'][info_index]
    v_path = info["lidar_path"]
    v_path = str(root_path / v_path)
    points = np.fromfile(v_path, dtype=np.float32, count=-1).reshape([-1, 4])
    return points, info
    

def voxel_generator_v2(points, voxel_generator, device):    
    voxel_gen = voxel_generator.generate(points, max_voxels=90000)
    voxels = voxel_gen['voxels'] 
    coords = voxel_gen['coordinates']
    num_points = voxel_gen['num_points_per_voxel']
    voxel_point_mask =  voxel_gen['voxel_point_mask']
    voxel_num = voxel_gen['voxel_num']
    
    # add batch idx to coords
    coords = np.pad(coords, ((0, 0), (1, 0)), mode='constant', constant_values=0)
    voxels = torch.tensor(voxels, dtype=torch.float32, device=device)
    coords = torch.tensor(coords, dtype=torch.int32, device=device)
    num_points = torch.tensor(num_points, dtype=torch.int32, device=device)
    
    return coords, voxels, num_points



def detection_v2(anchors, voxels, num_points, coords, net):
    example = {
        "anchors": anchors,
        "voxels": voxels,
        "num_points": num_points,
        "coordinates": coords
    }
    return net(example)[0]


def visualize(pred, points, vis_voxel_size=[0.1, 0.1, 0.1], vis_point_range=[-50, -30, -3, 50, 30, 1]):    
    boxes_lidar = pred["box3d_lidar"].detach().cpu().numpy()
    bev_map = simplevis.point_to_vis_bev(points, vis_voxel_size, vis_point_range)
    bev_map = simplevis.draw_box_in_bev(bev_map, vis_point_range, boxes_lidar, [0, 255, 0], 2)
    return bev_map


def infer(config_path, ckpt_path, point_cloud_key):
    input_cfg, model_cfg, device = read_config_file(config_path)
    target_assigner, voxel_generator, device, net = build_net_v2(ckpt_path, model_cfg, device)
    anchors = generate_anchors(voxel_generator, target_assigner, model_cfg, device)
    infos, root_path = read_kitti_info_file(input_cfg)  
    points, info = load_point_cloud(infos, point_cloud_key, root_path)
    coords, voxels, num_points = voxel_generator_v2(points, voxel_generator, device)
    pred = detection_v2(anchors, voxels, num_points, coords, net)
    bev_map = visualize(pred, points)
    return bev_map, info


def random_pointcloud_ids_list(max = 5):
    # max: the number of random numbers you want
    #
    #
    # generate :max random numbers in the range of of 0 - 5000
    random_pointcloud_ids = []
    for i in range(0, max):
        random_pointcloud_ids.append(random.randrange(0, 5000)) # find the max id number
    return random_pointcloud_ids

def plot_random_pointclouds(model_path, checkpoint, number_of_pointclouds):
    point_cloud_ids = random_pointcloud_ids_list(number_of_pointclouds);
    # plot the pointcloud and the image side by side
    for i in point_cloud_ids:
        plot_single_pointcloud(model_path, ckpt_path, i)
    return point_cloud_ids

def plot_single_pointcloud(model_path, ckpt_path, point_cloud_index):
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
    bev_map, info = infer(model_path+'/pipeline.config', ckpt_path, point_cloud_key=point_cloud_index)
    ax1.imshow(bev_map)
    img = mpimg.imread(info['cam_front_path'])
    ax2.imshow(img)
    plt.show()