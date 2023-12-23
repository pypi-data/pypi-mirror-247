from setuptools import setup,find_packages

VERSION = "0.0.1"
DESCRIPTION = "Pacote de teste"
LONG_DESCRIPTION = "Pacote de teste para o curso de Python"

#setting up

setup(
    # the name must match the folder name
    name="very_simple_kawan",
    version = VERSION,
    author = "Kawan",
    author_email = "kawanevilgenius321@gmai.com",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = ["numpy"],#adiciona bibliotecas adicionais
    keywords = ['python','primeiro pacote'],
    classifiers = ["Development Status :: 3 - Alpha",]

)