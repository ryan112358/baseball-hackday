#!/bin/bash

echo "Removing previous deployment artifacts..."
rm -rf deployment

echo "Creating new deployment bundle"
ARCHIVE_PATH="./deployment/heatmap.zip"
mkdir -p deployment
git archive --format=zip --output=$ARCHIVE_PATH HEAD

echo "Deploying app to Azure"
# Change these values to the ones used to create the App Service.
RESOURCE_GROUP_NAME="baseball-hackday"
APP_SERVICE_NAME="heatmaps"

az login

az webapp deploy \
    --name $APP_SERVICE_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --src-path $ARCHIVE_PATH
