# vinci-auth-python-pkg
A simple package to get vinci users auth token

# Como subir novas versoes
* Faça suas alterações
* Altere a versão no arquivo setup.py
* suba o repositório
* rode os seguintes comandos
    * python setup.py sdist bdist_wheel
    * python -m twine upload dist/*
        * Para auth informe o user __token__
        * E senha informe a que se encontra no .pypirc