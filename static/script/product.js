async function init() {
    console.log("initialized.")
    const cartButton = document.querySelector("#cart_button");
    var cart;
    cart = getCart();
    cartButton.addEventListener("click", e => {

    })

    var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function () {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                this.querySelector(".expandable-indicator").innerHTML = "+"
                content.style.display = "none";
            } else {
                this.querySelector(".expandable-indicator").innerHTML = "-"
                content.style.display = "block";
            }
        });
    }
}
window.addEventListener('load', init)