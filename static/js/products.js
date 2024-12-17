// static/js/products.js

function addToCart(productId, productName, productPrice) {
    console.log(`Adding product ${productId} to cart.`);
    $.ajax({
        url: `/cart/add-to-cart/${productId}/`,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': getCSRFToken()
        },
        success: function(response) {
            console.log('Add to cart response:', response);
            if (response.status === 'success') {
                // تحديث شارة العربة
                $('#cart-count').text(response.cart_count);
    
                // عرض رسالة نجاح باستخدام Toast
                const toastHTML = `
                    <div class="toast align-items-center text-white bg-success border-0" role="alert" aria-live="assertive" aria-atomic="true">
                        <div class="d-flex">
                            <div class="toast-body">
                                تم إضافة ${productName} بسعر ${productPrice} إلى العربة.
                            </div>
                            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                        </div>
                    </div>
                `;
                $('#toast-container').append(toastHTML);
                const toast = new bootstrap.Toast($('#toast-container .toast').last());
                toast.show();
            }
        },
        error: function(xhr, status, error) {
            console.error('Add to cart error:', error);
            // عرض رسالة خطأ باستخدام Toast
            const toastHTML = `
                <div class="toast align-items-center text-white bg-danger border-0" role="alert" aria-live="assertive" aria-atomic="true">
                    <div class="d-flex">
                        <div class="toast-body">
                            فشل في إضافة المنتج إلى العربة. حاول مرة أخرى.
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                </div>
            `;
            $('#toast-container').append(toastHTML);
            const toast = new bootstrap.Toast($('#toast-container .toast').last());
            toast.show();
        }
    });
}

function removeFromCart(itemId) {
    console.log(`Removing item ${itemId} from cart.`);
    $.ajax({
        url: `/cart/remove-from-cart/${itemId}/`,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': getCSRFToken()
        },
        success: function(response) {
            console.log('Remove from cart response:', response);
            if (response.status === 'success') {
                // تحديث عدد العناصر في السلة
                $('#cart-count').text(response.cart_count);
                
                // إزالة صف العنصر من الجدول
                $(`#cart-item-${itemId}`).remove();

                // تحديث الإجمالي
                $('h4').each(function(){
                    if ($(this).text().startsWith('الإجمالي')) {
                        $(this).text(`الإجمالي: ${response.new_total} شيكل`);
                    }
                });

                // عرض رسالة نجاح باستخدام Toast
                const toastHTML = `
                    <div class="toast align-items-center text-white bg-success border-0" role="alert" aria-live="assertive" aria-atomic="true">
                        <div class="d-flex">
                            <div class="toast-body">
                                تم إزالة العنصر من العربة بنجاح.
                            </div>
                            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                        </div>
                    </div>
                `;
                $('#toast-container').append(toastHTML);
                const toast = new bootstrap.Toast($('#toast-container .toast').last());
                toast.show();
            }
        },
       
    });
}

function getCSRFToken() {
    const csrfCookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    if (csrfCookie) {
        return csrfCookie.split('=')[1];
    }
    return '';
}

$(document).ready(function(){
    // التعامل مع نقر زر "إضافة إلى السلة"
    $('.add-to-cart-btn').click(function(event){
        event.preventDefault();
        const productId = $(this).data('product-id');
        const productName = $(this).data('product-name');
        const productPrice = $(this).data('product-price');
        addToCart(productId, productName, productPrice);
    });

    // التعامل مع نقر زر "إزالة من السلة"
    $('.remove-from-cart-btn').click(function(event){
        event.preventDefault();
        const itemId = $(this).data('item-id');
        removeFromCart(itemId);
    });
});
