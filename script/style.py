"""Use matplotlibrc file to generate corresponding style images

使用 matplotlibrc 文件生成相应风格的图片
"""

import os

import matplotlib.pyplot as plt

from config import get_logger


logger = get_logger()


def get_style_in_dir(style_dir: str) -> list:
    """Get the matplotlibrc file in the subdirectory

    如果子目录中包含 matplotlibrc 文件，则返回matplotlibrc路径
    """
    lst = []
    for root, _, files in os.walk(style_dir):
        if "matplotlibrc" in files:
            lst.append(os.path.join(root, "matplotlibrc"))

    return lst


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


def generate_stylebox(filename, image_format):
    """Generate the HTML code for the style box

    生成样式盒子的HTML代码
    """
    matplotlibrc = f"../../style/{filename}/matplotlibrc"
    img_src = f"../{image_format}/mplstyle/{filename}.{image_format}"
    logger.debug(f"Generating div of {filename}...")

    box_html = f"""
        <div class="box">
            <button id="{filename}" class="mplrc-button"
            data-text="{matplotlibrc}">{filename}</button>
            <img src="{img_src}"
            alt="{filename}">
            <button class="copy-button" data-text="{matplotlibrc}" >Copy</button>
        </div>
    """
    return box_html


if __name__ == "__main__":
    from config import tasks

    for task in tasks:
        logger.info(f"Run build task ****** {task['info']}")

        STYLE_DIR = os.path.join(task["project_dir"], task["style_dir"])
        style_list = get_style_in_dir(STYLE_DIR)

        fig_names = []
        for style in style_list:
            style_name = os.path.basename(os.path.dirname(style))
            fig_name = f"{style_name}.{task["image_format"]}"
            save_dir = os.path.join(
                task["project_dir"], task["build_dir"], task["image_format"], "mplstyle"
            )
            fig_names.append(f"{save_dir}/{fig_name}")

        i = 0
        html_content = f"<h2>{task['style_dir']}</h2>"
        for style, fig_name in zip(style_list, fig_names):
            if not os.path.exists(os.path.dirname(fig_name)):
                os.makedirs(os.path.dirname(fig_name))

            logger.debug(f"Build figure {fig_name}")
            gen_mplstyle_figure(style, fig_name)

            # 获取style的最后一个文件夹名，不是文件名
            style_name = os.path.basename(os.path.dirname(style))
            html_content += generate_stylebox(style_name, task["image_format"])
            i += 1

        outdir = os.path.join(
            task["project_dir"], task["build_dir"], "html", "mplstyle.html"
        )
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        with open(outdir, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"{i} matplotlibrc files have been build finished.")
