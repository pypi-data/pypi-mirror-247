from setuptools import setup, find_packages

setup(
    name='align_phonemes',
    version='0.12',
    packages=['align_phonemes', 'align_phonemes.utils', 'align_phonemes.src'],
    description='Phoneme Aligner',
    long_description=open('README.md').read(),
    long_description_content_type='text/plain',
    author='Will Stonebridge, Tyler Dierckman, Alex De Bruyn',
    url='https://github.itap.purdue.edu/kumar603/align_phonemes',
    install_requires=[
        'librosa>=0.10.1',
        'soundfile>=0.12.1',
        'docker>=7.0.0',
        'jiwer>=3.0.3',
        'scipy>=1.11.3',
        'numpy>=1.26.1',
        'torch>=2.1.0',
        'transformers>=4.34.1'
    ],
    classifiers=[
        # Classifiers help users find your project by categorizing it
        # For a full list, see https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    package_data={
        'align_phonemes': ['get_forced_alignments.py',
                           'utils/*', 'trials/*', 'src/*']
    },
    exclude_package_data={
        'align_phonemes': ['data/*', 'env/*', 'pretrained_models/*'],
    }
)