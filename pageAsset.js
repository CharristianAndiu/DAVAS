const imgGroupDiv = document.querySelector('.imgGroup');
const returnPage = () => {
    window.history.go(-1);
}
const renderAsset = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const params = urlParams.get('paper_id');
    const {paper_id,imgArray,eccelArray} = JSON.parse(sessionStorage.getItem(params));
    console.log(paper_id,imgArray,eccelArray);
    const fileName = `assets/output/${paper_id}`;
    if (imgArray!== null) {
        const title = document.createElement('h4');
        title.textContent='文章内部分图片';
        imgGroupDiv.appendChild(title);
        for (const imgSrc of imgArray) {
            createImg(`${fileName}/${imgSrc}`);
        }
    }
    if (eccelArray!==null) {
        fetch(`${fileName}/${eccelArray[0]}`) // 使用Fetch API获取文件数据
            .then(response => response.arrayBuffer())
            .then(buffer => {
                const workbook = XLSX.read(buffer, { type: 'array' }); // 使用SheetJS读取文件

                const sheetName = workbook.SheetNames[0]; // 获取第一个工作表的名称
                const sheetData = XLSX.utils.sheet_to_html(workbook.Sheets[sheetName]); // 将工作表转换为HTML表格

                const xlsxContainer = document.getElementById('xlsx-container');
                xlsxContainer.innerHTML = sheetData; // 将HTML表格渲染到容器中
            });
    }
}

const createImg = (src) => {
    const img = document.createElement('img');
    img.src = src;
    imgGroupDiv.appendChild(img);
}

renderAsset();