function decreaseQuantity(qty,id,sub_total,c_id){
    var qty=$('#'+qty)
    var sub_total=$('#'+sub_total)
    console.log('jfdfsgsgsdgsdgsdg')
    $.ajax({
        type:"GET",
        url:"/cartapp/decrease_quantity/",
        data:{
            'id':id,
            'c_id':c_id
        },
        success : function(r){
            if(r.status==true){

            
            $(qty).val(r.quantity)
            $(sub_total).text("₹"+r.sub_total)
            $('#total').text("₹"+r.total)
            $('#total_price').text("₹"+r.total_price)
            $('#saved').text("-"+r.saved)
        }else{
            console.log('not possible')
        }
        },
        error:function(r){
            alert('Error Occured')
        }
    });
}


function increaseQuantity(qty,id,sub_total,c_id){
    var qty=$('#'+qty)
    var sub_total=$('#'+sub_total)
    
    $.ajax({
        type:"GET",
        url:"/cartapp/increase_quantity/",
        data:{
            'id':id,
            'c_id':c_id
        },
        success : function(r){
            $(qty).val(r.quantity)
            $(sub_total).text("₹"+r.sub_total)
            $('#total').text("₹"+r.total)
            $('#total_price').text("₹"+r.total_price)
            $('#saved').text("-"+r.saved)
            
        },
        error:function(r){
            alert('Error Occured')
        }
    });
}