$(document).ready(function() {
    $('#id_city_tt').typeahead(
        {
            name: 'name',
            valueKey: 'name',
            prefetch: '/api/v1/cities-typeahead/.json',
            remote: '/api/v1/cities-typeahead/.json?city=%QUERY'
        }
    ).bind('typeahead:selected', function (obj, datum) {
            $('#id_city').val(datum.id);
        }).bind('typeahead:autocompleted', function (obj, datum) {
            $('#id_city').val(datum.id);
        });

});