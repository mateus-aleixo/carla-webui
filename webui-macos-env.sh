#!/bin/bash

if [[ -x "$(command -v python3.8)" ]]
then
    python_cmd="python3.8"
fi

export install_dir="$HOME"
