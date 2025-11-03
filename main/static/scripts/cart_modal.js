// static/scripts/cart_modal.js (Updated)

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById('cartModal');
    const modalImage = document.getElementById('modalProductImage');
    const modalPrice = document.getElementById('modalProductPrice');
    const allCartButtons = document.querySelectorAll('.cart-btn');
    // ✅ CRITICAL: Get the cart count element from the navbar
    const cartCountElement = document.getElementById('cart-count'); 

    // 1. Function to open the modal and populate data
    function openCartModal(itemData) {
        modalImage.src = itemData.item.image_url;
        modalPrice.textContent = `$${itemData.item.price.toFixed(2)}`;
        
        modal.style.display = 'flex'; // Show the modal
    }

    // 2. Global function to close the modal
    window.closeCartModal = function() {
        modal.style.display = 'none';
    }

    // 3. Event listener for ALL cart buttons
    allCartButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            
            const url = button.closest('a').href; 
            const templateId = url.split('/').filter(Boolean).pop(); 

            if (!templateId) {
                console.error("Could not find template ID.");
                return;
            }

            // AJAX call to add to cart
            fetch(`/cart/add/${templateId}/`, {
                method: 'GET', 
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    // 403 error often means the user is not logged in
                    if (response.status === 403) { 
                        window.location.href = '/login/'; // Redirect to login page
                        return;
                    }
                    throw new Error('Network response was not ok. Status: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // ✅ CRITICAL FIX: Update Cart count in header
                    if(cartCountElement) {
                        // Server sends cart_count, update the element's text
                        cartCountElement.textContent = data.cart_count; 
                        
                        // If the count is 0, optionally hide the badge, or if > 0 show it
                        if (data.cart_count > 0) {
                            cartCountElement.style.display = 'inline-block';
                        } else {
                            cartCountElement.style.display = 'none';
                        }
                    }
                    
                    // Open the modal with received data
                    openCartModal(data);
                } else {
                    console.error('Server returned success=false');
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                alert('An error occurred while adding the item to the cart.');
            });
        });
    });
});