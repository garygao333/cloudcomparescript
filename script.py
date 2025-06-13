import cloudComPy as cc  
import json
import numpy as np
import scipy
import requests
import matplotlib
import os

json_filepath = "example.json"

with open(json_filepath, "r") as f:
    job_data = json.load(f)

desktop_path = os.path.expanduser("~/Desktop/mesh")
output_path = os.path.expanduser("~/Desktop/cloudcomparescript/Data")

os.makedirs(output_path, exist_ok=True)

def load_mesh(job_id):
    desktop_path = os.path.expanduser("~/Desktop/mesh")
    ply_file_path = os.path.join(desktop_path, f"{job_id}.ply")
    mesh = cc.loadMesh(ply_file_path)
    mesh.setName(job_id)
    print(mesh.getName())
    return mesh

def sample_mesh(mesh, density=20000):
    cloud = mesh.samplePoints(densityBased=True, samplingParameter=density, withNormals=True)
    cloud.setName(mesh.getName())
    return cloud

def save_cloud(cloud, type=""):
    name = f"{cloud.getName()}_{type}" if type else cloud.getName()
    save_path = os.path.join(output_path, f"{name}.las")
    res = cc.SavePointCloud(cloud, save_path) 
    return save_path

def compute_bidirectional_distances(cloud1, cloud2):
    cloud1_copy = cloud1.cloneThis()
    cloud2_copy = cloud2.cloneThis()
    cc.DistanceComputationTools.computeApproxCloud2CloudDistance(cloud1_copy, cloud2 )
    cc.DistanceComputationTools.computeApproxCloud2CloudDistance(cloud2_copy,cloud1)
    return cloud1_copy, cloud2_copy

def filter_high_distance(cloud, threshold=0.01):
    sf_index = cloud.getNumberOfScalarFields() - 1  
    cloud.setCurrentOutScalarField(sf_index)
    filtered = cc.filterBySFValue(threshold, float("inf"), cloud)
    if filtered and filtered.size() > 0:
        filtered.setName(cloud.getName() + "_filtered")
        result = cc.ExtractConnectedComponents(clouds=[filtered], octreeLevel=7,randomColors=False)
        components = result[1]
        if components:
            return components
    return []

def get_bounding_box(cloud):
    bbox = cloud.getOwnBB()
    bb_min = bbox.minCorner()
    bb_max = bbox.maxCorner()
    return bb_min, bb_max


def clouds_overlap_spatially(cloud1, cloud2, tolerance=0.05):
    bb1_min, bb1_max = get_bounding_box(cloud1)
    bb2_min, bb2_max = get_bounding_box(cloud2)
    overlap_x = not (bb1_max[0] + tolerance < bb2_min[0] or bb2_max[0] + tolerance < bb1_min[0])
    overlap_y = not (bb1_max[1] + tolerance < bb2_min[1] or bb2_max[1] + tolerance < bb1_min[1])
    overlap_z = not (bb1_max[2] + tolerance < bb2_min[2] or bb2_max[2] + tolerance < bb1_min[2])
    return overlap_x and overlap_y and overlap_z

for job in job_data:
    top_id = job["top"]
    bottom_id = job["bottom"]

    top_mesh = load_mesh(top_id)
    bottom_mesh = load_mesh(bottom_id)
    top_cloud = sample_mesh(top_mesh)
    bottom_cloud = sample_mesh(bottom_mesh)

    save_cloud(top_cloud, "raw")
    save_cloud(bottom_cloud, "raw")

    top_with_dist, bottom_with_dist = compute_bidirectional_distances(top_cloud, bottom_cloud)
    top_components = filter_high_distance(top_with_dist, threshold=0.01)
    bottom_components = filter_high_distance(bottom_with_dist, threshold=0.01)

    matched_pairs = []
    for i, top_comp in enumerate(top_components):
        for j, bottom_comp in enumerate(bottom_components):
            if clouds_overlap_spatially(top_comp, bottom_comp):
                matched_pairs.append((top_comp, bottom_comp, i, j))
    if matched_pairs:
        best_pair = max(matched_pairs, key=lambda p: p[0].size() + p[1].size())
        top_region, bottom_region, top_idx, bottom_idx = best_pair
        
        save_cloud(top_region, "gap_region")
        save_cloud(bottom_region, "gap_region")
        cc.invertNormals([bottom_region])
        merged = cc.MergeEntities([top_region, bottom_region])
        merged.setName(f"merged_{top_id}_{bottom_id}")
        save_cloud(merged, "merged")
    else:
        for i, comp in enumerate(top_components):
            comp.setName(f"{top_id}_component_{i}")
            save_cloud(comp, f"debug_top_comp_{i}")
        for i, comp in enumerate(bottom_components):
            comp.setName(f"{bottom_id}_component_{i}")
            save_cloud(comp, f"debug_bottom_comp_{i}")

print("completed")