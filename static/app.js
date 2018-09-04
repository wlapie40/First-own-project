$(document).ready(function() {

    $('.updateButton').on('click'),function() {

        var member_id = $(this).attr('submit');

        var continent = $('#continent').val();
        var country = $('#contry').val();
        var city = $('#city').val();
        var zip_code = $('#zip_code').val();
        var street = $('#street').val();
        var street_number = $('#street_number').val();

        req = $.ajax({
            url : '/update',
            type : 'POST',
            data : {continent : continent, contry : contry, city : city, zip_code : zip_code,street : street, street_number : street_number}
        });

        $('$panel').fadeOut(1000).fadeIn(1000);
    });
});