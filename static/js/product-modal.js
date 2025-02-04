document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', function (event) {
            event.preventDefault();

            const productId = this.closest('a').dataset.id;

            fetch(`/product/${productId}/`)
                .then(response => response.json())
                .then(data => {
                    let basePrice = data.variants.length > 0 ? parseFloat(data.variants[0].price) : 0;
                    let selectedExtras = new Set(); // Храним выбранные ингредиенты

                    // Обновляем заголовок и описание
                    document.getElementById('productModalLabel').textContent = data.name;
                    document.getElementById('productName').textContent = data.name;
                    document.getElementById('productDescription').textContent = data.description;

                    // Обновляем цену (по умолчанию первый размер)
                    const priceElement = document.getElementById('productPrice');
                    priceElement.textContent = `${basePrice.toFixed(2)} ${data.currency}`;
                    priceElement.classList.remove('text-secondary');
                    priceElement.classList.add('text-primary');

                    // Обновляем карусель изображений
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

                    // Обновляем размеры продукта
                    const sizeContainer = document.getElementById('productSizes');
                    sizeContainer.innerHTML = '';
                    data.variants.forEach((variant, index) => {
                        const button = document.createElement('button');
                        button.className = `btn btn-outline-primary size-btn ${index === 0 ? 'active' : ''}`;
                        button.textContent = variant.code;
                        button.dataset.price = variant.price;

                        button.addEventListener('click', () => {
                            basePrice = parseFloat(variant.price);
                            updateTotalPrice();
                            document.querySelectorAll('.size-btn').forEach(btn => btn.classList.remove('active'));
                            button.classList.add('active');
                        });

                        sizeContainer.appendChild(button);
                    });

                    // Обновляем ингредиенты
                    const ingredientsRow = document.getElementById('productIngredients');
                    ingredientsRow.innerHTML = '';
                    data.ingredients.forEach(ingredient => {
                        const col = document.createElement('div');
                        col.className = 'ingredient';
                        col.innerHTML = `
                            <img src="${ingredient.image || 'https://via.placeholder.com/80'}" class="img-thumbnail" alt="${ingredient.name}">
                            <p class="small">${ingredient.name}</p>
                            <span class="price-badge btn btn-outline-primary" data-price="${ingredient.price}">
                                +${ingredient.price} ${data.currency}
                            </span>
                        `;
                        const priceBadge = col.querySelector('.price-badge');
                        col.addEventListener('click', function () {
                            if (selectedExtras.has(ingredient.name)) {
                                selectedExtras.delete(ingredient.name);
                                col.classList.remove('selected');
                                priceBadge.classList.remove('btn-primary', 'text-white');
                                priceBadge.classList.add('btn-outline-primary');
                            } else {
                                selectedExtras.add(ingredient.name);
                                col.classList.add('selected');
                                priceBadge.classList.add('btn-primary', 'text-white');
                                priceBadge.classList.remove('btn-outline-primary');
                            }
                            updateTotalPrice();
                        });
                        ingredientsRow.appendChild(col);
                    });

                    // Функция для обновления цены
                    function updateTotalPrice() {
                        let totalPrice = basePrice;
                        document.querySelectorAll('.ingredient.selected .price-badge').forEach(el => {
                            totalPrice += parseFloat(el.dataset.price);
                        });
                        priceElement.textContent = `${totalPrice.toFixed(2)} ${data.currency}`;
                    }

                    // Добавление в корзину
                    document.getElementById('addToCartBtn').onclick = () => {
                        console.log("Добавлено в корзину:", {
                            product: data.name,
                            size: document.querySelector('.size-btn.active').textContent,
                            ingredients: [...selectedExtras],
                            totalPrice: `${priceElement.textContent}`
                        });
                    };

                    // Открываем модальное окно
                    new bootstrap.Modal(document.getElementById('productModal')).show();
                })
                .catch(error => console.error('Error fetching product data:', error));
        });
    });
});
