from setuptools import setup, find_packages

setup(
    name='aadhaar-detection',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        # Add any other dependencies your library needs
    ],
    author='Girinath',
    author_email='girinathr@simplfin.tech',
    description='Aadhaar card detection library',
    long_description='A library for detecting Aadhaar cards in images.',
    url='https://github.com/yourusername/aadhaar-detection',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
