pip uninstall -y khandytool
rm -rf ./dist/*
rm -rf ./build/*
python setup.py sdist bdist_wheel
pip install ./dist/khandytool-0.2.59-py3-none-any.whl
# pip install ./dist/khandytool-0.2.54.tar.gz
