from setuptools import setup, find_packages

VERSION = "0.0.2"
DESCRIPTION = "Pacote de teste"
LONG_DESCRIPTION = "Pacote de teste para o curso de Python"

# setting up

setup(
    # the name must match the folder name
    name="verysimplemodule_crisly",
    version=VERSION,
    author="crisly",
    author_email="crislymaria21@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["numpy"],  # adiciona bibliotecas adicionais
    keywords=['python', 'primeiro pacote'],
    classifiers=["Development Status :: 3 - Alpha",]

)
