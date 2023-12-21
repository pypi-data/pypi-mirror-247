# json-tracer
A python library that generates a json file that traces the execution of a python program.

Can be run from command line or imported as a library.

## install
```bash
pip install json-tracer
```

## Run
```bash
python3 -m tracer examples/hello_world.py
```

## publish
```bash
python -m build
python -m twine upload dist/*
```
