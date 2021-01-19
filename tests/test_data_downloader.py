# This module is named "test_*" so that it will be picked up and run
# when pytest is used to run all tests, e.g. with "pytest tests".
#
# The actual purpose of this module is to pre-clone a git repository
# to download all the required test data before any of the tests run.
#
# It works as follows:
# - clone repo
# - move repo into location where test data is expected to be found
#
import os, shutil

tmp_repo = '/tmp/.mini-esgf-data'
test_data_dir = os.path.join(tmp_repo, 'test_data')
repo_url = 'https://github.com/roocs/mini-esgf-data'
target = '/root/.mini-esgf-data/master'

if not os.path.isdir(target):
    os.makedirs(target) 
    os.system(f'git clone {repo_url} {tmp_repo}')

    shutil.move(test_data_dir, target)
    shutil.rmtree(tmp_repo)  

print(f'[INFO] Cloned test_data repo to: {target}')

