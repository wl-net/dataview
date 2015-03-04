// dataview portal shared javascript code

$(document).ready(function() {
  $('.portal-messages-container button').click(function() {
    var e = this;
    data = {messageid: $(e).attr('data-messageid')}
    $.post( "/portal/api/dismiss-message", data, function( data ) {
    });
  });
});