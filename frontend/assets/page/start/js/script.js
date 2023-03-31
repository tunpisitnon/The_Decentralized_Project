let countdown = 3; // จำนวนวินาทีที่ต้องการนับถอยหลัง
const countdownTimer = setInterval(() => {
    console.log(countdown);
    countdown--;
    if (countdown === 0) {
        clearInterval(countdownTimer);
        const container = document.querySelector('.HTML');
        fetch('../assets/page/home/home.html')
            .then(response => response.text())
            .then(html => container.innerHTML = html);
        const style = document.createElement('link');
        style.rel = 'stylesheet';
        style.href = '../assets/page/home/css/style.css';
        document.head.appendChild(style);
        const script = document.createElement('script');
        script.src = '../assets/page/home/js/script.js';
        document.head.appendChild(script);
        const vendorScript = document.createElement('script');
        vendorScript.src = '../assets/page/home/assets/vendors/js/vendor.bundle.base.js';
        document.head.appendChild(vendorScript);
        const miscScript = document.createElement('script');
        miscScript.src = '../assets/page/home/assets/js/misc.js';
        document.head.appendChild(miscScript);
        const canvas = document.createElement('script');
        canvas.src = '../assets/page/home/assets/js/off-canvas.js';
        document.head.appendChild(canvas);
    }
}, 1000);


