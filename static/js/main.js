let cart = [];

// Helper to escape single quotes safely for inline HTML onclick attributes
function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

document.addEventListener('DOMContentLoaded', () => {
    const filterBtns = document.querySelectorAll('.pill-btn');
    const searchInput = document.getElementById('search-input');

    let currentCategory = 'all';

    function fetchProducts() {
        const search = searchInput ? searchInput.value : '';
        fetch(`/api/products?category=${currentCategory}&search=${encodeURIComponent(search)}`)
            .then(res => res.json())
            .then(data => renderProducts(data))
            .catch(err => console.error('Error fetching products:', err));
    }

    function renderProducts(products) {
        const productGrid = document.getElementById('product-grid');
        if (!productGrid) return;

        if (products.length === 0) {
            productGrid.innerHTML = `<div class="col-12 text-center py-5 text-muted"><p>No items found in this collection.</p></div>`;
            return;
        }

        const fallbackImg = 'https://via.placeholder.com/300x300?text=No+Image';

        productGrid.innerHTML = products.map(item => {
            const escapedName = escapeHtml(item.name);
            const escapedMat = escapeHtml(item.material || 'Traditional Gold Plated');
            const escapedDesc = escapeHtml(item.description || 'Handcrafted traditional Maharashtrian jewellery.');
            const escapedCat = escapeHtml(item.category);
            const escapedImg = escapeHtml(item.image);

            return `
                <div class="col-6 col-md-4 col-lg-3">
                    <div class="card product-card h-100 position-relative">
                        <span class="badge-cat">${item.category}</span>
                        <div class="product-card-img-wrapper">
                            <img src="${item.image}" class="product-card-img" alt="${item.name}" onerror="this.onerror=null; this.src='${fallbackImg}';">
                        </div>
                        <div class="card-body d-flex flex-column justify-content-between p-3">
                            <div>
                                <h6 class="font-serif fw-bold mb-1" style="font-size: 0.95rem;">${item.name}</h6>
                                <p class="text-maroon fw-bold mb-2">₹${item.price}</p>
                            </div>
                            <div class="d-flex gap-2">
                                <button class="btn btn-outline-secondary btn-sm flex-fill" 
                                        onclick="openProductModal('${escapedName}', ${item.price}, '${escapedMat}', '${escapedDesc}', '${escapedCat}', '${escapedImg}')" 
                                        title="Quick View">
                                    <i class="bi bi-eye"></i> QUICK VIEW
                                </button>
                                <button class="btn btn-maroon btn-sm flex-fill" 
                                        onclick="addToCart('${escapedName}', ${item.price}, '${escapedCat}', '${escapedImg}')">
                                    <i class="bi bi-bag"></i> ADD
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCategory = btn.dataset.category;
            fetchProducts();
        });
    });

    if (searchInput) {
        searchInput.addEventListener('input', fetchProducts);
    }
    
    fetchProducts();
});

// Quick View Modal Trigger Function
function openProductModal(name, price, material, desc, category, image) {
    document.getElementById('modal-title').innerText = name;
    document.getElementById('modal-price').innerText = `₹${price}`;
    document.getElementById('modal-material').innerText = material || 'Standard Alloy';
    document.getElementById('modal-desc').innerText = desc || 'Handcrafted traditional Maharashtrian jewellery featuring gold-plated finish and intricate work.';
    document.getElementById('modal-cat').innerText = category;
    document.getElementById('modal-img').src = image;

    // Attach Add to Cart action inside modal
    const addBtn = document.getElementById('modal-add-btn');
    addBtn.onclick = () => {
        addToCart(name, price, category, image);
        const modalEl = document.getElementById('productDetailModal');
        const modal = bootstrap.Modal.getInstance(modalEl);
        if (modal) modal.hide();
    };

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('productDetailModal'));
    modal.show();
}

// Enhanced Cart Management
function addToCart(name, price, category = '', image = '') {
    const existingIndex = cart.findIndex(item => item.name === name);

    if (existingIndex > -1) {
        cart[existingIndex].qty += 1;
    } else {
        cart.push({
            name: name,
            price: Number(price),
            category: category || 'Jewellery',
            image: image || 'https://via.placeholder.com/60?text=No+Img',
            qty: 1
        });
    }

    updateCartUI();
}

function proceedToCheckout() {
    if (cart.length === 0) {
        alert("Your cart is empty. Please add items before checking out!");
        return;
    }
    alert("Demo checkout — no payment is processed.");
}

function updateQuantity(index, delta) {
    cart[index].qty += delta;
    if (cart[index].qty <= 0) {
        cart.splice(index, 1);
    }
    updateCartUI();
}

function clearCart() {
    cart = [];
    updateCartUI();
}

function updateCartUI() {
    const totalItems = cart.reduce((sum, item) => sum + item.qty, 0);
    const cartCountEl = document.getElementById('cart-count');
    if (cartCountEl) cartCountEl.innerText = totalItems;
    renderCart();
}

function renderCart() {
    const container = document.getElementById('cart-items-container');
    const totalEl = document.getElementById('cart-total');
    if (!container || !totalEl) return;
    
    if (cart.length === 0) {
        container.innerHTML = `<p class="text-muted text-center py-5">Your cart is empty.</p>`;
        totalEl.innerText = '₹0';
        return;
    }

    let total = 0;
    const fallbackImg = 'https://via.placeholder.com/60?text=No+Img';

    container.innerHTML = cart.map((item, index) => {
        const itemTotal = item.price * item.qty;
        total += itemTotal;

        return `
            <div class="d-flex align-items-center gap-3 py-3 border-bottom">
                <img src="${item.image}" alt="${item.name}" 
                     style="width: 70px; height: 70px; object-fit: cover; border-radius: 8px;"
                     onerror="this.onerror=null; this.src='${fallbackImg}';">
                     
                <div class="flex-grow-1">
                    <h6 class="fw-bold mb-0 text-dark small">${item.name}</h6>
                    <small class="text-muted text-capitalize d-block mb-2" style="font-size: 0.8rem;">${item.category}</small>
                    
                    <div class="d-inline-flex align-items-center border rounded px-2 py-1">
                        <button class="btn btn-sm p-0 border-0 me-2 text-muted" onclick="updateQuantity(${index}, -1)" style="line-height:1;">—</button>
                        <span class="small fw-semibold px-1">${item.qty}</span>
                        <button class="btn btn-sm p-0 border-0 ms-2 text-muted" onclick="updateQuantity(${index}, 1)" style="line-height:1;">+</button>
                    </div>
                </div>

                <div class="text-end">
                    <span class="text-maroon font-serif fw-bold">₹${itemTotal.toLocaleString('en-IN')}</span>
                </div>
            </div>
        `;
    }).join('');

    totalEl.innerText = `₹${total.toLocaleString('en-IN')}`;
}


// Auth & Profile State Management
let currentUser = JSON.parse(localStorage.getItem('kalakruti_user')) || null;
let userOrders = JSON.parse(localStorage.getItem('kalakruti_orders')) || [];

document.addEventListener('DOMContentLoaded', () => {
    updateProfileUI();

    // Trigger Sign-In popup 5 seconds after landing (if not signed in)
    setTimeout(() => {
        if (!currentUser) {
            const authModalEl = document.getElementById('authModal');
            if (authModalEl) {
                const authModal = new bootstrap.Modal(authModalEl);
                authModal.show();
            }
        }
    }, 5000);
});

function handleAuthSubmit(e) {
    e.preventDefault();
    const name = document.getElementById('user-name-input').value;
    const email = document.getElementById('user-email-input').value;

    if (!name || !email) return;

    currentUser = { name, email };
    localStorage.setItem('kalakruti_user', JSON.stringify(currentUser));

    // Hide Modal
    const modalEl = document.getElementById('authModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    if (modal) modal.hide();

    updateProfileUI();
}

function handleProfileClick() {
    if (currentUser) {
        const drawerEl = document.getElementById('profileDrawer');
        const drawer = new bootstrap.Offcanvas(drawerEl);
        drawer.show();
    } else {
        const authModalEl = document.getElementById('authModal');
        const authModal = new bootstrap.Modal(authModalEl);
        authModal.show();
    }
}

function updateProfileUI() {
    const profileBtn = document.getElementById('profile-nav-btn');
    if (!profileBtn) return;

    if (currentUser) {
        // Highlighting logged in user icon
        profileBtn.classList.remove('btn-outline-dark');
        profileBtn.classList.add('btn-maroon', 'text-white');
        
        document.getElementById('display-user-name').innerText = currentUser.name;
        document.getElementById('display-user-email').innerText = currentUser.email;
        document.getElementById('user-avatar').innerText = currentUser.name.charAt(0).toUpperCase();

        renderProfileOrders();
    } else {
        profileBtn.classList.remove('btn-maroon', 'text-white');
        profileBtn.classList.add('btn-outline-dark');
    }
}

function renderProfileOrders() {
    const orderCountEl = document.getElementById('profile-order-count');
    const ordersListEl = document.getElementById('profile-orders-list');
    
    if (!orderCountEl || !ordersListEl) return;

    orderCountEl.innerText = userOrders.length;

    if (userOrders.length === 0) {
        ordersListEl.innerHTML = `No active orders placed yet.`;
    } else {
        ordersListEl.innerHTML = userOrders.map((ord, i) => `
            <div class="border-bottom py-2">
                <div class="fw-bold text-dark">Order #${ord.id}</div>
                <div class="text-maroon">₹${ord.total.toLocaleString('en-IN')} (${ord.itemsCount} items)</div>
            </div>
        `).join('');
    }
}

function cancelCurrentOrders() {
    if (userOrders.length === 0) {
        alert("No active orders to cancel.");
        return;
    }
    
    if (confirm("Are you sure you want to cancel all active orders?")) {
        userOrders = [];
        localStorage.setItem('kalakruti_orders', JSON.stringify(userOrders));
        renderProfileOrders();
        alert("All active orders have been cancelled.");
    }
}

function signOutUser() {
    currentUser = null;
    localStorage.removeItem('kalakruti_user');
    
    const drawerEl = document.getElementById('profileDrawer');
    const drawer = bootstrap.Offcanvas.getInstance(drawerEl);
    if (drawer) drawer.hide();

    updateProfileUI();
}

// Intercept checkout to log active orders
function proceedToCheckout() {
    if (cart.length === 0) {
        alert("Your cart is empty. Please add items before checking out!");
        return;
    }

    if (!currentUser) {
        alert("Please sign in before placing an order.");
        handleProfileClick();
        return;
    }

    const total = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
    const itemsCount = cart.reduce((sum, item) => sum + item.qty, 0);

    // Save order
    userOrders.push({
        id: Math.floor(1000 + Math.random() * 9000),
        total: total,
        itemsCount: itemsCount,
        date: new Date().toLocaleDateString()
    });

    localStorage.setItem('kalakruti_orders', JSON.stringify(userOrders));
    
    // Clear Cart
    clearCart();

    alert("Demo checkout — no payment is processed. Order added to your profile!");
}