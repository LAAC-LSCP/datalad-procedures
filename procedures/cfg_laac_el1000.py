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
el1000_organization = 'EL1000'
laac_organization = 'LAAC-LSCP'

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

el1000_url = "git@gin.g-node.org:/{}/{}.git".format(el1000_organization, dataset_name)
confidential_url = "git@gin.g-node.org:/{}/{}-confidential.git".format(el1000_organization, dataset_name)
laac_url = "git@gin.g-node.org:/{}/{}.git".format(laac_organization, dataset_name)

siblings = {
    'el1000': {'url': el1000_url, 'wanted': '(include=*) and (exclude=**/confidential/*) and (exclude=recordings/*) and (exclude=)'},
    'confidential': {'url': confidential_url, 'wanted': 'include=**/confidential/*'},
    'origin': {'url': laac_url, 'wanted': 'include=*' }
}

master = repo.heads.master
master.rename('main')

for sibling_name in siblings:
    sibling = siblings[sibling_name]
    
    datalad.api.siblings(
        name = ,
        dataset = ds,
        action = 'add',
        url = sibling['url']
    )

    datalad.api.push(dataset = ds, to = sibling_name)   


for sibling_name in siblings:
    sibling = siblings[sibling_name]

    datalad.api.siblings(
        name = sibling_name,
        dataset = ds,
        action = 'configure',
        annex_wanted = sibling['wanted'],
        annex_required = sibling['wanted']
    )

master.set_tracking_branch(repo.remotes.origin.refs.main)