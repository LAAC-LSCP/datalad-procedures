#!/usr/bin/env python3
import os
import requests
import shutil
import sys
import zipfile

import datalad.api
from datalad.distribution.dataset import require_dataset

from git import Repo

ds = require_dataset(
    sys.argv[1],
    check_installed = True,
    purpose = 'setup empty dataset'
)

dataset_name = os.path.basename(ds.path)
organization = os.getenv('GITHUB_ORGANIZATION') # e.g. LAAC-LSCP
template = 'https://github.com/LAAC-LSCP/laac1-template'
path = os.getenv('DATASET_PATH') # e.g. /scratch1/data/laac_data
ssh_hostname = os.getenv('SSH_HOSTNAME') # e.g. oberon

# remove files to be replaced
os.remove(os.path.join(sys.argv[1], ".gitattributes"))

# download empty-dataset template
res = requests.get("{}/archive/master.zip".format(template))
open("master.zip", "wb").write(res.content)

with zipfile.ZipFile("master.zip") as zip_file:
    for member in zip_file.namelist():
        filename = member.replace("{}-master/".format(os.path.basename(template)), "")

        source = zip_file.open(member)
        dest = os.path.join(sys.argv[1], filename)

        if os.path.isdir(filename) or filename.endswith('/'):
            os.makedirs(filename, exist_ok = True)
            continue

        if os.path.exists(dest):
            continue

        target = open(dest, "wb")

        with source, target:
            shutil.copyfileobj(source, target)

os.remove("master.zip")

open(os.path.join(sys.argv[1], '.datalad/path'), 'w+').write(os.path.join(dataset_path, dataset_name))

# commit everything
repo = Repo(sys.argv[1])
repo.git.add('*')
repo.git.commit(m = "initial commit")

url = open(os.path.join(sys.argv[1], '.datalad/path')).read().strip()

if ssh_hostname:
    url = "ssh://{}{}".format(ssh_hostname, url)

# create the cluster sibling
datalad.api.create_sibling(
    name = 'cluster',
    dataset = ds,
    sshurl = url,
    annex_wanted = 'include=*'
)

# create github sibling
datalad.api.create_sibling_github(
    name = 'origin',
    reponame = dataset_name,
    dataset = ds,
    github_organization = organization,
    access_protocol = 'ssh',
    private = True,
    publish_depends = 'cluster'
)

datalad.api.push(dataset = ds, to = 'origin')
repo.heads.master.set_tracking_branch(repo.remotes.origin.refs.master)