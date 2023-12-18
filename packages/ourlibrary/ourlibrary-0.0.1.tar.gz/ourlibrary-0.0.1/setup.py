from setuptools import setup, find_packages

setup(
    name="ourlibrary",
    version="0.0.1",
    author="Labdhi Gandhi",
    author_email="ramasandeepedlabadkar@g.harvard.edu",
    description="Team 12 package",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://code.harvard.edu/CS107/team12_2023.git",  
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        'pytest==7.3.0', 
        'scikit-learn',
        'numpy==1.21.2',
        'pandas==1.3.3',
        'matplotlib==3.4.3',
        'bokeh==3.3.2',
    ],
    setup_requires=["setuptools>=61.0"],
    include_package_data=True,
    zip_safe=False,
)
