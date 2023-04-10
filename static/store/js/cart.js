let updateBtns = document.getElementsByClassName('update-cart')
let badge = document.getElementById('cart-total')

if (user !== 'AnonymousUser') {
    if (badge !== null) {
        getTotalItem(user)
    }
}

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('USER:', user)
        if (user === 'AnonymousUser') {
            console.log('Not logged in')
        } else {
            updateOrderItem(productId, action)
        }
    })
}

function updateOrderItem(productId, action){
    console.log('User is logged in, sending data...')

    let url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
        .then((response)=>{
            return response.json()
    })
        .then((data) => {
            if (data.quantity === 0) {
                location.reload()
            } else {
                let itemquantity = "item-quantity" + productId
                let element = document.getElementById(itemquantity)
                if (element !== null) {
                    document.getElementById(itemquantity).textContent = data.quantity
                    document.getElementById("total-items").textContent = data.total_items
                }
            getTotalItem(user)
            }
        })

}

function getTotalItem(user){
    console.log('updating counter...')
    let url = "/basket/cart_counter/"
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'user': user})
    })
        .then((response)=>{
            return response.json()
    })
        .then((data) => {
            badge.textContent = data.count
            })
}
