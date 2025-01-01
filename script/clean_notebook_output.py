"""
Clear the output of all notebook files under the specified folder

清空指定文件夹下的所有notebook文件的输出
"""

import os
import json


def clear_ipynb_outputs(folder_path):
    """Recursively traverse the specified folder and clear the output content of
    all .ipynb files in it.

    递归遍历指定文件夹，清空其中所有.ipynb文件的输出内容
    """
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".ipynb"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        notebook_data = json.load(f)

                    for cell in notebook_data["cells"]:
                        if "outputs" in cell:
                            cell["outputs"] = []
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(notebook_data, f, indent=4)

                # pylint: disable=broad-except
                except Exception as e:
                    print(f"Error when processing {file_path}: {str(e)}")


if __name__ == "__main__":
    clear_ipynb_outputs("../notebook")

    print("Clear all output in notebook completed.")
