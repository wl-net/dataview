var timers = [];
var itenCounters = [];

$(document).on('configReady', (function() {
    showDestinations();
    setInterval(function() {
        showDestinations();
    }, 1000 * 300 );
    
    function showDestinations() {
        $.get('/transportation/destinations/1', function(destinations) {
        for (i in timers) {
        clearInterval(timers[i]);
        console.debug("cleared timer");
        };
        
        $('.transit-results').html('');


        for (i in destinations) {
            var destination = destinations[i];
            $('.transit-results').append('<div class="transit-result transit-result-' + i +'" style="overflow:auto"><div style="overflow:auto"><h2 class="pull-left"><strong>'
            + (destinations[i][0]) + '</strong></h2> <h2 class="transit-time pull-right">' 
            + 'N/A minutes' + '</h2></div><div style="overflow:auto"><h2 class="transit-directions">...</h2></div></div');
        }
        updateData(destinations);

    });
    }
  
  
  function updateData(destinations) {
    for (i in destinations) {
      $('.widget-transit_arrivals > .heading').attr('data-title', 'Transit Arrival Times // Updated ' + Date.today().setTimeToNow().toString("HH:mm:ss"))
      $.ajax({
        url: '/api/transit/otp/otp-rest-servlet/ws/plan?fromPlace=' + $.fn.dataview.getDataviewConfig('my_location') + '&toPlace='+ destinations[i][1] + '&maxWalkDistance=1500&walkSpeed=1.4&bannedStops=KCM_431&maxHours=1&numItineraries=3&x_wlnet_destination=' + i,
        success: function(response1) {
          var i = response1.requestParameters.x_wlnet_destination
          if (null != response1.plan && null == response1.plan.error) {
            var d = new Date(response1.plan.itineraries[0].legs[0].startTime);

            setTimeout(function(arg) {
            itenCounters[arg.i] = 0;
            timers.push(setInterval(function() {
                var res = arg.response;
                var iten = itenCounters[arg.i];
                try {
                    var date = new Date(res.plan.itineraries[iten].legs[0].startTime);
                } catch (e) {} 
            
                var mode;
                if (res.plan.itineraries[iten].legs.length == 1) {
                    mode = '<em>' + res.plan.itineraries[iten].legs[0].mode.toLowerCase() + '</em> at 1.7m/s';
                } else {
                    mode = '<em>' + res.plan.itineraries[iten].legs[1].mode.toLowerCase() + '</em> via route <em>' + res.plan.itineraries[iten].legs[1].routeShortName + '</em>';
                }

                if (res.plan.itineraries.length == 1) {
                    $('.transit-result-' + i + ' .transit-directions').html(mode + ', leaving at ' + d.toString('HH:mm'));
                } else {
                    if (res.plan.itineraries[iten].legs[1].realTime) {
                        var leaveAt = "<strong>" + date.toString('HH:mm') + "</strong>";
                    } else {
                        var leaveAt = date.toString('HH:mm');
                    }
                    $('.transit-result-' + i + ' .transit-directions').html('(' + (iten+1) + ' / ' + (res.plan.itineraries.length) +') ' 
                    + mode + ', leaving at ' + leaveAt);
                }

                    $('.transit-result-' + i + ' .transit-time').text(Math.round(res.plan.itineraries[iten].duration / 60) + ' minutes');
                    itenCounters[arg.i] = (iten + 1) % res.plan.itineraries.length;
            }, 1000 * 6, arg));
            
            }, 1000 * Math.random(3), {i: i, response: response1});
          } else {
            console.log("Error");
          }      
        },
        error: function(e) { console.log(e); }
      });
    }
  }
}));
