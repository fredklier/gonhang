import setuptools


setuptools.setup(
    name='gonhang',
    version='0.0.0',
    author="Fred Cox",
    author_email="fredcox@gmail.com",
    description='gonhang - The Next Generation Light-Weight System Monitor for Linux',
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/fredcox/gonha-ng",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.8',
    scripts=['bin/gonhang'],

    install_requires=[
        'PyQt5',
        'psutil',
        'humanfriendly',
        'coloredlogs',
    ],
    include_package_data=True,
    zip_safe=False,
)
