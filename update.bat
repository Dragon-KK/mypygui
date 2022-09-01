@echo off
if [%1] == [] goto invalid-args

echo 0.0.%1 > __version__.ignore
del /Q dist
del /Q build
python setup.py sdist bdist_wheel

if not [%2] == [twine] goto end

python -m twine upload dist/*
goto end

:invalid-args
echo "Invalid arguments | need one argument (version number)"
exit 1

:end