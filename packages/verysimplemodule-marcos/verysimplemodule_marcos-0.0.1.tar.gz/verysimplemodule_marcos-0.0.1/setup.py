from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Meu primeiro pacote'
LONG_DESCRIPTION = 'Meu primeiro pacote usando a linguagem de programação python'

setup(
        name = "verysimplemodule_marcos",
        version = VERSION,
        author = "Marcos",
        author_email = "marcosofc04@gmail.com",
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        packages = find_packages(),
        install_requires = ['scikit-image', 'numpy'],

        keywords = ['python', 'primeiro pacote'],
        # classifiers = [
        #     "Development status :: 3 - Alpha",
        #     "Intended Audience :: Education",
        #     "Operating System :: Os Independent",
        # ]
)