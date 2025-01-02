"""
Configuring build parameters

用于配置构建参数
"""

import logging
from os.path import abspath, join


zh_CN = dict(
    info="中文构建",
    lang="zh_CN",
    project_dir="..",
    notebook_dir="notebook",
    style_dir="style",
    build_dir="build",
    image_format="jpg",
    image_dpi=200,
    outfilename="matplotlib绘图模板",
    sub_dir=[  # 手动指定子目录的顺序
        "折线图",
        "条形图",
        "饼图",
        "散点图",
        "统计图",
        "正交网格场",
        "三角网格场",
        "其它绘图",
        "三维图像",
        "坐标系布局",
    ],
)


def get_task_params(tasks):
    """Get task parameters

    获取任务参数
    """
    task_params = []
    for task in tasks:
        param = task.copy()

        param["project_dir"] = abspath(param["project_dir"])
        param["notebook_dir"] = join(param["project_dir"], param["notebook_dir"])
        param["style_dir"] = join(param["project_dir"], param["style_dir"])
        param["build_dir"] = join(param["project_dir"], param["build_dir"])
        param["image_dir"] = join(
            param["build_dir"], f"{param['image_format']}-{param['image_dpi']}"
        )
        param["html_dir"] = join(param["build_dir"], "html")
        param["py_dir"] = join(param["build_dir"], "python_scripts")

        lang_path = join(param["project_dir"], "resources", param["lang"])
        param["header_path"] = join(lang_path, "html", "header.html")
        param["footer_path"] = join(lang_path, "html", "footer.html")
        param["css_path"] = join(lang_path, "css", "style.css")
        param["js_path"] = join(lang_path, "js", "script.js")

        task_params.append(param)

    return task_params


params = get_task_params([zh_CN])


def get_logger():
    """获取日志记录器"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler("build.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    console_formatter = logging.Formatter("%(levelname)s - %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
