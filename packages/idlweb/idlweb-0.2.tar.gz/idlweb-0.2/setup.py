import setuptools 

setuptools.setup(
    name="idlweb",
    version="0.2",
    author="issam iso",
    description="Sipmle Library in python for login web site",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 ",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[
        'requests',
        'bs4'
    ]
)
