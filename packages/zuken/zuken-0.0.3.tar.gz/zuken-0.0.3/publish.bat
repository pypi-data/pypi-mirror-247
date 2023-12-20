python -m build
python -m twine upload -u "__token__" --repository testpypi dist/*
