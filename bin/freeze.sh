#!/bin/bash

# ensure our working directory is bin
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
# save list of dependencies to requirements.txt
pip freeze > ../requirements.txt
