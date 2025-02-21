document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', function (event) {
            event.preventDefault();

            const productId = this.closest('a').dataset.id;

            fetch(`/product/${productId}/`)
                .then(response => response.json())
                .then(data => {
                    let basePrice = data.variants.length > 0 ? parseFloat(data.variants[0].price) : 0;
                    let selectedExtras = new Set();
                    let selectedVariant = data.variants.length > 0 ? data.variants[0].id : null;

                    document.getElementById('productModalLabel').textContent = data.name;
                    document.getElementById('productName').textContent = data.name;
                    document.getElementById('productDescription').textContent = data.description;

                    const priceElement = document.getElementById('productPrice');
                    priceElement.textContent = `${basePrice.toFixed(2)} ${data.currency}`;
                    priceElement.classList.remove('text-secondary');
                    priceElement.classList.add('text-primary');

                    const carouselInner = document.querySelector('.carousel-inner');
                    carouselInner.innerHTML = '';

                    if (data.images.length > 0) {
                        data.images.forEach((url, index) => {
                            const item = document.createElement('div');
                            item.className = `carousel-item ${index === 0 ? 'active' : ''}`;
                            item.innerHTML = `<img src="${url}" class="d-block w-100 rounded" alt="Product Image">`;
                            carouselInner.appendChild(item);
                        });
                    } else {
                        carouselInner.innerHTML = `
                            <div class="carousel-item active">
                                <img src="https://via.placeholder.com/300" class="d-block w-100 rounded" alt="No Image Available">
                            </div>
                        `;
                    }

                    const sizeContainer = document.getElementById('productSizes');
                    sizeContainer.innerHTML = '';
                    data.variants.forEach((variant, index) => {
                        const button = document.createElement('button');
                        button.className = `btn btn-outline-primary size-btn ${index === 0 ? 'active' : ''}`;
                        button.textContent = variant.code;
                        button.dataset.variantId = variant.id;
                        button.dataset.price = variant.price;

                        button.addEventListener('click', () => {
                            basePrice = parseFloat(variant.price);
                            selectedVariant = variant.id;
                            updateTotalPrice();
                            document.querySelectorAll('.size-btn').forEach(btn => btn.classList.remove('active'));
                            button.classList.add('active');
                        });

                        sizeContainer.appendChild(button);
                    });

                    const ingredientsRow = document.getElementById('productIngredients');
                    ingredientsRow.innerHTML = '';
                    data.ingredients.forEach(ingredient => {
                        const col = document.createElement('div');
                        col.className = 'ingredient';
                        col.dataset.ingredientId = ingredient.id;
                        col.innerHTML = `
                            <img src="${ingredient.image || 'https://via.placeholder.com/80'}" class="img-thumbnail" alt="${ingredient.name}">
                            <p class="small">${ingredient.name}</p>
                            <span class="price-badge btn btn-outline-primary" data-price="${ingredient.price}">
                                +${ingredient.price} ${data.currency}
                            </span>
                        `;
                        const priceBadge = col.querySelector('.price-badge');
                        col.addEventListener('click', function () {
                            const ingredientId = parseInt(col.dataset.ingredientId);
                            if (selectedExtras.has(ingredientId)) {
                                selectedExtras.delete(ingredientId);
                                col.classList.remove('selected');
                                priceBadge.classList.remove('btn-primary', 'text-white');
                                priceBadge.classList.add('btn-outline-primary');
                            } else {
                                selectedExtras.add(ingredientId);
                                col.classList.add('selected');
                                priceBadge.classList.add('btn-primary', 'text-white');
                                priceBadge.classList.remove('btn-outline-primary');
                            }
                            updateTotalPrice();
                        });
                        ingredientsRow.appendChild(col);
                    });

                    function updateTotalPrice() {
                        let totalPrice = basePrice;
                        document.querySelectorAll('.ingredient.selected .price-badge').forEach(el => {
                            totalPrice += parseFloat(el.dataset.price);
                        });
                        priceElement.textContent = `${totalPrice.toFixed(2)} ${data.currency}`;
                    }

                    document.getElementById('addToCartBtn').onclick = () => {
                        const ingredientIds = [...selectedExtras].filter(id => !isNaN(id)); // Убираем NaN

                        fetch(`/cart/add/${productId}/`, {
                            method: "POST",
                            headers: {
                                "X-CSRFToken": getCookie("csrftoken"),
                                "Content-Type": "application/x-www-form-urlencoded"
                            },
                            body: new URLSearchParams({
                                variant_id: selectedVariant,
                                ingredient_ids: ingredientIds.length > 0 ? ingredientIds.join(",") : "",
                                quantity: 1
                            })
                        }).then(response => response.json())
                          .then(() => {
                              fetchCart(); // Обновляем корзину

                              // **Правильное закрытие модального окна**
                              let modalEl = document.getElementById('productModal');
                              let modalInstance = bootstrap.Modal.getInstance(modalEl);
                              if (modalInstance) {
                                  modalInstance.hide();
                              }

                              document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());

                              setTimeout(() => {
                                  document.getElementById('cartSidebar').classList.add("open");
                              }, 300);
                          })
                          .catch(error => console.error("Error adding to cart:", error));
                    };

                    new bootstrap.Modal(document.getElementById('productModal')).show();
                })
                .catch(error => console.error('Error fetching product data:', error));
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function fetchCart() {
    fetch("/cart/")
        .then(response => response.json())
        .then(data => {
            const cartCount = document.getElementById("cartCount");
            const cartItems = document.getElementById("cartItems");
            const cartTotal = document.getElementById("cartTotal");

            cartItems.innerHTML = "";
            let total = 0;

            if (data.cart.length === 0) {
                cartItems.innerHTML = `<p class="text-center text-muted">Your cart is empty.</p>`;
                cartTotal.textContent = "0.00 USD";
                cartCount.textContent = "0";
                return;
            }

            data.cart.forEach(item => {
                total += parseFloat(item.total_price);
                cartItems.innerHTML += `
                    <div class="cart-item">
                        <h6>${item.name} (${item.size})</h6>
                        <p>Quantity: ${item.quantity}</p>
                        <p>Price: $${item.total_price}</p>
                    </div>
                `;
            });

            cartTotal.textContent = `${total.toFixed(2)} USD`;
            cartCount.textContent = data.cart.length.toString();
        })
        .catch(error => console.error("Error fetching cart:", error));
}
