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

### The LAAC1 template

The LAAC2 template creates a dataset with three GIN siblings:

 - One containing all the data
 - One containing confidential data, but not the recordings
 - One containing all non-confidential data


```bash
export GIN_ORGANIZATION="LAAC-LSCP" # name of your GitHub organization
datalad create -c laac2 dataset-name
```

### The EL1000 template

1. Create two *empty* repositories in your GIN organization: `<dataset-name>` and `<dataset-name>-confidential`, e.g. `dataset1` and `dataset1-confidential`.

2. Run the following script (edit the environment variables to suit your configuration):

```bash
export GIN_ORGANIZATION='EL1000' # name of your GIN organization
export CONFIDENTIAL_DATASET=0 # set to 1 if there should be a confidential sibling
datalad create -c el1000 dataset-name
```
