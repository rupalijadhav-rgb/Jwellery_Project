// Helper to ensure Flask resolves images correctly
function resolveImageUrl(path) {
    if (!path) return 'https://placehold.co/40x40?text=No+Img';
    
    // 1. Clean whitespace & accidental surrounding quotes
    let cleanPath = path.toString().trim().replace(/^["']|["']$/g, '');
    
    // 2. Convert Windows backslashes (\) to standard web slashes (/)
    cleanPath = cleanPath.replace(/\\/g, '/');
    
    // 3. Keep external URLs intact
    if (cleanPath.startsWith('http://') || cleanPath.startsWith('https://')) {
        return cleanPath;
    }
    
    // 4. Handle paths containing 'static'
    const staticIndex = cleanPath.toLowerCase().indexOf('static/');
    if (staticIndex !== -1) {
        return '/' + cleanPath.substring(staticIndex);
    }
    
    // 5. Default fallback for relative file paths
    return '/static/images/' + cleanPath.replace(/^\/+/, '');
}

document.addEventListener('DOMContentLoaded', () => {
    loadAdminCatalogue();

    const addProductForm = document.getElementById('add-product-form');
    if (addProductForm) {
        addProductForm.addEventListener('submit', (e) => {
            e.preventDefault();

            let rawImage = document.getElementById('p-image').value.trim();

            const payload = {
                name: document.getElementById('p-name').value.trim(),
                category: document.getElementById('p-category').value,
                price: parseFloat(document.getElementById('p-price').value) || 0,
                material: document.getElementById('p-material').value.trim(),
                description: document.getElementById('p-desc').value.trim(),
                image: resolveImageUrl(rawImage)
            };

            fetch('/api/products', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(() => {
                addProductForm.reset();
                loadAdminCatalogue();
            })
            .catch(err => console.error('Error adding product:', err));
        });
    }
});

function loadAdminCatalogue() {
    fetch('/api/products?category=all')
        .then(res => res.json())
        .then(data => {
            const countEl = document.getElementById('admin-count');
            const tbody = document.getElementById('admin-table-body');

            if (countEl) countEl.innerText = data.length;
            if (!tbody) return;

            if (data.length === 0) {
                tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-muted">No items in catalogue.</td></tr>`;
                return;
            }

            // Reliable SVG placeholder service
            const fallbackImg = 'https://placehold.co/40x40?text=No+Img';

            tbody.innerHTML = data.map(item => `
                <tr>
                    <td>
                        <div class="d-flex align-items-center gap-2">
                            <img src="${resolveImageUrl(item.image)}" 
                                 alt="${item.name}" 
                                 style="width: 40px; height: 40px; object-fit: cover; border-radius: 4px;"
                                 onerror="this.onerror=null; this.src='${fallbackImg}';">
                            <span class="fw-semibold small">${item.name}</span>
                        </div>
                    </td>
                    <td class="text-capitalize small text-muted">${item.category}</td>
                    <td class="text-maroon fw-bold small">₹${item.price}</td>
                    <td><span class="badge bg-light text-success border border-success extra-small">IN STOCK</span></td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteAdminItem('${item._id || item.id}')">
                            <i class="bi bi-trash"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        })
        .catch(err => console.error('Error loading catalogue:', err));
}

function deleteAdminItem(id) {
    if (confirm('Delete this item?')) {
        fetch(`/api/products/${id}`, { method: 'DELETE' })
            .then(() => loadAdminCatalogue())
            .catch(err => console.error('Error deleting item:', err));
    }
}