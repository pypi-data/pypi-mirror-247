from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Pacote de teste'
LONG_DESCRIPTION = 'Pacote de teste para o curso de Poo@'

# Setting up
setup(
    name="verysimplemodule_guilherme",
    version=VERSION,
    author="Guilherme",
    author_email="guilherme.silva@ufpi.edu.br",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['scikit-image', 'numpy', 'matplotlib'],

    keywords=['python', 'pacote', 'teste'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ]
)
