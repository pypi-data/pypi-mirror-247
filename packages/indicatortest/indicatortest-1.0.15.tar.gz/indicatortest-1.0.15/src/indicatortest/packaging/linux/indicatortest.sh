#!/bin/sh

cd $HOME/.local && \
. venv_indicatortest/bin/activate && \
cd $(ls -d $HOME/.local/venv_indicatortest/lib/python3.* | head -1)/site-packages/indicatortest && \
python3 indicatortest.py
