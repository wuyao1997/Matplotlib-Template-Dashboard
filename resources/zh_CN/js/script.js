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
