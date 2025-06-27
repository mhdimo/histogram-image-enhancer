from setuptools import setup, find_packages
from pathlib import Path

current_directory = Path(__file__).parent
long_description = (current_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="histogram_image_enhancer",
    version="0.2.0",
    description="Advanced image processing using histogram manipulation techniques",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mihal Dimo",
    author_email="mihal@kakao.com",
    packages=find_packages(exclude=["tests", "docs", ".github"]),
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "matplotlib>=3.3.0",
        "click>=8.0",
    ],
    entry_points={
        "console_scripts": [
            "histogram-enhancer=histogram_image_enhancer.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
