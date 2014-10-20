$(document).on('configReady', function() {
    var mapOptions = {
        zoom: 14,
        center: new google.maps.LatLng($.fn.dataview.getDataviewConfig('my_location_latlng')[0], $.fn.dataview.getDataviewConfig('my_location_latlng')[1]),
        disableDefaultUI: true
    };
    map = new google.maps.Map(document.getElementById('traffic-map'), mapOptions);
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng($.fn.dataview.getDataviewConfig('my_location_latlng')[0], $.fn.dataview.getDataviewConfig('my_location_latlng')[1]),
        map: map,
        title: 'Aspira'
    });
    var transitLayer = new google.maps.TransitLayer();
    transitLayer.setMap(map);
    var trafficLayer = new google.maps.TrafficLayer();
    trafficLayer.setMap(map);
});
