# snake_me_please/converter.py
import os
import re
import ast
import keyword
import argparse
from typing import List, Tuple, Set


def is_valid_variable_name(name: str) -> bool:
    """
    Check if a variable name is valid (not a keyword, not imported, and not a Python built-in).

    Parameters:
    - name (str): The variable name.

    Returns:
    - bool: True if the variable name is valid, False otherwise.
    """
    return name.isidentifier() and not keyword.iskeyword(name)


def convert_to_snake_case(variable_name: str) -> str:
    """
    Convert a variable name to snake_case.

    Parameters:
    - variable_name (str): The variable name to convert.

    Returns:
    - str: The variable name in snake_case.
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", variable_name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def process_file(file_path: str) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Process a Python file and convert user-defined variable names to snake_case.

    Parameters:
    - file_path (str): The path to the Python file.

    Returns:
    - Tuple[str, List[Tuple[str, str]]]: A tuple containing the file path and the list of converted variables.
    """
    with open(file_path, "r") as file:
        content = file.read()

    tree = ast.parse(content)
    converted_variables = []
    imported_modules = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            for alias in node.names:
                module_name = alias.asname or alias.name.split(".")[0]
                imported_modules.add(module_name)

        if isinstance(node, ast.Name) and is_valid_variable_name(node.id):
            original_name = node.id
            converted_name = convert_to_snake_case(original_name)

            if (
                original_name != converted_name
                and original_name not in imported_modules
            ):
                converted_variables.append((original_name, converted_name))
                content = re.sub(
                    r"\b" + original_name + r"\b", converted_name, content
                )

    with open(file_path, "w") as file:
        file.write(content)

    return file_path, converted_variables


def process_directory(
    directory_path: str,
) -> Tuple[List[Tuple[str, List[Tuple[str, str]]]], int]:
    """
    Process all Python files in a directory and convert user-defined variable names to snake_case.

    Parameters:
    - directory_path (str): The path to the directory.

    Returns:
    - Tuple[List[Tuple[str, List[Tuple[str, str]]]], int]: A tuple containing a list of file conversion results
      and the total count of converted variables.
    """
    total_converted_count = 0
    converted_files = []

    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".py"):
                file_path = os.path.join(root, file_name)
                result = process_file(file_path)
                converted_files.append(result)
                total_converted_count += len(result[1])

    return converted_files, total_converted_count


def print_conversion_results(
    results: List[Tuple[str, List[Tuple[str, str]]]], total_count: int
) -> None:
    """
    Print the conversion results, including the list of variables converted and the total count.

    Parameters:
    - results (List[Tuple[str, List[Tuple[str, str]]]]): A list of tuples containing file paths and converted variable lists.
    - total_count (int): The total count of converted variables.
    """
    if total_count == 0:
        print("No variables were converted.")
        return

    print(f"Total Converted Variables: {total_count}\n")

    for file_path, converted_list in results:
        if converted_list:
            print(f"File: {file_path}")
            print("Converted Variables:")
            unique_conversions = set(converted_list)
            for original, converted in unique_conversions:
                print(f"  {original} -> {converted}")
            print()


def main() -> None:
    """
    Main entry point for the Snake Me Please command-line tool.
    """
    parser = argparse.ArgumentParser(
        description="Convert user-defined variables to snake_case in Python files."
    )
    parser.add_argument("file", help="Path to the Python file or directory")
    args = parser.parse_args()

    if os.path.isdir(args.file):
        results, total_count = process_directory(args.file)
        print_conversion_results(results, total_count)
        print(f"Conversion completed for all Python files in {args.file}")
    else:
        result = process_file(args.file)
        print(f"Conversion completed for {result[0]}")
        print_conversion_results([result], len(result[1]))


if __name__ == "__main__":
    main()
