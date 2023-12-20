#!/bin/sh

cd $HOME/.local && \
. venv_indicatortest/bin/activate && \
cd venv_indicatortest/lib/python3.*/site-packages/indicatortest && \
python3 indicatortest.py
