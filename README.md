## Installation instructions

### Download the package

```bash
git clone git@github.com:LAAC-LSCP/datalad-procedures.git
cd datalad-procedures
```

### If needed, activate the ChildProjectVenv virtual environment

```bash
source ~/ChildProjectVenv/bin/activate
```


### Install the dependencies

```bash
apt-get install git-annex || brew install git-annex
pip3 install -r requirements.txt
```

### Install the procedures

```bash
python3 install.py
```

### Check the installation

```bash
datalad run-procedure --discover
```

Expected output:

> cfg_laac1 (/Users/acristia/ChildProjectVenv/lib/python3.6/site-packages/datalad/resources/procedures/cfg_laac1.py) [python_script]
cfg_yoda (/Users/acristia/ChildProjectVenv/lib/python3.6/site-packages/datalad/resources/procedures/cfg_yoda.py) [python_script]
cfg_el1000 (/Users/acristia/ChildProjectVenv/lib/python3.6/site-packages/datalad/resources/procedures/cfg_el1000.py) [python_script]
cfg_text2git (/Users/acristia/ChildProjectVenv/lib/python3.6/site-packages/datalad/resources/procedures/cfg_text2git.py) [python_script]
cfg_metadatatypes (/Users/acristia/ChildProjectVenv/lib/python3.6/site-packages/datalad/resources/procedures/cfg_metadatatypes.py) [python_script]
cfg_laac2 (/Users/acristia/ChildProjectVenv/lib/python3.6/site-packages/datalad/resources/procedures/cfg_laac2.py) [python_script]

## Usage

### The LAAC1 template

The LAAC1 template creates a dataset with two siblings:

 - One on GitHub
 - One on a specified SSH location


```bash
export GITHUB_ORGANIZATION="LAAC-LSCP" # name of your GitHub organization
export DATASET_PATH="/location/of/your/datasets/" # remote location of the dataset in the server
export SSH_HOSTNAME="your.cluster.com" # hostname/alias of your ssh server

datalad create -c laac1 dataset-name
```

### The LAAC2 template

The LAAC2 template creates a dataset with three GIN siblings:

 - One containing all the data
 - One containing confidential data, but not the recordings
 - One containing all non-confidential data


```bash
export GIN_ORGANIZATION="LAAC-LSCP" # name of your GitHub organization
datalad create -c laac2 dataset-name
```

### The EL1000 template

1. Using the browser capabilities on GIN, create two *empty* repositories in your GIN organization: `<dataset-name>` and `<dataset-name>-confidential`, e.g. `dataset1` and `dataset1-confidential`. Here's an example of creation of the first (i.e. non confidential); notice that in the last step, you need to uncheck the box at the bottom.

![Screen Shot 2021-05-05 at 09 03 01](https://user-images.githubusercontent.com/7464861/117106856-df609500-ad80-11eb-8bee-394083c920a6.png)

![image](https://user-images.githubusercontent.com/7464861/117107064-467e4980-ad81-11eb-9861-f6466b437caf.png)



2. Run the following script (edit the environment variables to suit your configuration):

```bash
export GIN_ORGANIZATION='EL1000' # name of your GIN organization
export CONFIDENTIAL_DATASET=0 # set to 1 if there should be a confidential sibling
datalad create -c el1000 dataset-name
```

For instance, in the example above, we'd do:

```bash
export GIN_ORGANIZATION='EL1000' # name of your GIN organization
export CONFIDENTIAL_DATASET=0 # set to 1 if there should be a confidential sibling
datalad create -c el1000 rague
export CONFIDENTIAL_DATASET=1 # set to 1 if there should be a confidential sibling
datalad create -c el1000 rague-confidential

```
