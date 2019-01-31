#!/usr/bin/env bash

python rebuild_tools
git commit
git push
sudo conda build .
sudo conda install --use-local .