/*
 * Core javascript functionality for dataview signs
 */
$(document).ready(function() {
  setInterval(function() {
    $('.current-time').html(Date.today().toString("dddd, MMMM d") + " &ndash; " + Date.today().setTimeToNow().toString("HH:mm:ss"));
  }, 1000);

  setInterval(function() {
    $('.transit-times').load('/sign/transit');
  }, 1000 * 30 );

  lastSwitch = null;

  setInterval(function() {
    var baseUrl = "http://archives.earthcam.com/archives5/ecnetwork/us/wa/seattle/ullrailmp1/";
    var lastUpdate = { hour: Date.today().setTimeToNow().getHours(), minute: (Math.floor((Date.today().setTimeToNow().getMinutes() - 5) / 15)) * 15 };
    if (JSON.stringify(lastUpdate) == lastSwitch) {
      return;
    }

    var image = new Image();
    image.onload = function() {
      $('.earthcam').attr('src', (baseUrl + Date.today().at(lastUpdate).toString("/yyyy/MM/dd/HHmm") + '.jpg'));
      lastSwitch = JSON.stringify(lastUpdate);
    }
    image.src = (baseUrl + Date.today().at(lastUpdate).toString("yyyy/MM/dd/HHmm") + '.jpg');
  }, 1000 * 5);
});

