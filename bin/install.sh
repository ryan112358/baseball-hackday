#!/bin/bash

# ensure our working directory is bin
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
# install dependencies defined in requirements.txt
pip install -r ../requirements.txt
