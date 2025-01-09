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
const vscode = acquireVsCodeApi();
notebookButtons.forEach(button => {
    button.addEventListener('click', function () {
        vscode.postMessage({
            "id": this.id,
            "ipynb": this.dataset.text
        });
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
