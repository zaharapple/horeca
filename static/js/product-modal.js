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

                    const additivesRow = document.getElementById('productAdditives');
                    additivesRow.innerHTML = '';
                    data.additives.forEach(additive => {
                        const col = document.createElement('div');
                        col.className = 'additive';
                        col.dataset.additiveId = additive.id;
                        col.innerHTML = `
                            <img src="${additive.image || 'https://via.placeholder.com/80'}" class="img-thumbnail" alt="${additive.name}">
                            <p class="small">${additive.name}</p>
                            <span class="price-badge btn btn-outline-primary" data-price="${additive.price}">
                                +${additive.price} ${data.currency}
                            </span>
                        `;
                        const priceBadge = col.querySelector('.price-badge');
                        col.addEventListener('click', function () {
                            const additiveId = parseInt(col.dataset.additiveId);
                            if (selectedExtras.has(additiveId)) {
                                selectedExtras.delete(additiveId);
                                col.classList.remove('selected');
                                priceBadge.classList.remove('btn-primary', 'text-white');
                                priceBadge.classList.add('btn-outline-primary');
                            } else {
                                selectedExtras.add(additiveId);
                                col.classList.add('selected');
                                priceBadge.classList.add('btn-primary', 'text-white');
                                priceBadge.classList.remove('btn-outline-primary');
                            }
                            updateTotalPrice();
                        });
                        additivesRow.appendChild(col);
                    });

                    function updateTotalPrice() {
                        let totalPrice = basePrice;
                        document.querySelectorAll('.additive.selected .price-badge').forEach(el => {
                            totalPrice += parseFloat(el.dataset.price);
                        });
                        priceElement.textContent = `${totalPrice.toFixed(2)} ${data.currency}`;
                    }

                    document.getElementById('addToCartBtn').onclick = () => {
                        const additiveIds = [...selectedExtras].filter(id => !isNaN(id));

                        fetch(`/cart/add/${productId}/`, {
                            method: "POST",
                            headers: {
                                "X-CSRFToken": getCookie("csrftoken"),
                                "Content-Type": "application/x-www-form-urlencoded"
                            },
                            body: new URLSearchParams({
                                variant_id: selectedVariant,
                                additive_ids: additiveIds.length > 0 ? additiveIds.join(",") : "",
                                quantity: 1
                            })
                        }).then(response => response.json())
                          .then(() => {
                              fetchCart();

                              // Ensure modal is closed properly
                              const modalEl = document.getElementById('productModal');
                              const modalInstance = bootstrap.Modal.getInstance(modalEl);
                              if (modalInstance) {
                                  modalInstance.hide();
                              }

                              // Remove leftover modal backdrop
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

            if (!cartItems || !cartCount || !cartTotal) {
                console.error("Cart elements not found in DOM!");
                return;
            }

            cartItems.innerHTML = "";
            let total = 0;

            if (!data.cart || data.cart.length === 0) {
                cartItems.innerHTML = `<p class="text-center text-muted">Your cart is empty.</p>`;
                cartTotal.textContent = "0.00 USD";
                cartCount.textContent = "0";
                return;
            }

            data.cart.forEach(item => {
                total += parseFloat(item.total_price);
                cartItems.innerHTML += `
                    <div class="cart-item">
                        <h6>${item.name} (Size: ${item.size})</h6>
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

document.addEventListener("DOMContentLoaded", function () {
    fetchCart();
});
