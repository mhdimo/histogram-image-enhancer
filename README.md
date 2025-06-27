# Histogram Image Enhancer

Python tool to improve images using histogram techniques:  
- **Global Equalization**  
- **CLAHE** (Contrast Limited Adaptive Histogram Equalization)  
- **Gamma Correction**  

It provides an intuitive and configurable command-line interface (`histogram-enhancer`), generating the processed image along with a graphical comparison including histograms.

---

## Table of Contents

1. [Features](#features)  
2. [Installation](#installation)  
3. [Requirements](#requirements)  
4. [Quick Start](#quick-start)  
5. [CLI: Options and Commands](#cli-options-and-commands)  
6. [Advanced Examples](#advanced-examples)  
7. [Results Structure](#results-structure)  
8. [Testing](#testing)  
9. [Development](#development)  
10. [Contributing](#contributing)  
11. [License](#license)  

---

## Features

- **Global Histogram Equalization**: Improves the overall image contrast.  
- **CLAHE**: Locally adapts the equalization to avoid over-enhancement.  
- **Gamma Correction**: Adjusts brightness based on the gamma curve.  
- **Visual Comparison**: Saves a 2×2 image with the original, processed, and their histograms.  
- **CLI based on [Click](https://click.palletsprojects.com/)**: Clear, extensible, and testable.  
- **Logging**: Operation logs stored in `histogram_image_enhancer/logs/enhancer.log`.  
- **Modular**: Code organized into packages and modules with **type hints**, **pathlib**, **docstrings**.  

---

## Installation

### Windows (PowerShell)

```powershell
git clone <repo-url>
cd <repo-directory>
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

### Linux/macOS

```bash
git clone <repo-url>
cd <repo-directory>
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Requirements

Check requirements.txt for exact versions. In general:

- Python 3.6+
- opencv-python
- numpy
- matplotlib
- click

### Quick Start

Run:

```bash
histogram-enhancer path/to/image.jpg
```

By default, it applies equalization and saves:

- results/image.jpg
- results/image_comparison.png

## CLI: Options and Commands

To view all options:

```bash
histogram-enhancer --help
```

## Advanced Examples

Equalize globally (default):

```bash
histogram-enhancer photo.jpg
```

Custom CLAHE:

```bash
histogram-enhancer document.tif \
    --method clahe \
    --clip-limit 3.5 \
    --tile-size 16,16
```

Low Gamma (brighter image):

```bash
histogram-enhancer landscape.png \
    --method gamma \
    --gamma 0.4
```

Simple batch processing (with bash):

```bash
for img in folder/*.jpg; do
    histogram-enhancer "$img" --method equalize
done
```

## Results Structure

After each execution, in the results/ directory you'll find:

- image.jpg — processed image
- image_comparison.png — 2×2 comparison (original, processed, histograms)

Example directory tree:

```bash
results/
├── photo.jpg
└── photo_comparison.png
```

## Testing

Run all tests with pytest:

```bash
pytest --maxfail=1 --disable-warnings -q
```

## Development

- Code quality supported by: Black, isort, Flake8 via pre-commit.
- Continuous integration setup: GitHub Actions in .github/workflows/ci.yml.
- Add your tests and modules in histogram_image_enhancer/core/ and update tests/.

## Contributing

- Read docs/CONTRIBUTING.md.
- Fork the repository and create a new branch (git checkout -b feature/my-enhancement).
- Ensure that Black and isort pass, and pytest runs successfully.
- Open a Pull Request describing your enhancement.

## License

This project is under the MIT License.  
See the LICENSE file for details.
