# Cloud Compare Script
Script to automate Cloud Compare processes; part of the Tharros Archaeological Research Project (TARP). 

Download for mac: https://www.simulation.openfields.fr/index.php/cloudcompare-downloads/7-cloudcompare-macos-binaries/116-cloudcompare-20250314-2-14-alpha-with-python-plugin 

Setup instructions for Mac: https://gitlab.com/openfields1/CloudComPy/-/blob/master/doc/UseMacOSCondaBinary.md?plain=1  
Setup instructions for Linux: https://github.com/CloudCompare/CloudComPy/blob/master/doc/UseLinuxCondaBinary.md

Documentation: https://tmontaigu.github.io/CloudCompare-PythonRuntime/index.html 

Setup for Ubuntu: https://github.com/CloudCompare/CloudComPy/blob/master/doc/BuildLinuxConda.md 


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
For Ubuntu:  
```
cd ~/CloudComPy/installConda/CloudComPy310/
. bin/condaCloud.sh activate CloudComPy310
```

Then run script with python script name. 

### Set up Input/Output directories
1. Create `Data/Final_Volumes` and `Data/Final_Volume_Tops`for outputs.  
2. Create a `~/TARP/` where all the input .ply files go

### Workflow
1. populate the example.json with the top and bottom pgram Job ids correctly labeled (refer to example.json). And, have the corresponding .ply files in the Data/Pgram_Job_<pgram#>_SU<su-numbers> folder.  
2. The pre_snip_script runs on the .ply files and produces point clouds with distances for the top and bottom cloud as .las files.  
3. Next step is to open the top and bottom .las files in CloudCompare and manually snip out the SU area of interest and clean out any outlier points. Then save the files as Pgram_Job_<pgram#>_SU<su-numbers>_cleaned_<specific_su_number>.bin as Data/Pgram_Job_<pgram#>_SU<su#> folder.  The number after cleaned is to match tops and bottoms of multiple SUs extracted from the same pgram job # model.   
If the pgram job number of the top cloud is higher than that of the bottom cloud, then make sure to rename the cleaned bin file of the top as Pgram_Job_<pgram#>_SU<su-numbers>_cleaned_<specific_su_number>_top.bin (notice the "_top" at the end of the filename).
4. Then run the `post_snip_script.py` that reads the _cleaned files and produces the SU<su#>.obj, SU<su#>_top_filtered.obj and SU<su#>_top_raw.obj. The top raw is the unprocessed Top of the SU volume that may need cleaning using the Density scalar field slider in its Properties section on CloudCompare. Top filtered obj is, frankly, a failed attempt (so far) at doing the filtering in code. As of Jul 1 2025, the filtered obj doesn't actually get filtered as expected and is the same as Top Raw object. After cleaning or if cleaning is not needed, save it as SU<su#>_top.obj
5. The volumes are written to `Data/Final_Volumes` and the top volumes are written to `Data/Final_Volume_Tops`
 
### TODO  
1. Modify the post snip script to read the directory `Data/Final_Volumes` and only process those SUs that are not present in that directory. 

### Troubleshooting  
For ubuntu, if you have any issues with [the build script](https://github.com/CloudCompare/CloudComPy/blob/master/building/genCloudComPy_Conda310_Ubuntu2004.sh) consider disabling all plugins and only keeping the essential ones in :
```
-DPLUGIN_IO_QCORE:BOOL="1" \
-DPLUGIN_IO_QADDITIONAL:BOOL="1" \
-DPLUGIN_IO_QE57:BOOL="1" \
-DPLUGIN_GL_QEDL:BOOL="1" \
-DPLUGIN_GL_QSSAO:BOOL="1" \
-DPLUGIN_IO_QLAS:BOOL="1" \
-DPLUGIN_STANDARD_QPOISSON_RECON:BOOL="1" \
```