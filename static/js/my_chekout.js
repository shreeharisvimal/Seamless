
$(document).ready(function () {
    // Add change event listener to both select elements
    $("#select_ship, #select_bill").change(function () {
        // Check if both shipping and billing addresses are selected
        if ($("#select_ship").val() && $("#select_bill").val()) {
            // Enable the "Place Order" button
            $("#placeOrderBtn").prop("disabled", false);
        } else {
            // Disable the "Place Order" button
            $("#placeOrderBtn").prop("disabled", true);
        }
    });
});


    var payment;
    var shippingAddressId;
    var billingAddressId;

    function mess(){
        Swal.fire({
            icon: 'Info',
            title: 'Please wait',
            text: 'Please hang in there for a while',
        });
    }
    function getSelectedPaymentOption() {
        var radioButtons = document.querySelectorAll('input[name="payment_option"]');
    
        for (var i = 0; i < radioButtons.length; i++) {
            console.log('RadioButton:', radioButtons[i].id, 'Checked:', radioButtons[i].checked);

            if (radioButtons[i].checked) {
                payment = radioButtons[i].id;
                console.log('Selected payment option:', payment);

                if (payment == 'exampleRadios3'){
                    $('#seamPayDiv').show();
                    console.log(seam)
                }
                else{
                    $('#seamPayDiv').hide();
                    console.log(seam)

                }
                break;
            }
        }
    }
    $(document).ready(function() {
        $('input[name="payment_option"]').prop('checked', false);
        $('#exampleRadios3').prop('checked', false);

        function openAddress() {
            $('#my_address_form').toggle($('#flexCheckChecked').prop('checked'));
        }
        $('#flexCheckChecked').change(openAddress);

        openAddress();
    });

    $('#select_ship').change(function () {
        shippingAddressId = $(this).val();
        console.log('Selected shipping Address ID:', shippingAddressId);
    });
    $('#select_bill').change(function () {
        billingAddressId = $(this).val();
        console.log('Selected billing Address ID:', billingAddressId);
    });
    var seam = 0;
    $('#seampay').change(function (){
        if(seam == 0){
            seam = 1
        }
        else{
            seam = 0 
        }
    }); 

    


    function place_order() {
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        console.log('Data being sent:', {
            'shipping': shippingAddressId,
            'billing': billingAddressId,
            'payment_select': payment,
            'the seam val': seam,
            'csrfmiddlewaretoken': csrfToken
        });

        if (payment == 'exampleRadios6') {
            $.ajax({
                url: "place_order",
                method: "POST",
                dataType: 'json',
                data: {
                    'shipping': shippingAddressId,
                    'billing': billingAddressId,
                    'payment_select': payment,
                    'csrfmiddlewaretoken': csrfToken
                },
                success: function (data) {
                    if (data.success) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Hooray',
                            text: 'The order has been placed successfully',
                        });
                        window.location.href = 'order_placed_view';
                    } else {
                        Swal.fire({
                            icon: 'warning',
                            title: 'Please select Your address',
                            text: 'Select your Billing or shipping address',
                        });
                    }
                },
            });
        } else {
            var seampayCheckbox = document.getElementById('seampay');
            var isSeampayChecked = seampayCheckbox.checked;

            var cartTotal = parseFloat($(".product-subtotal span").text().trim().replace('₹', '').replace(',', ''));
            var labelContent = document.getElementById('seampay_balance').textContent;

            var numericValue = labelContent.replace(/[^\d.]/g, '');
            var seamBalance = parseFloat(numericValue);
            
            // Check if the values are successfully extracted
            console.log('Cart Total:', cartTotal);
            console.log('Seam Balance:', seamBalance);

            if (isSeampayChecked) {
                if (cartTotal > seamBalance) {
                    console.log('in the razor pay and wallet altogether');
                    $.ajax({
                        method: "POST",
                        url: "pay_with_razor_wallet",
                        data: {
                            'shipping': shippingAddressId,
                            'billing': billingAddressId,
                            'seampay': seam,
                            'csrfmiddlewaretoken': csrfToken,
                        },
                        success: function (response) {
                            console.log(response);
                            console.log(shippingAddressId);
                            console.log(billingAddressId);
                            console.log(seam);

                            if (response.success) {
                                var options = {
                                    "key": "rzp_test_WOCu4tYSeELze1",
                                    "amount": response.order_response.amount,
                                    "currency": "INR",
                                    "name": "SEAMLESS",
                                    "description": "Thank you for purchasing with seamless",
                                    "order_id": response.order_response.id,
                                    "image": "imgs/favicon.png",
                                    "handler": function (response) {
                                        
                                        window.location.href = 'order_placed_view';
                                    },
                                    "prefill": {
                                        "name": response.full_name,
                                        "email": response.email,
                                        "contact": response.phone_number
                                    },
                                    "theme": {
                                        "color": "#3399cc"
                                    }
                                };

                                var rzp1 = new Razorpay(options);

                                rzp1.on('payment.failed', function (response) {
                                    console.log(shippingAddressId);
                                    console.log(billingAddressId);
                                    alert(response.error.code);
                                    alert(response.error.description);
                                    alert(response.error.source);
                                    alert(response.error.step);
                                    alert(response.error.reason);
                                    alert(response.error.metadata.order_id);
                                    alert(response.error.metadata.payment_id);
                                });

                                rzp1.open();
                            } else {
                                Swal.fire({
                                    icon: 'Warning',
                                    title: 'Something went wrong',
                                    text: 'Cannot place order Check if address are Selected',
                                });
                            }
                        },
                        error: function (error) {
                            console.log(error.responseText);
                        }
                    });
                } else {
                    $.ajax({
                        url: "seampay",
                        method: "POST",
                        dataType: 'json',
                        data: {
                            'shipping': shippingAddressId,
                            'billing': billingAddressId,
                            'payment_select': payment,
                            'csrfmiddlewaretoken': csrfToken
                        },
                        success: function (data) {
                            if (data.success) {
                                
                                window.location.href = 'order_placed_view';
                            } else {
                                Swal.fire({
                                    icon: 'warning',
                                    title: 'Please select Your address',
                                    text: 'Select your Billing or shipping address',
                                });
                            }
                        },
                    });
                
                   
                }
            } else {
                $.ajax({
                    method: "POST", // Change to POST
                    url: "pay_with_razor",
                    data: {
                        'shipping': shippingAddressId,
                        'billing': billingAddressId,
                        'seampay':seam,
                        'csrfmiddlewaretoken': csrfToken,
                    },
                    success: function (response) {
                        console.log(response);
                        console.log(shippingAddressId)
                        console.log(billingAddressId)
                        console.log(seam)
        
                        if (response.success){
            
                            var options = {
                                "key": "rzp_test_WOCu4tYSeELze1",
                                "amount": response.order_response.amount, 
                                "currency": "INR",
                                "name": "SEAMLESS",
                                "description": "Thank you for purchasing with seamless",
                                "order_id": response.order_response.id,
                                "image": "imgs/favicon.png",
                                "handler": function (response) {
                                   
                                    window.location.href = 'order_placed_view';
        
                                },
                                "prefill": {
                                    "name": response.full_name,
                                    "email": response.email,
                                    "contact": response.phone_number
                                },
                                "theme": {
                                    "color": "#3399cc"
                                }
                            };
                
                            var rzp1 = new Razorpay(options);
                
                            rzp1.on('payment.failed', function (response) {
                                // Handle payment failure
                                console.log(shippingAddressId)
                                console.log(billingAddressId)
                                alert(response.error.code);
                                alert(response.error.description);
                                alert(response.error.source);
                                alert(response.error.step);
                                alert(response.error.reason);
                                alert(response.error.metadata.order_id);
                                alert(response.error.metadata.payment_id);
                            });
                
                            rzp1.open();
                        }    
                        else{
                            Swal.fire({
                                icon: 'Warning',
                                title: 'Something went wrong',
                                text: 'Cannot place order Check if address are Selected',
                            });
                        }
                    },
                    error: function (error) {
                        console.log(error.responseText);
                        // Handle the error if necessary
                    }
                });
            
                console.log('Seampay checkbox is not checked');
            }
        }
    }


        
  