from setuptools import setup, find_packages

setup(
    name='aadhaar_detection',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy',
        'tensorflow',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'aadhaar-detect=aadhaar_detection.your_main_script:main',
        ],
    },
    author='Girinath',
    author_email='girinathr@simplfin.tech',
    description='A library that helps identify Aadhaar cards in images.',
    url='https://github.com/GirinathRG/aadhaar_lib',
    zip_safe=False,  # Add this line
    setup_requires=["setuptools_scm"],  # Add this line
)
