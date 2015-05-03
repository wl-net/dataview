/*
 * Core javascript functionality for dataview signs
 */
var timers = [];
$(document).ready(function() {
  setInterval(function() {
    $('.current-time').html(Date.today().toString("dddd, MMMM d") + " &ndash; " + Date.today().setTimeToNow().toString("HH:mm:ss"));
  }, 1000);
});

