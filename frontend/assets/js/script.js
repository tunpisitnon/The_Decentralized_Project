const container = document.querySelector('.HTML');
fetch('../assets/page/start/start.html')
        .then(response => response.text())
        .then(html => container.innerHTML = html);

// โหลดไฟล์ css ของหน้า start
const startStyle = document.createElement('link');
startStyle.rel = 'stylesheet';
startStyle.href = '../assets/page/start/css/style.css';
document.head.appendChild(startStyle);

// โหลดไฟล์ script ของหน้า start
const startScript = document.createElement('script');
startScript.src = '../assets/page/start/js/script.js';
document.head.appendChild(startScript);




