
let makeOrderBtn = document.getElementsByClassName('make-order')
if (makeOrderBtn > 0){
    makeOrderBtn[0].addEventListener('click', function (){
    if(user === 'AnonymousUser'){
        console.log('Not logged in')
    }else {
        makeOrder()
    }
    })
}


function makeOrder() {
    let url = '/make_order/'
    let f = document.getElementById('address')
    let d = document.getElementById('delivery_date')
    const address = f.value;
    const date = d.value;
    if (!isNaN(address) * !isNaN(date)) {
        fetch(url, {
            method: 'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'address': address, 'date': date})
        })
            .then((response)=>{
                return response.json()
        })
            .then((data) => {
                console.log('Result:', data);
                window.location.href = "/orders/"
            })
    }
    else {
        alert("Выберите дату и адрес доставки")
    }
}