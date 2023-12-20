from setuptools import setup, find_packages

setup(
    name='GirderPatchLoad',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'joblib',
        'xgboost',
    ],
)
