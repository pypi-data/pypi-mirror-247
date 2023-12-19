#!/usr/bin/env bash
rm -rf dist/*
python setup.py sdist bdist_wheel
#tar -zxvf ./dist/core_base-1.0.5.tar.gz -C ./dist/
twine upload --repository-url https://upload.pypi.org/legacy/ -u wangcongxing -p wang@199394  dist/*
# twine upload dist/*