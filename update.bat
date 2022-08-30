@echo off
if [%1] == [] goto invalid-args

echo 0.0.%1 > __version__.ignore
del /Q dist
python setup.py sdist bdist_wheel
python -m twine upload dist/*
exit 0

:invalid-args
echo "Invalid arguments | need one argument (version number)"
exit 1