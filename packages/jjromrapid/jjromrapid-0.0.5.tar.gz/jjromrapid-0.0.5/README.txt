# resto_api
resto python API

## Build

Install virtual environnment :

    python3 -m venv venv
    source venv/bin/activate
    pip install wheel
    pip install setuptools
    pip install build
    pip install twine

    # Build
    python -m build

    # Install library on PyPi
    python3 -m pip install --upgrade twine
    python3 -m twine upload --repository jjromrapid dist/*    

    # Install library from local build
    pip install ./dist/resto_api-0.0.1-py3-none-any.whl --force-reinstall
