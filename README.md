# README

### Overview

The CND system includes 2 python files: `work_createInstance.py`, `CNDinInstance.py`.

- `work_createInstance.py` : This file should be run on PC. After enter some parameters, it would create instances and wait for result. 

- `CNDinInstance.py` : This file would be run on instances. And I have upload it to Github. The script in `work_createInstance.py` would download it automatically to the instances.

### Configuration

- Environment in PC
  - The user should install python3, pip, AWSCLI, and boto3 
  - Configure AWSCLI 
- The way of uploading access_key to instances
  - If you upload your access_key to Instances by yourself, please delete line 201 - 217 in `work_createInstance.py`
  - If not, please copy your access_key to  line 185 (ACCESS_KEY) in `work_createInstance.py`

### Running

`$ Python3 work_createInstance.py`



