$(document).ready(function() {
        $('.updateButton').on('click', function() {

        var id_fighter = $(this).attr('id_fighter');

        var continent = $('#continent'+{{ i.ID_FIGHTER }}).val();
        var country = $('#country'+{{ i.ID_FIGHTER }}).val();
        var city = $('#city'+{{ i.ID_FIGHTER }}).val();
//        var id_fighter = $('#id_fighter'+{{ i.ID_FIGHTER }}).val();

        req = $.ajax({
            url : '/deleteRequest',
            type : 'POST',
            data : { continent : continent, country:country,city:city,id_fighter : id_fighter}
        });
    });
});