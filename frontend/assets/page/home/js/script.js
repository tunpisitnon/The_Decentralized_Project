window.addEventListener('DOMContentLoaded', async () => {
    document.getElementById('game').style.display = 'none';
    document.getElementById('profile').style.display = 'none';
    await connectMetamask();
});
const toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})

async function connectMetamask() {
    try {
        const provider = await detectEthereumProvider();
        if (!provider) {
            Swal.fire({
                icon: 'error',
                title: 'เกิดข้อผิดพลาด...',
                text: 'กรุณาเชื่อมต่อ Metamask!',
            })
        }
        const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
        const account_user = accounts[0];
        const data = {
            address: account_user
        };
        fetch('http://127.0.0.1:5000/wood/initial_player',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }, body: JSON.stringify(data)
        })
        .then(response => response.json()) // แปลง response เป็น JSON
        .then(data => {
            if (data.initial === true) {
            Swal.fire({
                title: 'ยินดีต้อนรับ!',
                icon: 'success',
                confirmButtonText: 'เข้าสู่หน้าเว็บ',
                textColor: 'black'
            })
        }
        })
        .catch(error => console.error(error));

        const balance = await ethereum.request({ method: 'eth_getBalance', params: [account_user, 'latest'] });
        const balanceNumber = Number.parseFloat(ethers.utils.formatEther(balance));
        const formattedBalance = balanceNumber.toFixed(2);
        document.getElementById('account2').innerHTML = `Account: ${account_user}`;
        document.getElementById('account3').innerHTML = `Balance: ${formattedBalance} ETH`;
        document.getElementById('balance').innerHTML = `Balance: ${formattedBalance} ETH`;
        document.getElementById('account').innerHTML = `Account: ${account_user}`;
        document.getElementById('connect-btn').style.display = 'none';
        document.getElementById('img-profile').innerHTML = `<img src="https://robohash.org/${account_user}?set=set3" alt="profile picture" style="width: 35px;">`;
        document.getElementById('img-profile2').innerHTML = `<img src="https://robohash.org/${account_user}?set=set3" alt="profile picture" style="width: 35px;">`;
        fetch('http://127.0.0.1:5000/wood/supply_left')
            .then(response => response.json())
            .then(data => {
                const woodSupplyLeft = data.wood_supply_left.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('Supply_left').innerHTML = `Total Supply: ${woodSupplyLeft} WOOD`;
            })
        fetch('http://127.0.0.1:5000/check_price_token')
            .then(response => response.json())
            .then(data => {
                document.getElementById('Check_price').innerHTML = `GPW To RDP: ${data.oneWoodToRainDrop} Price`;
            })
        return account_user;
    } catch (error) {
        Swal.fire({
            icon: 'error',
            title: 'เกิดข้อผิดพลาด...',
            text: 'กรุณาเชื่อมต่อ Metamask!',
        })
    }

}
function cutTree() {
    document.getElementById('cutTrees').disabled = true;
    connectMetamask().then(account_user => {
            const data = {
                address: account_user
            };
        fetch('http://127.0.0.1:5000/wood/check_player_status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json()) // แปลง response เป็น JSON
            .then(data => {
                // ดึงข้อมูลที่ต้องการจาก response
                const { mana } = data.player_status;
                if(mana > 1){
                const data = {
                    address: account_user
                };
                // ส่ง request แบบ POST พร้อม body
                fetch('http://127.0.0.1:5000/wood/cutting_wood', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                toast.fire({
                    iconHtml: '<img src="https://cdn-icons-png.flaticon.com/512/928/928746.png" width="70px">',
                    title: 'กำลังตัดต้นไม้',
                    text: 'รอสักครู่ ระบบกำลังทำการตัดต้นไม้',
                    background: '#fff1c1',
                })
                const sound = new Audio('../assets/sound/axe.mp3');
                sound.play();
                count = 0;
                const interval = setInterval(() => {
                    count++;
                    if (count === 5) {
                        clearInterval(interval);
                        toast.fire({
                            iconHtml: '<img src="https://cdn-icons-png.flaticon.com/512/928/928746.png" width="70px">',
                            title: 'ตัดต้นไม้สำเร็จ',
                            text: 'Wood Farm ได้เพิ่ม 1 ท่อน',
                            background: '#9DC08B',
                        })
                        document.getElementById('cutTrees').disabled = false;
                    }
                }, 1000);
            }else{
                const sound = new Audio('../assets/sound/axe.mp3');
                sound.play();
                count = 0;
                const interval = setInterval(() => {
                    count++;
                    if (count === 5) {
                        clearInterval(interval);
                        toast.fire({
                            iconHtml: '<img src="https://cdn-icons-png.flaticon.com/512/928/928746.png" width="70px">',
                            title: 'ไม่สามารถตัดไม้ได้',
                            text: 'Mana ไม่เพียงพอ',
                            background: '#9DC08B',
                        })
                        document.getElementById('cutTrees').disabled = false;
                    }
                }, 1000);
            }
            
        });
    });
}

function showStatus() {
    connectMetamask().then(account_user => {
        const data = {
            address: account_user
        };
        // ส่ง request แบบ POST พร้อม body
        fetch('http://127.0.0.1:5000/wood/check_player_status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json()) // แปลง response เป็น JSON
            .then(data => {
                // ดึงข้อมูลที่ต้องการจาก response
                const { mana, total, wood } = data.player_status;
                console.log(`Mana: ${mana}, Total: ${total}, Wood: ${wood}`);

                Swal.fire({
                    title: 'สถานะ',
                    html: `
                            <div class="row">
                                <div class="col-6">
                                    <img src="../assets/page/home/image/jackStatus.png" alt="Wood Farm" width="300px">
                                </div>
                                <div id="jackStatus" class="col-6">
                                    <h3 class="mt-4">ชื่อ: Jack</h3>
                                    <h3>เพศ: ชาย</h3>
                                    <h3>อายุ: 20 ปี</h3>
                                    <h3>พลัง: ${mana} Point</h3>
                                    <h3>จำนวนครั้งที่เคยตัด: ${total} Wood</h3>
                                    <h3>ท่อนไม้: ${wood} Wood</h3>
                                </div>
                            </div>
                        `,
                    showCloseButton: true,
                    showCancelButton: false,
                    showConfirmButton: false
                })
            })
            .catch(error => console.error(error));
            
        });
}   


function swap() {
    Swal.fire({
        title: 'Swap',
        input: 'text',
        inputLabel: 'จำนวนเหรียญ Swap ',
        inputPlaceholder: 'Swap',
        showCancelButton: true,
        confirmButtonText: 'ยืนยัน',
        cancelButtonText: 'ยกเลิก',
        textColor: 'black',
        inputValidator: (value) => {
            if (!value) {
                return 'กรุณาระบุจำนวนเหรียญที่ต้องการ Swap ';
            } else if (isNaN(value)) {
                return 'กรุณาระบุจำนวนเหรียญ เป็นตัวเลขเท่านั้น';
            }
        }
    }).then((result) => {
        if (result.isConfirmed) {
            const inputValue = result.value;
            console.log('จำนวนเหรียญ Swap :', inputValue);
        }
    });
}

function manaShop() {
    Swal.fire({
        title: 'ร้านค้าและ Mana',
        input: 'text',
        inputLabel: 'จำนวน Mana ที่ต้องการซื้อ',
        inputPlaceholder: 'Mana',
        showCancelButton: true,
        confirmButtonText: 'ยืนยัน',
        cancelButtonText: 'ยกเลิก',
        imageUrl: 'https://cdn-icons-png.flaticon.com/512/7320/7320924.png',
        imageWidth:150,
        imageHeight: 150,
        imageAlt: 'Mana Icon',
        inputValidator: (value) => {
            if (!value) {
                return 'กรุณาระบุจำนวน Mana ที่ต้องการซื้อ';
            } else if (isNaN(value)) {
                return 'กรุณาระบุจำนวน Mana เป็นตัวเลขเท่านั้น';
            }
        }
    }).then((result) => {
        if (result.isConfirmed) {
            const inputValue = result.value;
            console.log('จำนวน Mana:', inputValue);
        }
    });
    
}
