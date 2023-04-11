
let makeOrderBtn = document.getElementsByClassName('make-order')
makeOrderBtn[0].addEventListener('click', function (){
    console.log('USER:', user)
    if(user === 'AnonymousUser'){
        console.log('Not logged in')
    }else {
        makeOrder()
    }
    })

function makeOrder(){
    console.log('Making order...')
    let url = '/make_order/'
    let f = document.getElementById('address')
    const address = f.value;
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'address': address})
    })
        .then((response)=>{
            return response.json()
    })
        .then((data) => {
            console.log('Result:', data);
            window.location.href = "/orders/"
        })
}