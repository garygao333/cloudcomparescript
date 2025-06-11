import cloudComPy as cc  
import json
import numpy
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
    print(mesh.getName())
    return mesh

def sample_mesh(mesh, density=20000):
    cloud = mesh.samplePoints(densityBased=True, samplingParameter=50, withNormals=True)
    cloud.setName(mesh.getName())
    return cloud

def save_cloud(cloud):
    save_path = os.path.join(output_path, f"{cloud.getName()}.las")
    res=cc.SavePointCloud(cloud, save_path) 
    return save_path

for job in job_data:
    top_id = job["top"]
    bottom_id = job["bottom"]

    top_mesh = load_mesh(top_id)
    bottom_mesh = load_mesh(bottom_id)
    top_cloud = sample_mesh(top_mesh)
    bottom_cloud = sample_mesh(bottom_mesh)

    top_path = save_cloud(top_cloud)
    bottom_path = save_cloud(bottom_cloud)

    top_to_bottom = cc.DistanceComputationTools.computeApproxCloud2CloudDistance(top_cloud, bottom_cloud)
    save_cloud(top_cloud, f"c2c_to_{bottom_id}")
    top_to_bottom = cc.DistanceComputationTools.computeApproxCloud2CloudDistance(bottom_cloud, top_cloud)
    save_cloud(bottom_cloud, f"c2c_to_{top_id}")
    
    print("finished processing")