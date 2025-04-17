from setuptools import setup, find_packages

setup(
    name="histogram_image_enhancer",
    version="0.1.0",
    description="Advanced image processing using histogram manipulation techniques",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mihal Dimo",
    author_email="mihal@kakao.com",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "numpy",
        "matplotlib"
    ],
    entry_points={
        "console_scripts": [
            "histogram-enhancer=histogram_image_enhancer.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)