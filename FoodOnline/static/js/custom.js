let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    // console.log(place);
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_adress').value
     
    geocoder.gocoder({'address' : address }),function(results, status){
    // console.results("results =>" ,results)
    // console.results("status =>" ,status)
        if(status === google.maps.GeocoderStatus.ok){
        var latitude = results[0].geometry.location.lat()
        var longitude = results[0].geometry.location.lng()
        
        $('#id_latitude').val(latitude)
        $('#id_longitude').val(longitude)

        $('#id_address').val(address)

        }

    };

    // loop through the address components and assign other address data
    // console.log(place.address_components)
    for(var i=0; i<place.address_components.length; i++){
        for (j=0; j<place.address_components[i].types.length; j++){
            //get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name) 
            }
            //get state
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name) 
            }
            //get city
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name) 
            }
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name) 
            }
            else{
                $('#id_pin_code').val("") 
            }
        }
    }

}


// add to cart
$(document).ready(function(){
    //add to cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        // alert(food_id);
        // data when you send
        data = {
            food_id: food_id,
        }
        
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                console.log(response);
                //push value in html
                if(response.status == 'Login required !'){
                    //sweet alert
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: response.status,
                        // footer: '<a href="#">Why do I have this issue?</a>'
                      }).then(function () {
                        window.location = '/login';
                      })
                }
                else if(response.status == 'Failed'){
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: response.message,
                        // footer: '<a href="#">Why do I have this issue?</a>'
                      })
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                    //cart subtotal, grand total, tax
                    applyCartAmount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],

                    )
                }
            },
            // error: function(response) { 
            //     alert(response);
            // }
        })
    })

    //place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        // console.log(qty,the_id);
        $('#'+the_id).html(qty);
    })

    //decrease cart
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

        // alert(food_id);
        // data when you send
        data = {
            food_id: food_id,
        }
        
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                console.log(response);
                //push value in html
                if(response.status == 'Login require !'){
                    //sweet alert
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: response.status,
                        // footer: '<a href="#">Why do I have this issue?</a>'
                      }).then(function () {
                        window.location = '/login';
                      })
                }
                else if(response.status == 'Failed'){
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: response.message,
                        // footer: '<a href="#">Why do I have this issue?</a>'
                      })
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                    //cart subtotal, grand total, tax
                    applyCartAmount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],

                    )

                    if(window.location.pathname == '/cart/'){
                        removeCartItem(response.qty, cart_id);
                        checkEmptyCart();
                    }
                    
                }
            },
        })
    })


    //DELETE cart item
    $('.delete_cart').on('click', function(e){
        e.preventDefault();

        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response);
                //push value in html
                if(response.status == 'Failed'){
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: response.message,
                        // footer: '<a href="#">Why do I have this issue?</a>'
                      })
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    Swal.fire({
                        icon: 'success',
                        title: 'Done...',
                        text: response.message,
                        // footer: '<a href="#">Why do I have this issue?</a>'
                    })

                    //cart subtotal, grand total, tax
                    applyCartAmount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],

                    )

                      removeCartItem(0, cart_id);
                      checkEmptyCart();
                }
            },
        })
    })

    //delete cart element if the the qty is 0
    function removeCartItem(cartItemQty, cart_id){
        if(cartItemQty <= 0 ){
            // alert('The cart element')
            //remove cart item elements
            document.getElementById("cart-"+ cart_id).remove()
        }
    }

    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if (cart_counter == 0)
            document.getElementById('empty-cart').style.display = 'block';
    }

    //apply cart amount
    function applyCartAmount(subtotal, tax, grand_total){
        if(window.location.pathname == '/cart/'){
        $('#subtotal').html(subtotal)
        $('#tax').html(tax)
        $('#grand_total').html(grand_total)
        }
    }
    
});
