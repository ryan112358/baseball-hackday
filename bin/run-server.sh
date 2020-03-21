#!/bin/bash

# Tell Flask where to find our server, then start it
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
export FLASK_APP="../server/app.py"
flask run
