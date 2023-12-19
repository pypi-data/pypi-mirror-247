from setuptools import setup

setup(
    name='molvoxel',
    version='0.1.0',
    description='MolVoxel:easy-to-use Molecular Voxelization Tool implemented in Python.',
    author='Seonghwan Seo',
    author_email='shwan0106@gmail.com',
    url='https://github.com/SeonghwanSeo/molvoxel',
    packages=['molvoxel/'],
    install_requires=['numpy', 'scipy'],
    extras_require={
            'numba': ['numba'],
            'torch': ['torch'],
            'rdkit': ['rdkit'],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',

        'Development Status :: 4 - Beta',

        'Operating System :: OS Independent',

        'License :: OSI Approved :: MIT License',

        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
