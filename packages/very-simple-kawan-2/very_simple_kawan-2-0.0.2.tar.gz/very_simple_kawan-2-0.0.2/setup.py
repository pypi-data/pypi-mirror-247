from setuptools import setup, find_packages

VERSION = "0.0.2"  # Atualize para a nova versão
DESCRIPTION = "Pacote de teste python"
LONG_DESCRIPTION = ("Pacote de teste para o curso de Python"
                    "para iniciantes"
                    "Funcoes:"
                    "soma"
                    "subtracao"
                    "multiplicacao"
                    "divisao")

# Configuração do setup
setup(
    # O nome deve corresponder ao nome da pasta
    name="very_simple_kawan-2",
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
