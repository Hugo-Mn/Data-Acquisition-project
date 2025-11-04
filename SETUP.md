# Setup Instructions

## Python Installation

1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, make sure to check "Add Python to PATH"
3. Verify installation by opening a terminal and running:

   ```bash
   python --version
   ```

## Required Packages Installation

Install all required packages using pip:

```bash
pip install pandas matplotlib seaborn requests
```

To verify the installations:

```bash
python -c "import pandas; import matplotlib; import seaborn; import requests; print('All packages installed successfully!')"
```

## Troubleshooting

If you encounter pip command not found:

1. Make sure Python is in your PATH
2. Try using:

   ```bash
   python -m pip install pandas matplotlib seaborn requests
   ```

If you have both Python 2 and 3:

- Use `python3` instead of `python`
- Use `pip3` instead of `pip`
