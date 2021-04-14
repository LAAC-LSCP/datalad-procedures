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
private_organization = 'LAAC-LSCP'

# remove files to be replaced
os.remove(os.path.join(sys.argv[1], ".gitattributes"))

res = requests.get("https://github.com/LAAC-LSCP/laac2-template/archive/master.zip")
open("master.zip", "wb").write(res.content)

with zipfile.ZipFile("master.zip") as zip_file:
    for member in zip_file.namelist():
        filename = member.replace("laac2-template-master/", "")

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

open(os.path.join(sys.argv[1], '.datalad/path'), 'w+').write(os.path.join('/scratch1/data/private_data/', dataset_name))

# commit everything
repo = Repo(sys.argv[1])
repo.git.add('*')
repo.git.commit(m = "initial commit")

el1000_url = "git@gin.g-node.org:/{}/{}.git".format(el1000_organization, dataset_name)
confidential_url = "git@gin.g-node.org:/{}/{}-confidential.git".format(el1000_organization, dataset_name)
private_url = "git@gin.g-node.org:/{}/{}.git".format(private_organization, dataset_name)

siblings = {
    'private': {'url': private_url, 'wanted': 'include=*' },
    'el1000': {'url': el1000_url, 'wanted': '(metadata=EL1000=*) and (exclude=**/confidential/*)'},
    'confidential': {'url': confidential_url, 'wanted': '(metadata=EL1000=*) and (include=**/confidential/*)'}
}

master = repo.heads.master
master.rename('main')

origin = 'private'

for sibling_name in siblings:
    sibling = siblings[sibling_name]
    name = 'origin' if sibling_name == origin else sibling_name
    
    datalad.api.siblings(
        name = name,
        dataset = ds,
        action = 'add',
        url = sibling['url']
    )

    datalad.api.push(dataset = ds, to = name)

for sibling_name in siblings:
    sibling = siblings[sibling_name]
    name = 'origin' if sibling_name == origin else sibling_name

    datalad.api.siblings(
        name = name,
        dataset = ds,
        action = 'configure',
        annex_wanted = sibling['wanted'],
        annex_required = sibling['wanted']
    )

master.set_tracking_branch(repo.remotes.origin.refs.main)

available_siblings = {sibling['name'] for sibling in datalad.api.siblings(dataset = ds)}

datalad.api.siblings(
    name = 'origin',
    dataset = ds,
    action = 'configure',
    publish_depends = list( (set(siblings.keys()) & available_siblings) - {origin} )
)