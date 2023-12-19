#!/bin/bash

echo "Running pyup_dirs..."
pyup_dirs --py38-plus --recursive faststream examples tests

echo "Running ruff..."
ruff faststream tests --fix

echo "Running black..."
black faststream tests
