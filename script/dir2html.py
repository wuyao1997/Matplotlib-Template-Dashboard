"""
Generate HTML pages according to the file structure of the specified directory

根据指定目录的文件结构生成 HTML 页面
"""

import os

from config import get_logger


logger = get_logger()


STYLE = """<style>
    body {
        background-color: #1e1e1e;
    }

    h2 {
        text-align: center;
        width: 100vw;
        margin: 0;
        background-color: #0e639c;
        color: white;
    }

    .container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }

    .box {
        width: 240px;
        height: 220px;
        margin: 10px;
        margin-top: 20px;
        text-align: center;
        background-color: #929292;
        position: relative;
    }

    .box img {
        width: auto;
        height: 88%;
        max-height: 100%;
        max-width: 100%;
    }

    button {
        border: none;
        margin-bottom: 0px;
        width: 100%;
        text-align: center;
        outline: 1px solid transparent;
        outline-offset: 2px !important;
        color: white;
        background: #0e639c;
        font-size: 16px;
    }

    button:hover {
        cursor: pointer;
        background: #1a8dda;
    }

    .copy-button {
        position: absolute;
        bottom: 0px;
        right: 0px;
        width: 40%;
        height: auto;
    }

    footer {
        background-color: #333;
        color: #fff;
        padding: 20px 0;
    }

    .footer-content,
    .footer-bottom {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }

    .footer-content {
        margin-left: 20px;
    }

    .social-icons,
    .footer-bottom p {
        margin: 0;
    }

    .social-icons a {
        margin-right: 15px;
    }

    .social-icons img {
        width: 24px;
        height: 24px;
    }

    .footer-bottom {
        border-top: 1px solid #444;
        padding-top: 10px;
        margin-left: auto;
    }
</style>
"""

HEADER = f"""<!DOCTYPE html>
<html lang="zh_CN">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<head><title>matplotlib绘图模板</title>
<link rel="icon" href="../../resources/logo/matplotlib制图师.t.png" type="image/x-icon">
{STYLE}
"""


FOOTER = """\n
<footer>
<div class="container">
<div class="footer-content">
<div class="social-icons">
<a href="https://space.bilibili.com/3546387249629871" target="_blank"><img
        src="../../resources/logo/bili.png" alt="哔哩哔哩"></a>
<a href="https://www.wolai.com/matplotlib/uecbhR3MHhaZkK55za779h" target="_blank">
    <img src="../../resources/logo/matplotlib制图师.t.png" alt="我来"></a>
<a href="https://mp.weixin.qq.com/s/K8EqXk0j5XuHXMVb9Mc4Hw" target="_blank">
    <img src="../../resources/logo/weixin.png" alt="微信公众号"></a>
<a href="https://github.com/wuyao1997/Matplotlib-Template-Dashboard" target="_blank">
    <img src="../../resources/logo/github-mark-white.png" alt="github主页"></a>
<a href="https://marketplace.visualstudio.com/items?itemName=litchi.plt-snippet"
    target="_blank">
    <img src="../../resources/logo/vscode.png" alt="VS Code插件页"></a>
<a href="https://matplotlib.org" target="_blank">
    <img src="../../resources/logo/matplotlib.logo.png" alt="matplotlib官网"></a>
</div>
</div>
<div class="footer-bottom">
<p>&copy; 2024-2025 matplotlib制图师</p>
</div>
</div>
</footer>
"""

