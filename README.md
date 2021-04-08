## Installation instructions

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
