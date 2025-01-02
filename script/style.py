"""Use matplotlibrc file to generate corresponding style images

使用 matplotlibrc 文件生成相应风格的图片
"""

import os

import matplotlib.pyplot as plt

from config import get_logger


logger = get_logger()


def get_style_in_dir(style_dir: str) -> list:
    """Get all the filenames in the specified directory that end with mplstyle

    获取指定目录下所有以 mplstyle 结尾的文件名，不递归查找
    """
    lst = []
    for file in os.listdir(style_dir):
        if file.endswith("mplstyle"):
            filename = os.path.splitext(file)[0]
            lst.append(filename)

    return lst


# pylint: disable=redefined-outer-name
def gen_mplstyle_figure(rcfile, savefilename):
    """build a figure using the given matplotlibrc file

    用给定的 matplotlibrc 文件生成一张图
    """
    plt.style.use("default")
    plt.style.use(rcfile)

    fig, ax = plt.subplots(constrained_layout=True)

    ax.plot([1, 2, 3, 4, 3, 4, 5], marker="o", label="data: a")
    ax.plot([3, 4, 3, 2, 1, 2, 3], marker="s", label="data: b")

    ax.legend(loc=2)

    ax.set_xlabel("t (s)", fontweight="bold")
    ax.set_ylabel(r"$f$ (Hz)", fontweight="bold")

    fig.savefig(savefilename)
    plt.close()


# pylint: disable=redefined-outer-name
def generate_stylebox(style_name, rcfile_path, image_path):
    """Generate the HTML code for the style box

    生成样式盒子的HTML代码
    """
    box_html = f"""
        <div class="box">
            <button id="{style_name}" class="mplrc-button"
            data-text="{rcfile_path}">{style_name}</button>
            <img src="{image_path}"
            alt="{style_name}">
            <button class="copy-button" data-text="{rcfile_path}" >Copy</button>
        </div>
    """
    return box_html


if __name__ == "__main__":
    from config import params

    for param in params:
        logger.info(f"Run build task ****** {param['info']}")

        style_names = get_style_in_dir(param["style_dir"])

        IMG_DIR = os.path.join(param["image_dir"], "mplstyle")
        IMG_FMT = param["image_format"]
        if not os.path.exists(IMG_DIR):
            os.makedirs(IMG_DIR)

        h2_title = os.path.basename(param["style_dir"])
        html_content = f"<h2>{h2_title}</h2>"

        i = 0
        for style_name in style_names:
            logger.debug(f"Build figure {style_name}")

            rcfile_path = os.path.join(param["style_dir"], style_name + ".mplstyle")
            fig_path = os.path.join(IMG_DIR, f"{style_name}.{IMG_FMT}")

            gen_mplstyle_figure(rcfile_path, fig_path)

            html_content += generate_stylebox(style_name, rcfile_path, fig_path)
            i += 1

        if not os.path.exists(param["html_dir"]):
            os.makedirs(param["html_dir"])

        outfilename = os.path.join(param["html_dir"], "mplstyle.html")
        with open(outfilename, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"{i} matplotlibrc files have been build finished.")
