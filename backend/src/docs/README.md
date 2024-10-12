# Requirements

You need to install ```sphinx``` and ```sphinxcontrib-napoleon```

See ```requirements.txt```

For making LaTeX documentation you need to install ```latex```. ```texlive```, ```texlive-latex-base```, ```texlive-latex-extra```

```bash
apt install latex texlive texlive-latex-base texlive-latex-extra
```
# Making documentation

To make documentation you have to run the following command:

```bash
sphinx-apidoc -f -o src/docs src/app
```

As a result of this, files with the .rst extension corresponding to the program modules will appear in the ```docs``` folder.

## HTML

To make documentation file with .html extension you need to run the following commands:

```bash
sphinx-build -b=html src/docs src/docs/_build/html
```

An ```index.html``` file with documentation will appear in the ```/src/docs/_build/html`` directory. 
