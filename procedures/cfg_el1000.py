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
organization = os.getenv('GIN_ORGANIZATION')
has_confidential_sibling = int(os.getenv('CONFIDENTIAL_DATASET')) == 1

# remove files to be replaced
os.remove(os.path.join(sys.argv[1], ".gitattributes"))

res = requests.get("https://github.com/LAAC-LSCP/el1000-template/archive/master.zip")
open("master.zip", "wb").write(res.content)

with zipfile.ZipFile("master.zip") as zip_file:
    for member in zip_file.namelist():
        filename = member.replace("el1000-template-master/", "")

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

open(os.path.join(sys.argv[1], '.datalad/path'), 'w+').write(os.path.join('/scratch1/data/laac_data/', dataset_name))

# commit everything
repo = Repo(sys.argv[1])
repo.git.add('*')
repo.git.commit(m = "initial commit")

url = "git@gin.g-node.org:/{}/{}.git".format(organization, dataset_name)
confidential_url = "git@gin.g-node.org:/{}/{}-confidential.git".format(organization, dataset_name)

# create the cluster sibling
datalad.api.siblings(
    name = 'origin',
    dataset = ds,
    action = 'add',
    url = url
)

if 'main' not in repo.heads:
    if 'master' in repo.heads:
        master = repo.heads.master
        master.rename('main')
    else:
        raise ValueError(f"Could not find branch <main> nor <master>")
else:
    master = repo.heads.main

datalad.api.push(dataset = ds, to = 'origin')   

master.set_tracking_branch(repo.remotes.origin.refs.main)

datalad.api.siblings(
    name = 'origin',
    dataset = ds,
    action = 'configure',
    annex_wanted = '(include=*) and (exclude=**/confidential/*)',
    annex_required = '(include=*) and (exclude=**/confidential/*)'
)

if has_confidential_sibling:
    datalad.api.siblings(
        name = 'confidential',
        dataset = ds,
        action = 'add',
        url = confidential_url
    )

    datalad.api.push(dataset = ds, to = 'confidential')

    datalad.api.siblings(
        name = 'confidential',
        dataset = ds,
        action = 'configure',
        annex_wanted = 'include=**/confidential/*',
        annex_required = 'include=**/confidential/*'
    )

    datalad.api.siblings(
        name = 'origin',
        dataset = ds,
        action = 'configure',
        publish_depends = 'confidential'
    )
