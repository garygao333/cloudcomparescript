# Cloud Compare Script
Script to automate Cloud Compare processes; part of the Tharros Archaeological Research Project (TARP). 

Download for mac: https://www.simulation.openfields.fr/index.php/cloudcompare-downloads/7-cloudcompare-macos-binaries/116-cloudcompare-20250314-2-14-alpha-with-python-plugin 

Setup instructions: https://gitlab.com/openfields1/CloudComPy/-/blob/master/doc/UseMacOSCondaBinary.md?plain=1  

Documentation: https://tmontaigu.github.io/CloudCompare-PythonRuntime/index.html 

## Setup

Run script using VS Code. 

### Set up the Conda environment 

```
source ~/miniconda3/etc/profile.d/conda.sh  

conda create --name CloudComPy310 python=3.10
conda activate CloudComPy310

conda config --add channels conda-forge
conda config --set channel_priority flexible
```

### Install required dependencies

```
conda install -y boost cgal cmake draco "ffmpeg=6.1" gdal jupyterlab laszip matplotlib "mysql=8" notebook numpy opencv "openssl=3.1" pcl pdal psutil pybind11 quaternion "qhull=2020.2" "qt=5.15.8" scipy sphinx_rtd_theme spyder tbb tbb-devel "xerces-c=3.2" xorg-libx11
```

### Activate environment

This is done with the CloudComPy custom script. 

```
cd ~/Desktop/CloudComPy310
source bin/condaCloud.zsh activate CloudComPy310

```

Then run script with python script name. 
