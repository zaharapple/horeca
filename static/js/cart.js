document.addEventListener("DOMContentLoaded", function () {
    const cartIcon = document.getElementById("cartIcon");
    const cartSidebar = document.getElementById("cartSidebar");
    const closeCart = document.getElementById("closeCart");
    const cartItems = document.getElementById("cartItems");
    const cartCount = document.getElementById("cartCount");
    const cartTotal = document.getElementById("cartTotal");

    function fetchCart() {
        fetch("/cart/")
            .then(response => response.json())
            .then(data => updateCartDisplay(data.cart))
            .catch(error => console.error("Error fetching cart:", error));
    }

    function updateCartDisplay(cart) {
        cartItems.innerHTML = "";
        let total = 0;

        if (cart.length === 0) {
            cartItems.innerHTML = `<p class="text-center text-muted">Your cart is empty.</p>`;
            cartTotal.textContent = "0.00 USD";
            cartCount.textContent = "0";
            return;
        }

        cart.forEach(item => {
            total += item.total_price;
            cartItems.innerHTML += `
                <div class="cart-item">
                    <h6>${item.name} (${item.size})</h6>
                    <p>Additives: ${item.additives.join(", ") || "None"}</p>
                    <p>Price: $${item.total_price.toFixed(2)}</p>
                    <div class="cart-controls">
                        <button class="btn btn-sm btn-outline-primary change-qty" data-id="${item.id}" data-action="decrease">-</button>
                        <span>${item.quantity}</span>
                        <button class="btn btn-sm btn-outline-primary change-qty" data-id="${item.id}" data-action="increase">+</button>
                        <button class="btn btn-sm btn-outline-danger remove-item" data-id="${item.id}">×</button>
                    </div>
                </div>
            `;
        });

        cartTotal.textContent = `${total.toFixed(2)} USD`;
        cartCount.textContent = cart.length.toString();
    }

    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("remove-item")) {
            fetch(`/cart/remove/${event.target.dataset.id}/`, { method: "POST" })
                .then(() => fetchCart());
        }
    });

    cartIcon.addEventListener("click", () => {
        cartSidebar.classList.toggle("open");
    });

    closeCart.addEventListener("click", () => {
        cartSidebar.classList.remove("open");
    });

    fetchCart();
});
