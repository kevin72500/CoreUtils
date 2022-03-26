pip uninstall -y khandytool
rm -rf ./dist/*
python setup.py sdist bdist_wheel
pip install ./dist/khandytool-0.2.46-py3-none-any.whl
