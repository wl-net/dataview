var config = {};

(function($) {
    "use strict";
    $(document).ready(function() {
        console.debug("dataview.js ready()");
        $.fn.dataview.loadConfig()

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
});
    });

    $.fn.dataview = {};
    
    $.fn.dataview.loadConfig = function() {
        $.get('/api/1/config', function(result) {
            
            config = result;
            console.debug("config loaded with " + Object.keys(config).length + " keys");
            
            $.event.trigger({
                    type: "configReady",
                    message: "Config loaded",
                    time: new Date()
            });
        });
    }

    $.fn.dataview.getConfig = function(key) {
        return config[key].toString();
    };

    $.fn.dataview.getDataviewConfig = function(key) {
        return config['dataview'][key].toString();
    };
}(jQuery));