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
    plt.style.use('default')
    plt.style.use(rcfile)

    fig, ax = plt.subplots(constrained_layout=True)

    ax.plot([1, 2, 3, 4, 3, 4, 5], marker="o", label="data: a")
    ax.plot([3, 4, 3, 2, 1, 2, 3], marker="s", label="data: b")

    ax.legend(loc=2)

    ax.set_xlabel("t (s)", fontweight="bold")
    ax.set_ylabel(r"$f$ (Hz)", fontweight="bold")

    fig.savefig(savefilename)
    plt.close()


if __name__ == "__main__":
    from config import tasks

    for task in tasks:
        logger.info(f"Run build task ****** {task['info']}")

        STYLE_DIR = os.path.join(task["project_dir"], task["style_dir"])
        style_list = get_style_in_dir(STYLE_DIR)

        # 使用style_list内容，生成保存文件的路径列表
        # 保存文件名字和style_list最后一级目录名相同
        fig_names = []
        for style in style_list:
            style_name = os.path.basename(os.path.dirname(style))
            fig_name = f"{style_name}.{task["image_format"]}"
            save_dir = os.path.join(
                task["project_dir"], task["build_dir"], task["image_format"], "mplstyle"
            )
            fig_names.append(f"{save_dir}/{fig_name}")

        i = 0
        for style, fig_name in zip(style_list, fig_names):
            if not os.path.exists(os.path.dirname(fig_name)):
                os.makedirs(os.path.dirname(fig_name))

            logger.debug(f"Build figure {fig_name}")
            gen_mplstyle_figure(style, fig_name)
            i += 1

        logger.info(f"{i} matplotlibrc files have been build finished.")
