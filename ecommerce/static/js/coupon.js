function apply_coupon() {
    var coupon_code = document.getElementById('code').value
    var grand_total = document.getElementById('grand_total').textContent
    var token=$('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        url: '/cartapp/apply_coupon/',
        method: 'POST',
        dataType: 'json',
        data: {
            coupon_code: coupon_code,
            grand_total: grand_total,
            csrfmiddlewaretoken: token,
        },
        success: (response) => {
            console.log(response.flag)
            if (response.flag == 1) {
                swal("Sorry!", "Coupon already used!", "error");
                document.getElementById('discount_price').textContent = 0
                document.getElementById('amount_pay').textContent = grand_total
                
            }
            else if (response.flag == 0){
                
                swal("Sorry!", "Invalid Coupon!", "error");
                document.getElementById('discount_price').textContent = 0
                document.getElementById('amount_pay').textContent = grand_total
            }
            else{
                console.log(response.amount_pay)
                swal("Congratulations!", "Coupon applied Successfully!", "success");
                document.getElementById('discount_price').innerHTML = response.discount_price
                document.getElementById('amount_pay').innerHTML = response.amount_pay
            }
            
        }
    })
}
