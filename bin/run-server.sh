#!/bin/bash

# ensure our working directory is bin
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
# configure Flask, then start the server
export FLASK_APP="../server/app.py"
export FLASK_ENV=development

flask run
