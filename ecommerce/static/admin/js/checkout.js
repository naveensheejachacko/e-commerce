$(document).ready(function(){
    $('.payWithRazorpay').click(function(e){
        e.preventDefault();
        var address=$(".address:checked").val();
        var token=$('input[name=csrfmiddlewaretoken]').val();
        if(address ==undefined)
        {
            swal(
                'Please Select Address',
                'Alert',
                'error'
              );
            return false;
        }
        else
        {
            $.ajax({
                type:"GET",
                url:"/orders/proceed_to_pay",

                success:function(response){
                    console.log(response);

                var options = {
                        "key": "rzp_test_J3V3xgJZgn0BJa", // Enter the Key ID generated from the Dashboard
                        "amount": response.total_price*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "Electro Mart",
                        "description": "Thank you",
                       
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb){
                            alert(responseb.razorpay_payment_id);
                            data={
                                'address':address,
                                "payment_mode":"Razorpay",
                                'payment_id': responseb.razorpay_payment_id,
                                csrfmiddlewaretoken:token                        
                        },
                        $.ajax({
                            method: "POST",
                            url: "/orders/place_order/",
                            data: data,
                            success: function (responsec) {
                                swal("Congrats",responsec.status).then((value) => {
                                    window.location.href='/dashboard/'
                                });
                                
                                
                            }
                        });                       

                    },
                        "prefill": {
                            "name": "Gaurav Kumar",
                            "email": "gaurav.kumar@example.com",
                            "contact": "9999999999"
                        },
                        "notes": {
                           "address": "Razorpay Corporate Office"
                        },
                        "theme": {
                    "color": "#3399cc"
                        }
                    };
            var rzp1 = new Razorpay(options);
            rzp1.open();

        
        }
     
    });
    
    }

});

});
