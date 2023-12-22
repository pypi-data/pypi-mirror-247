# Snake Me Please

Snake Me Please is a Python package and command-line tool designed to convert user-defined variable names to snake_case in Python files while excluding imported variables and keywords from Python libraries.

## Installation

Install the package using `pip`:

```bash
pip install snake-me-please
```

# Usage
## Convert a Single File

To convert user-defined variables to snake_case in a single Python file, use the following command:

```bash

snake-me-please your_python_file.py
```

## Convert Files in a Directory

To convert user-defined variables in all Python files within a directory, use the following command:

```bash

snake-me-please your_directory
```

## Display Conversion Results

The tool will display unique conversions and exclude imported variables or Python keywords.

### Example

```bash

snake-me-please examples/
```

This will process all Python files in the examples directory and display the conversion results.

# License

This project is licensed under the GNU General Public License - see the LICENSE file for details.

# Contributing

Feel free to contribute to this project. For major changes, please open an issue first to discuss what you would like to change.
Acknowledgments

    Inspired by the need for consistent naming conventions in Python code.
    Thanks to the open-source community for valuable contributions.

# Contact

For any inquiries, please contact [Aditya Jetely](ajetely@gmail.com).
