#!/usr/bin/env bash

set -euxo pipefail

/dc.py  -f $INPUT_FILENAME -m $INPUT_MOUNTDIR -u $INPUT_URL -hn $INPUT_HOSTNAME

echo $INPUT_FILENAME
