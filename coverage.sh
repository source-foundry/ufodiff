#!/bin/sh

coverage run --source ufodiff -m py.test
coverage report -m
coverage html

#coverage xml
#codecov --token=$CODECOV_{{ufodiff}}
