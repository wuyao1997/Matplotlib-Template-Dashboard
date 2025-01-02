"""
Generate HTML pages according to the file structure of the specified directory

根据指定目录的文件结构生成 HTML 页面
"""

import os

from config import get_logger


logger = get_logger()


# pylint: disable=too-many-arguments
def build_html(
    body, header_path, footer_path, js_path, css_path, language, project_dir
):
    """Generate an HTML page"""
    text = f"""<!DOCTYPE html>\n<html lang="{language}">"""

    with open(header_path, "r", encoding="utf-8") as file:
        header_text = file.read()
        header_text = header_text.replace("${project_dir}", project_dir)

    with open(footer_path, "r", encoding="utf-8") as file:
        footer_text = file.read()
        footer_text = footer_text.replace("${project_dir}", project_dir)

    with open(css_path, "r", encoding="utf-8") as file:
        css_text = file.read()

    with open(js_path, "r", encoding="utf-8") as file:
        js_text = file.read()

    return f"""{text}
        <head>
            {header_text}
            <style>
                {css_text}
            </style>
        </head>
        <body>
            {body}
            {footer_text}
            <script>
                {js_text}
            </script>
        </body>
    </html>
    """


def template_boxs(h2, nb_dir, py_dir, img_dir, image_format):
    """Generate the HTML code for the template box

    生成模板盒子的HTML代码
    """
    box_html = f"<h2>{h2}</h2>\n"
    h2_path = os.path.join(nb_dir, h2)

    # 遍历 h2_path 文件夹下的所有ipynb文件，不递归查找子文件夹
    for file in os.listdir(h2_path):
        if file.endswith(".ipynb"):
            filename = os.path.splitext(file)[0]
            logger.debug(f"Generating div of {filename} ...")

            pyfile = os.path.join(py_dir, h2, f"{filename}.py")
            nbfile = os.path.join(nb_dir, h2, f"{filename}.ipynb")
            imgfile = os.path.join(img_dir, h2, f"{filename}.{image_format}")

            box_html += f"""<div class="box">
                <button id="{filename}" class="notebook-button"
                data-text="{nbfile}">{filename}</button>
                <img src="{imgfile}"
                alt="{filename}">
                <button class="copy-button" data-text="{pyfile}" >Copy</button>
                </div>"""

    return box_html


# pylint: disable=dangerous-default-value
# pylint: disable=too-many-arguments
def html_body(nb_dir, html_dir, py_dir, img_dir, image_format="png", h2_order=[]):
    """Generate an HTML page

    生成HTML页面
    """
    text = '<div class="container" id="notebook">\n'

    # process sub_dir in h2_order
    for h2 in h2_order:
        h2_path = os.path.join(nb_dir, h2)
        if os.path.exists(h2_path) and os.path.isdir(h2_path):
            text += template_boxs(h2, nb_dir, py_dir, img_dir, image_format)
        else:
            logger.warning(f"Directory {h2} not found. Skipping.")

    # load mplstyle.html to insert
    mplsyle_html_path = os.path.join(html_dir, "mplstyle.html")
    if os.path.exists(mplsyle_html_path):
        with open(mplsyle_html_path, "r", encoding="utf-8") as file:
            text += file.read()
    else:
        logger.warning(f"File {mplsyle_html_path} not found. Skipping.")

    text += "\n</div>"
    return text


if __name__ == "__main__":
    from config import params

    for param in params:
        logger.info(f"Run build task ****** {param['info']}")

        sub_dir = param["sub_dir"]
        NB_DIR = param["notebook_dir"]
        IMG_FMT = param["image_format"]
        IMG_DIR = param["image_dir"]
        PY_DIR = param["py_dir"]
        HTML_DIR = param["html_dir"]
        if not os.path.exists(HTML_DIR):
            os.makedirs(HTML_DIR)

        body_text = html_body(
            NB_DIR, HTML_DIR, PY_DIR, IMG_DIR, image_format=IMG_FMT, h2_order=sub_dir
        )

        html_text = build_html(
            body_text,
            param["header_path"],
            param["footer_path"],
            param["js_path"],
            param["css_path"],
            param["lang"],
            param["project_dir"],
        )

        outfilename = os.path.join(HTML_DIR, "index.html")
        with open(outfilename, "w", encoding="utf-8") as f:
            f.write(html_text)
            logger.info(f"{HTML_DIR}/index.html has been generated.")
