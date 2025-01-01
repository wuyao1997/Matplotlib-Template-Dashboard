"""
Execute Python scripts in the specified directory to generate pictures

执行指定目录下的 Python 脚本生成图片
"""

import os
from datetime import datetime

from config import get_logger


logger = get_logger()


def get_python_script_list(dir_path):
    """Get all Python script files under the specified directory

    获取指定目录下的所有Python脚本文件
    """
    python_script_list = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".py"):
                python_script_list.append(os.path.join(root, file))
    return python_script_list


# pylint: disable=redefined-outer-name
def generate_images_by_file(filename, image_format="png", dpi=200):
    """Read and execute the script in the specified file, and add a statement to save
    the picture at the end of the script

    读取并执行指定文件中的脚本，在脚本最后添加保存图片的语句
    """
    outfilename = filename.replace("python_scripts", image_format)
    outfilename = outfilename.replace(".py", f".{image_format}")

    script_mtime = datetime.fromtimestamp(os.path.getmtime(filename))
    image_mtime = (
        datetime.fromtimestamp(os.path.getmtime(outfilename))
        if os.path.exists(outfilename)
        else None
    )

    # Only update if the image file is newer than the script file
    if image_mtime is None or script_mtime > image_mtime:
        with open(filename, "r", encoding="utf-8") as file:
            script = file.read()

        # delete `plt.show()` to avoid blank images
        script = script.replace("plt.show()", "")

        # add `plt.savefig()` to save the image
        script += f"\nplt.savefig('{outfilename}', dpi={dpi})\nplt.close()"

        if not os.path.exists(os.path.dirname(outfilename)):
            os.makedirs(os.path.dirname(outfilename))

        try:
            # pylint: disable=exec-used
            exec(script)
        except Exception as e:  # pylint: disable=broad-except
            logger.error(f"Error when run {filename}: {e}")


if __name__ == "__main__":
    from config import tasks

    for task in tasks:
        logger.info(f"Run build task ****** {task['info']}")

        IMG_FMT = task["image_format"]
        IMG_DPI = task["image_dpi"]
        py_dir = os.path.join(task["project_dir"], task["build_dir"], "python_scripts")

        filenames = get_python_script_list(py_dir)

        i = 0
        for filename in filenames:
            filename = filename.replace("\\", "/")

            logger.debug(f"Run {filename} to generate image ...")

            generate_images_by_file(filename, image_format=IMG_FMT, dpi=IMG_DPI)
            i += 1

        logger.info(f"{i} pictures have been written into the directory {IMG_FMT}.")
