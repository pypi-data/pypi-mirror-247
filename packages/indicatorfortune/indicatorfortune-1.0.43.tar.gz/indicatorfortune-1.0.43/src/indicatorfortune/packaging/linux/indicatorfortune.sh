#!/bin/sh

cd $HOME/.local && \
. venv_indicatorfortune/bin/activate && \
cd $(ls -d $HOME/.local/venv_indicatorfortune/lib/python3.* | head -1)/site-packages/indicatorfortune && \
python3 indicatorfortune.py
