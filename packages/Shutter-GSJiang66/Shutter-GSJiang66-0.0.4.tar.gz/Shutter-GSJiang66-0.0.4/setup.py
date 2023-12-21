import setuptools

with open ('README.md','r',encoding='utf-8') as f:
    long_des=f.read()

setuptools.setup(
    name="Shutter-GSJiang66",
    version="0.0.4",
    author="GSJiang66",
    author_email="GSJiang66@outlook.com",
    description="A simple realization of optical shutter",
    long_description=long_des,
    long_description_content_type="text/markdown",
    install_requires=['serial>=0.0.97'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)