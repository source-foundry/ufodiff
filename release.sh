#!/usr/bin/env bash

python3 setup.py sdist bdist_wheel
twine upload dist/ufodiff-0.5.0*