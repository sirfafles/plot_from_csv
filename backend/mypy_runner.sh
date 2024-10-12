pycodestyle src/
pylint src/
mypy src/ --exclude 'docs' --allow-subclassing-any
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
find . | grep -E "(.mypy_cache)$" | xargs rm -rf
find . | grep -E "(.pytest_cache)$" | xargs rm -rf

read -p 'Press [Enter] key to continue...'
