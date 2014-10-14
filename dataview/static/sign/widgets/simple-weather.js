$(document).ready(function() {
  function getWeather() {
    $.simpleWeather({
      location: '98101',
      unit: 'f',
      success: function(weather) {
        html = '<h2>' + weather.temp + '&deg;'+weather.units.temp + '</h2>';
        html += '<h3>' + weather.currently + '</h3>';
    
        $("#widget-simple-weather").html(html);
      },
      error: function(error) {
        $("#widget-simple-weather").html('<p>Could not load weather</p>');
      }
    });
  }
  
  getWeather();
  setInterval(getWeather, 600000);
});
