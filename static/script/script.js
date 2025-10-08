var cart;
async function init() {
    var productData = {}
    await fetch('/products', {
        method: 'GET'
    })
        .then(response => response.json())
        .then(data => productData = data)
        .catch(error => console.error('Error:', error));
    console.log(productData)
    var products = productData.data.products.edges
    const productDiv = document.getElementById("allproducts")
    products.forEach(product => {
        console.log(product)
        const shortDescription = product.node.metafield ? product.node.metafield.value : '';
        const shopItem = document.createElement('div');
        shopItem.className = 'shop-item';

        const img = document.createElement('img');
        img.src = product.node.images.edges[0].node.src;
        shopItem.appendChild(img);

        const info = document.createElement('div');
        info.className = 'info';

        const itemName = document.createElement('span');
        itemName.id = 'item-name';
        itemName.textContent = product.node.title;
        info.appendChild(itemName);

        const itemDescription = document.createElement('p');
        itemDescription.id = 'item-description';
        itemDescription.innerHTML = shortDescription;
        info.appendChild(itemDescription);

        shopItem.appendChild(info);

        const button = document.createElement('button');
        button.className = 'add-to-basket';
        button.innerHTML = 'Add to basket <img src="/resources/images/icons/bag-full.svg">';

        shopItem.appendChild(button);
        productDiv.appendChild(shopItem);
        const productID = product.node.id.split("/").slice(-1).pop()
        const productLink = location.origin + `/product/${productID}`
        img.addEventListener("click", (e) => {
            location.href = productLink
        })
    })
    document.querySelectorAll(".shop-item>.add-to-basket").forEach(element => {
        element.addEventListener('mouseenter', function () {
            element.parentElement.querySelector('.info').classList.add('blurred');
        });

        element.addEventListener('mouseleave', function () {
            element.parentElement.querySelector('.info').classList.remove('blurred');
        });
    })
    cart = getCart();
}

init()
