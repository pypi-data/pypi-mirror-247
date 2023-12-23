from setuptools import setup, find_packages

VERSION = "0.0.5"  # Atualize para a nova versão
DESCRIPTION = "Pacote de teste python"
LONG_DESCRIPTION = ("Pacote de teste para o curso de Python"
                    "Dica de uso:                            "
                    "import very_simple_kawan as pacote"
                    "import very_simple_kawan.extra as extra"
                    " print(pacote.add(1,2)) "
                    " print(pacote.sub(1,2)) "
                    " print(extra.multiply(1,2)) "
                    " print(extra.divide(1,2))")

# Configuração do setup
setup(
    # O nome deve corresponder ao nome da pasta
    name="very_simple_kawan",
    version=VERSION,
    author="Kawan S. Dias",
    author_email="kawanevilgenius321@gmai.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["numpy"],  # Adiciona bibliotecas adicionais
    keywords=['python', 'primeiro pacote python'],
    classifiers=["Development Status :: 3 - Alpha", ]
)
