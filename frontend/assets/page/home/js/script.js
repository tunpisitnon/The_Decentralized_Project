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

const toast2 = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 5000,
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
        const accounts = await ethereum.request({method: 'eth_requestAccounts'});
        const account_user = accounts[0];
        const data = {
            address: account_user
        };
        fetch('http://127.0.0.1:5000/wood/initial_player', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }, body: JSON.stringify(data)
        })
            .then(response => response.json()) // แปลง response เป็น JSON
            .then((data) => {
                if (data.initial === true) {
                    toast.fire({
                        icon: 'success',
                        title: 'ยินดีต้อนรับเข้าสู่ Wood Farm',
                        text: 'เริ่มต้นเกมส์ได้เลย',
                        background: '#9DC08B',
                    })
                } else {
                    toast.fire({
                        icon: 'success',
                        title: 'ยินดีต้อนรับกลับมา',
                        text: 'เริ่มเล่นเกมส์ได้เลย',
                        background: '#9DC08B',
                    })
                }
            }).then(() => {
            console.log('เชื่อมต่อ Metamask สำเร็จ');
        })

        const balance = await ethereum.request({method: 'eth_getBalance', params: [account_user, 'latest']});
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
//     check player status
    connectMetamask().then(account_user => {
        fetch('http://127.0.0.1:5000/wood/check_player_status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"address": account_user})
        })
            .then(response => response.json()) // แปลง response เป็น JSON
            .then((data) => {
                if (data['player_status']['mana'] > 0) {
                    fetch('http://127.0.0.1:5000/wood/cutting_wood', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({"address": account_user})
                    }).then(() => {
                        const sound = new Audio('../assets/sound/axe.mp3');
                        sound.play();
                        toast2.fire({
                            iconHtml: '<img src="https://cdn-icons-png.flaticon.com/512/928/928746.png" width="70px">',
                            title: 'กำลังตัดต้นไม้',
                            text: 'รอสักครู่ ระบบกำลังทำการตัดต้นไม้',
                            background: '#d9b28d',
                        })
                        setTimeout(async () => {
                            const sound2 = new Audio('../assets/sound/pickup_item.mp3');
                            await sound2.play();
                            toast2.fire({
                                iconHtml: '<img src="https://cdn-icons-png.flaticon.com/512/928/928746.png" width="70px">',
                                title: 'ตัดต้นไม้สำเร็จ',
                                text: 'รับเหรียญ WOOD แล้ว',
                                background: '#9DC08B',
                            });
                            document.getElementById('cutTrees').disabled = false;
                        }, 5000)
                    })
                } else {
                    const sound = new Audio('../assets/sound/sigh.wav');
                    sound.play();
                    toast2.fire({
                        icon: 'error',
                        title: 'ไม่สามารถตัดต้นไม้ได้',
                        text: 'นั่งพักซักหน่อยไหม?',
                        background: '#9DC08B',
                    })
                    setTimeout(() => {
                        document.getElementById('cutTrees').disabled = false;
                    }, 5000)
                }
            });
    })
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
                const {mana, total, wood, Raindrops} = data.player_status;
                console.log(`Mana: ${mana}, Total: ${total}, Wood: ${wood}, Raindrops: ${Raindrops}`);

                Swal.fire({
                    title: 'Status',

                    html: ` <div class="container">
                                <div class="row">
                                    <div class="col-8">
                                        <img src="https://cdn-icons-png.flaticon.com/512/1597/1597159.png" class="img-fluid rounded" alt="Player Image">
                                    </div>
                                    <div class="col-4 align-self-start">
                                        <p><strong>Mana:</strong> ${mana}</p>
                                        <p><strong>Total:</strong> ${total}</p>
                                        <p><strong>Wood:</strong> ${wood}</p>
                                        <p><strong>Raindrops:</strong> ${Raindrops}</p>
                                    </div>
                                </div>
                            </div>           
                        `,
                    showCancelButton: false,
                    confirmButtonText: 'ตกลง',

                })
            })
            .catch(error => console.error(error));

    });
}


function swap() {
    connectMetamask().then(account_user => {
        fetch('http://127.0.0.1:5000/wood/check_player_status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"address": account_user})
        }).then(response => response.json()) // แปลง response เป็น JSON
            .then((data) => {
                const {wood} = data.player_status;
                Swal.fire({
                    title: 'แลกเปลี่ยน WOOD',
                    html:
                        `<div class="container">
                              <label for="woodInput" class="form-label">กรุณาระบุจำนวน WOOD ที่ต้องการแลก</label>
                              <div class="input-group mb-3">
                                <input type="text" class="form-control" id="woodInput" placeholder="WOOD">
                                <span class="input-group-text" onclick="document.getElementById('woodInput').value = '${wood}'">Balance = ${wood}</span>
                              </div>
                            </div>
                              `,
                    showCancelButton: true,
                    confirmButtonText: 'ยืนยัน',
                    cancelButtonText: 'ยกเลิก',
                    imageUrl: 'https://cdn-icons-png.flaticon.com/512/928/928746.png',
                    imageWidth: 100,
                    imageHeight: 100,
                    imageAlt: 'WOOD Icon'
                }).then((result) => {
                    if (result.isConfirmed) {
                        const woodInput = document.getElementById('woodInput').value;
                        if (woodInput <= wood) {
                            fetch('http://127.0.0.1:5000/wood/spending_wood', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({
                                    "address": account_user,
                                    "value": woodInput
                                })
                            }).then(r => r.json())
                                .then((data) => {
                                    console.log(data);
                                    if (data.status === 'success') {
                                        Swal.fire({
                                            title: 'แลกเปลี่ยน WOOD',
                                            text: 'แลกเปลี่ยน WOOD เป็น Raindrops สำเร็จ',
                                            icon: 'success',
                                            confirmButtonText: 'ตกลง'
                                        })
                                    } else {
                                        Swal.fire({
                                            title: 'แลกเปลี่ยน WOOD',
                                            text: 'แลกเปลี่ยน WOOD เป็น Raindrops ไม่สำเร็จ',
                                            icon: 'error',
                                            confirmButtonText: 'ตกลง'
                                        })
                                    }
                                })
                        }
                    }
                })
            })
    });
}

function manaShop() {
     connectMetamask().then(account_user => {
        fetch('http://127.0.0.1:5000/wood/check_player_status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"address": account_user})
        }).then(response => response.json()) // แปลง response เป็น JSON
            .then((data) => {
                const {Raindrops} = data.player_status;
                Swal.fire({
                    title: 'แลกเปลี่ยน Raindrops ให้เป็น Mana',
                    html:
                        `<div class="container">
                              <label for="woodInput" class="form-label">กรุณาระบุจำนวน Raindrop ที่ต้องการแลก</label>
                              <div class="input-group mb-3">
                                <input type="text" class="form-control" id="RaindropInput" placeholder="Raindrops">
                                <span class="input-group-text" onclick="document.getElementById('RaindropInput').value = '${Raindrops}'">Balance = ${Raindrops}</span>
                              </div>
                            </div>
                              `,
                    showCancelButton: true,
                    confirmButtonText: 'ยืนยัน',
                    cancelButtonText: 'ยกเลิก',
                    imageUrl: 'https://cdn-icons-png.flaticon.com/512/7320/7320924.png',
                    imageWidth: 100,
                    imageHeight: 100,
                })
            })
    });
}
