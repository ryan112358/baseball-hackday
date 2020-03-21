#!/bin/bash

# ensure our working directory is bin
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
# tell Flask where to find our server, then start it
export FLASK_APP="../server/app.py"
flask run
