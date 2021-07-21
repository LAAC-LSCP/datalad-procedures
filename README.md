## Installation instructions

### If needed, activate the ChildProjectVenv virtual environment

```bash
source ~/ChildProjectVenv/bin/activate
```

If the above line doesn't work, you may have installed ChildProject generally, rather than in a virtual environment. 

!Warning! If none of this rings a bell, you may have not installed ChildProject at all. To do so, follow [these instructions](https://childproject.readthedocs.io/en/latest/install.html)


### Download the package

```bash
git clone git@github.com:LAAC-LSCP/datalad-procedures.git
cd datalad-procedures
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

At this point, a message may ask you if you want to establish a fingerprint; say yes.


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


Since this relies on GIN, you need to make sure to set up your ssh key:

1. go to https://gin.g-node.org/
2. log in
3. click on top right on your avatar, choose parameters
4. click on SSH keys at the left, then click on add a key
5. do cat ~/.ssh/id_rsa.pub -- if you get an error, that means your computer does not yet have an ssh key, so follow [these instructions](https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key) to create one; if not, copy the output and paste it into the key area

Then you can create datasets as follows:

```bash
export GIN_ORGANIZATION="LAAC-LSCP" # name of your GitHub organization
datalad create -c laac2 dataset-name
```

### The EL1000 template

Since this template relies on GIN, you need to make sure to set up your ssh key:

1. go to https://gin.g-node.org/
2. log in
3. click on top right on your avatar, choose parameters
4. click on SSH keys at the left, then click on add a key
5. do cat ~/.ssh/id_rsa.pub -- if you get an error, that means your computer does not yet have an ssh key, so follow [these instructions](https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key) to create one; if not, copy the output and paste it into the key area

Then you can create datasets as follows:


1. Using the browser capabilities on GIN, create two *empty* repositories in your GIN organization: `<dataset-name>` and `<dataset-name>-confidential`, e.g. `dataset1` and `dataset1-confidential`. Here's an example of creation of the first (i.e. non confidential); notice that (a) you need to create the repo from the organization (and not your personal account) and (b) you need to uncheck the box at the bottom during actual creation.

![image](https://user-images.githubusercontent.com/7464861/117114235-dd500380-ad8b-11eb-873d-d47be02f659d.png)


![image](https://user-images.githubusercontent.com/7464861/117107064-467e4980-ad81-11eb-9861-f6466b437caf.png)



2. Run the following script (edit the environment variables to suit your configuration):

```bash
export GIN_ORGANIZATION='EL1000' # name of your GIN organization
export CONFIDENTIAL_DATASET=0 # set to 1 if there should be a confidential sibling
datalad create -c el1000 dataset-name
```

For instance, in the example above, we'd do the following, because this is a dataset that has some confidential content:

```bash
export GIN_ORGANIZATION='EL1000' # name of your GIN organization
export CONFIDENTIAL_DATASET=1 # set to 1 if there should be a confidential sibling
datalad create -c el1000 rague
```
And here is an example of a dataset that has some no content:

```bash
export GIN_ORGANIZATION='EL1000' # name of your GIN organization
export CONFIDENTIAL_DATASET=0 # set to 1 if there should be a confidential sibling
datalad create -c el1000 lyon
```
The output you'll see looks like this:

> [INFO   ] Creating a new annex repo at /Users/acristia/Documents/git-data/rague 
[INFO   ] Scanning for unlocked files (this may take some time) 
[INFO   ] Running procedure cfg_el1000 
[INFO   ] == Command start (output follows) ===== 
[INFO   ] Could not enable annex remote origin. This is expected if origin is a pure Git remote, or happens if it is not accessible. 
[WARNING] Could not detect whether origin carries an annex. If origin is a pure Git remote, this is expected.  
.: origin(-) [git@gin.g-node.org:/EL1000/rague.git (git)]
.: origin(+) [git@gin.g-node.org:/EL1000/rague.git (git)]                       
[INFO   ] Could not enable annex remote confidential. This is expected if confidential is a pure Git remote, or happens if it is not accessible. 
[WARNING] Could not detect whether confidential carries an annex. If confidential is a pure Git remote, this is expected.  
.: confidential(-) [git@gin.g-node.org:/EL1000/rague-confidential.git (git)]
.: confidential(+) [git@gin.g-node.org:/EL1000/rague-confidential.git (git)]    
[INFO   ] Configure additional publication dependency on "confidential"         
.: origin(+) [git@gin.g-node.org:/EL1000/rague.git (git)]
[INFO   ] == Command exit (modification check follows) ===== 
create(ok): /Users/acristia/Documents/git-data/rague (dataset)
