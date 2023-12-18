from setuptools import setup, find_packages

setup(
    name='noisedestroyer',
    version='0.0.1',
    author='Hans',
    author_email='hans@dreamgenerator.ai',
    description='Remove background noise from your video and audio files quickly',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',      
    install_requires=[
        'httpx',
        'aiofiles'
    ],
)