JS = """\n
<script>
    const copyButtons = document.querySelectorAll('.copy-button');
    let lastClickedCopyButton = null;

    copyButtons.forEach(button => {
        button.addEventListener('click', function () {
            const text = this.getAttribute('data-text');
            navigator.clipboard.writeText(text)
                .then(() => {
                    //alert("拷贝成功");
                    this.textContent = "Copied!";
                    if (lastClickedCopyButton && lastClickedCopyButton !== this) {
                        lastClickedCopyButton.textContent = "Copy";
                    }
                    lastClickedCopyButton = this;
                    console.log('Python Code has been copied to clipboard!');
                })
                .catch(err => {
                    //alert(err);
                    this.textContent = "Failed!";
                    console.error('Unable to copy Python Code to the clipboard.', err);
                })
        });
    });

    const notebookButtons = document.querySelectorAll('.notebook-button');
    notebookButtons.forEach(button => {
        button.addEventListener('click', function () {
            const defaultFileName = this.textContent;
            const fileName = prompt('下载 notebook 脚本为文件（不含后缀名）：', defaultFileName);

            if (fileName) {
                const fileContent = this.getAttribute('data-text');
                const blob = new Blob([fileContent], { type: 'application/json' });
                const url = URL.createObjectURL(blob);

                const a = document.createElement('a');
                a.href = url;
                a.download = `${fileName}.ipynb`;
                a.click();

                URL.revokeObjectURL(url);
            }
        });
    });

    const mplrcButtons = document.querySelectorAll('.mplrc-button');
    mplrcButtons.forEach(button => {
        button.addEventListener('click', function () {
            const style_name = this.textContent;

            const fileContent = this.getAttribute('data-text');
            const blob = new Blob([fileContent], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = `${style_name}.matplotlibrc`;
            a.click();

            URL.revokeObjectURL(url);
        });
    });
</script>
"""


def generate_templatebox(directory, filename, image_format, pyfile):
    """Generate the HTML code for the template box

    生成模板盒子的HTML代码
    """
    notebook_src = f"../../notebook/{directory}/{filename}.ipynb"
    img_src = f"../{image_format}/{directory}/{filename}.{image_format}"

    logger.debug(f"Generating div of {notebook_src} ...")

    box_html = f"""
        <div class="box">
            <button id="{filename}" class="notebook-button"
            data-text="{notebook_src}">{filename}</button>
            <img src="{img_src}"
            alt="{filename}">
            <button class="copy-button" data-text="{pyfile}" >Copy</button>
        </div>
    """
    return box_html


# pylint: disable=dangerous-default-value
def generate_html(directory, outdir, image_format="png", h2_order=[]):
    """Generate an HTML page

    生成HTML页面
    """
    html_content = HEADER
    html_content += '<div class="container" id="notebook">\n'

    # process sub_dir in h2_order
    for dirname in h2_order:
        dir_path = os.path.join(directory, dirname)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            html_content += f"<h2>{dirname}</h2>"
            for root, _, files in os.walk(dir_path):
                for file in files:
                    if file.endswith(".ipynb"):
                        filename = os.path.splitext(file)[0]

                        pyfile = f"../python_scripts/{dirname}/{filename}.py"

                        templatebox = generate_templatebox(
                            dirname, filename, image_format, pyfile
                        )
                        html_content += templatebox
        else:
            logger.warning(f"Directory {dirname} not found. Skipping.")

    # process other sub_dir
    for root, _, files in os.walk(directory):
        dirname = os.path.relpath(root, directory)
        if dirname != "." and dirname not in h2_order:
            html_content += f"<h2>{dirname}</h2>"
            for file in files:
                if file.endswith(".ipynb"):
                    filename = os.path.splitext(file)[0]

                    pyfile = f"../python_scripts/{dirname}/{filename}.py"

                    templatebox = generate_templatebox(
                        dirname, filename, image_format, pyfile
                    )
                    html_content += templatebox

    # load mplstyle.html to insert
    with open(f"{outdir}/mplstyle.html", "r", encoding="utf-8") as file:
        html_content += file.read()

    html_content += f"\n</div>\n{FOOTER}\n{JS}</body></html>"

    with open(f"{outdir}/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)


if __name__ == "__main__":
    from config import tasks

    for task in tasks:
        logger.info(f"Run build task ****** {task['info']}")

        sub_dir = task["sub_dir"]
        NB_DIR = os.path.join(task["project_dir"], task["notebook_dir"])
        IMG_FMT = task["image_format"]
        html_dir = os.path.join(task["project_dir"], task["build_dir"], "html")

        generate_html(NB_DIR, html_dir, image_format=IMG_FMT, h2_order=sub_dir)

        logger.info(f"{html_dir}/index.html has been generated.")
