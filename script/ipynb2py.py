"""
Extract the Python code in the notebook files in the specified directory
into Python files with the same name.

抽取指定目录中的 notebook 文件 的 Python 代码到同名的 Python 文件中
"""

import os
from datetime import datetime

import nbformat

from config import get_logger


logger = get_logger()


def get_notebook_in_dir(directory: str) -> list[str]:
    """Recursively obtain the file paths of notebook files
    under the specified directory

    递归获取指定目录下的 notebook 文件路径
    """

    notebooks = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ipynb"):
                notebooks.append(os.path.join(root, file))
    return notebooks


def get_code_from_notebook(notebook_path: str) -> None:
    """
    Extract the code in the notebook and write it into a Python file with the same name
    抽取 notebook 中的代码写入同名的 Python 文件
    """

    def _get_code(filename: str) -> str:
        """Extract the code in the notebook"""

        nb = nbformat.read(filename, as_version=4)

        code_list = []
        for cell in nb.cells:
            if cell.cell_type == "code":
                code_list.append(cell.source)

        code = "\n".join(code_list)

        # Modify the possible resource paths in the code
        code = code.replace("../resources", "resources")

        return code

    py_path = notebook_path.replace(".ipynb", ".py")
    py_path = py_path.replace("notebook", "build/python_scripts")

    # Only update if the py file is newer than the notebook file
    if os.path.exists(py_path):
        notebook_mtime = datetime.fromtimestamp(os.path.getmtime(notebook_path))
        py_mtime = datetime.fromtimestamp(os.path.getmtime(py_path))

        if notebook_mtime > py_mtime:
            code = _get_code(notebook_path)
            with open(py_path, "w", encoding="utf-8") as f:
                f.write(code)
    else:
        if not os.path.exists(os.path.dirname(py_path)):
            os.makedirs(os.path.dirname(py_path))

        code = _get_code(notebook_path)
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(code)


if __name__ == "__main__":
    from config import tasks

    for task in tasks:
        logger.info(f"Run build task ****** {task['info']}")

        NB_DIR = os.path.join(task["project_dir"], task["notebook_dir"])
        notebook_list = get_notebook_in_dir(NB_DIR)

        i = 0
        for notebook in notebook_list:
            logger.debug(f"process {notebook} ...")

            get_code_from_notebook(notebook)
            i += 1

        logger.info(f"{i} notebooks have been converted into Python files.")
