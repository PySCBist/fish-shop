let updateBtns = document.getElementsByClassName('update-cart')
let badge = document.getElementById('cart-total')

if (badge !== null) {
    getTotalItem()
}

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        let productId = this.dataset.product
        let action = this.dataset.action
        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateOrderItem(productId, action, updateBtns[i])
        }
    })
}

function updateOrderItem(productId, action, updateBtn){
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
                let itemquantity = "item-quantity-" + productId
                let element = document.getElementById(itemquantity)
                if (element !== null) {
                    document.getElementById(itemquantity).textContent = data.quantity
                    document.getElementById("total-items").textContent = data.total_items
                }
                else {
                    changeButton(updateBtn)
                }
            getTotalItem()
            }
        })

}

function getTotalItem(){
    let url = "/basket/cart_counter/"
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify()
    })
        .then((response)=>{
            return response.json()
    })
        .then((data) => {
            badge.textContent = data.count
            })
}

function changeButton(button){
    button.className = button.className.replace("btn-warning", "btn-outline-warning")
    button.textContent = 'В корзине'
    button.attributes[1]["nodeValue"] = "remove"
}

function addCookieItem(productId, action) {
    console.log('Not logged in...')

    if (action === 'add'){
        if (cart[productId] === undefined){
            cart[productId] = {'quantity': 1}
        }else {
            cart[productId]['quantity'] += 1
        }
    }
    if(action === 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('remove item')
            delete  cart[productId]
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    getTotalItem()
}