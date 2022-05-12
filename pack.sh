pip uninstall -y khandytool
rm -rf ./dist/*
python setup.py sdist bdist_wheel
pip install ./dist/khandytool-0.2.53-py3-none-any.whl
#pip install ./dist/khandytool-0.2.53.tar.gz
