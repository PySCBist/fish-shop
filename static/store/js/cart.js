let updateBtns = document.getElementsByClassName('update-cart')
let badge = document.getElementById('cart-total')

if (badge !== null) {
    getTotalItem(user)
}

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        let productId = this.dataset.product
        let action = this.dataset.action
        if (user === 'AnonymousUser') {
            console.log('Not logged in')
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
                let itemquantity = "item-quantity" + productId
                let element = document.getElementById(itemquantity)
                if (element !== null) {
                    document.getElementById(itemquantity).textContent = data.quantity
                    document.getElementById("total-items").textContent = data.total_items
                }
                else {
                    changeButton(updateBtn)
                }
            getTotalItem(user)
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