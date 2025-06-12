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
    save_path = os.path.join(output_path, f"{cloud.getName()}.las")
    res=cc.SavePointCloud(cloud, save_path) 
    return save_path

def filter_distance(cloud, threshold=0.01):
    sf_index = cloud.getNumberOfScalarFields() - 1  
    sf = cloud.getScalarField(sf_index)
    cloud.setCurrentOutScalarField(sf_index)
    sf.computeMinAndMax()
    filtered = cc.filterBySFValue(threshold, float("inf"), cloud)
    if filtered:
        filtered.setName(cloud.getName() + "_highchange")
        return filtered
    return None


def extract_largest_component(cloud, octree_level=11):
    result = cc.ExtractConnectedComponents(clouds=[cloud], octreeLevel=octree_level, randomColors=False)
    components = result[1] 
    largest = max(components, key=lambda c: c.size())
    largest.setName(cloud.getName() + "_largest")
    return largest


for job in job_data:
    top_id = job["top"]
    bottom_id = job["bottom"]

    top_mesh = load_mesh(top_id)
    bottom_mesh = load_mesh(bottom_id)
    top_cloud = sample_mesh(top_mesh)
    bottom_cloud = sample_mesh(bottom_mesh)
    save_cloud(top_cloud, "cloud")
    save_cloud(bottom_cloud, "cloud")

    cc.DistanceComputationTools.computeApproxCloud2CloudDistance(top_cloud, bottom_cloud)
    cc.DistanceComputationTools.computeApproxCloud2CloudDistance(bottom_cloud, top_cloud)

    top_filtered = filter_distance(top_cloud, threshold=0.01)
    bottom_filtered = filter_distance(bottom_cloud, threshold=0.01)

    top_clean = extract_largest_component(top_filtered) if top_filtered else None
    bottom_clean = extract_largest_component(bottom_filtered) if bottom_filtered else None
    if top_clean: save_cloud(top_clean, "clean")
    if bottom_clean: save_cloud(bottom_clean, "clean")

    if bottom_clean:
        cc.invertNormals([bottom_clean])
    if top_clean and bottom_clean:
        merged = cc.MergeEntities([top_clean, bottom_clean])
        merged.setName(f"merged_{top_clean.getName()}_{bottom_clean.getName()}")
        merged.setName(f"merged_{top_id}_{bottom_id}")
        save_cloud(merged, "merged")

    print(f"finished all")