from setuptools import setup, find_packages

name = 'shallow'
version = '0.3'

with open('README.md' ,'r') as f:
    long_description = f.read().strip()

setup(
    name=name,
    version=version,
    description=name,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=f'https://github.com/mdmould/{name}',
    author='Matthew Mould',
    author_email='mattdmould@gmail.com',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[
        'numpy',
        'tqdm',
        # 'tensorflow',
        # 'torch',
        # 'nflows @ git+https://github.com/bayesiains/nflows.git',
        # 'pyro-ppl',
        # 'numpyro',
        # 'jax',
        # 'jax_tqdm',
        # 'jax_tqdm',
        # 'optax',
        # 'equinox',
        # 'flowjax>=11.2.0',
        ],
    )
