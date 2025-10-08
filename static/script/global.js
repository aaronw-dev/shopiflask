function getCart() {
    let cartEntry = localStorage.getItem("hcs_cart");
    if (cartEntry == null) {
        let newCart = JSON.stringify({});
        cartEntry = newCart
        localStorage.setItem("hcs_cart", newCart);
    }
    return cartEntry
}