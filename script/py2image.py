"""
Execute Python scripts in the specified directory to generate pictures

执行指定目录下的 Python 脚本生成图片
"""

import os
from datetime import datetime

from config import get_logger


logger = get_logger()


# pylint: disable=redefined-outer-name
def get_python_script_list(dir_path):
    """Get all Python scripts in the specified directory,
    return a list of sub-directories and file names

    获取指定目录下一级子文件夹下的所有 Python 脚本文件，返回一个列表，元素为子目录和无后缀文件名
    """
    script_list = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".py"):
                directory = os.path.basename(root)
                file = file.replace(".py", "")
                script_list.append((directory, file))

    return script_list


# pylint: disable=redefined-outer-name
def generate_images_by_file(py_name, fig_name, dpi=200):
    """Read and execute the script in the specified file, and add a statement to save
    the picture at the end of the script

    读取并执行指定文件中的脚本，在脚本最后添加保存图片的语句
    """
    script_mtime = datetime.fromtimestamp(os.path.getmtime(py_name))
    image_mtime = (
        datetime.fromtimestamp(os.path.getmtime(fig_name))
        if os.path.exists(fig_name)
        else None
    )

    # Only update if the image file is newer than the script file
    if image_mtime is None or script_mtime > image_mtime:
        with open(py_name, "r", encoding="utf-8") as file:
            script = file.read()

        # delete `plt.show()` to avoid blank images
        script = script.replace("plt.show()", "")

        # add `plt.savefig()` to save the image
        script += f"\nplt.savefig(r'{fig_name}', dpi={dpi})\nplt.close()"

        try:
            # pylint: disable=exec-used
            exec(script)
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error when run {py_name}: {e}")


if __name__ == "__main__":
    from config import params

    for param in params:
        logger.info(f"Run build task ****** {param['info']}")

        PY_DIR = param["py_dir"]
        IMG_FMT = param["image_format"]
        IMG_DPI = param["image_dpi"]
        IMG_DIR = param["image_dir"]

        files = get_python_script_list(PY_DIR)

        i = 0
        for h2, filename in files:
            logger.debug(f"Run {filename} to generate image ...")

            py_path = os.path.join(PY_DIR, h2, f"{filename}.py")
            fig_path = os.path.join(IMG_DIR, h2)
            fig_name = os.path.join(fig_path, f"{filename}.{IMG_FMT}")

            if not os.path.exists(fig_path):
                os.makedirs(fig_path)

            generate_images_by_file(py_path, fig_name, dpi=IMG_DPI)
            i += 1

        logger.info(f"{i} pictures have been written into the directory {IMG_FMT}.")
