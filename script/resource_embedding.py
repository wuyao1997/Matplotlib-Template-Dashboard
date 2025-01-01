"""
Embed the resource files referenced in HTML in base64 encoding format, including:
1. referenced matplotlib images
2. referenced Python scripts
3. referenced notebook files
4. favicon
5. img in footer

将html中引用的资源文件以base64编码格式嵌入，包括：
1. 引用的 matplotlib 图片
2. 引用的 Python 脚本
3. 引用的 notebook 文件
4. 网页favicon
5. footer中的img元素

"""

import os
import base64
from bs4 import BeautifulSoup

from config import get_logger


logger = get_logger()


def embedding_resource(html_file: str, out_html_file: str):
    """将网页中引用的资源嵌入到文件中输出

    Args:
        html_file (str): 网页文件路径
    """
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    logger.info("Embedding favicon...")
    favicon_path = os.path.join(os.path.dirname(html_file), soup.find("link")["href"])
    with open(favicon_path, "rb") as f:
        favicon_data = f.read()
    favicon_base64 = base64.b64encode(favicon_data).decode("utf-8")
    soup.find("link")["href"] = f"data:image/x-icon;base64,{favicon_base64}"

    logger.info("Embedding image ...")
    for img in soup.find_all("img"):
        img_path = os.path.join(os.path.dirname(html_file), img["src"])

        logger.debug(f"Embedding {img_path} into html ...")

        with open(img_path, "rb") as f:
            img_data = f.read()

        img_base64 = base64.b64encode(img_data).decode("utf-8")
        img["src"] = f"data:image/jpeg;base64,{img_base64}"

    logger.info("Embedding Python files...")
    for button in soup.find_all("button"):
        if button.get("data-pycode"):
            pycode_path = os.path.join(
                os.path.dirname(html_file), button["data-pycode"]
            )

            logger.debug(f"Embedding {pycode_path} into html ...")

            with open(pycode_path, "r", encoding="utf-8") as f:
                pycode = f.read()
            button["data-pycode"] = pycode

    logger.info("Embedding notebook ...")
    for button in soup.find_all("button"):
        if button.get("data-notebook"):
            notebook_path = os.path.join(
                os.path.dirname(html_file), button["data-notebook"]
            )

            logger.debug(f"Embedding {notebook_path} into html ...")

            with open(notebook_path, "r", encoding="utf-8") as f:
                notebook = f.read()
            button["data-notebook"] = notebook

    with open(out_html_file, "w", encoding="utf-8") as f:
        f.write(str(soup))


if __name__ == "__main__":
    from config import tasks

    for task in tasks:
        logger.info(f"Run build task ****** {task['info']}")

        html_dir = os.path.join(task["project_dir"], task["build_dir"], "html")
        outfilename = f"{html_dir}/{task["outfilename"]}.html"

        embedding_resource(
            f"{html_dir}/index.html", outfilename
        )
        logger.info(f"{outfilename} has been generated.\n")
