#!/bin/zsh

cd "$(dirname "$0")";

python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

read "channelId?CHANNEL_ID: "
outputFile=".env"
(
  echo "CHANNEL_ID=$channelId"
) > $outputFile

echo ".env initialized"