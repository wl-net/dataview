var config = {};

(function($) {
    "use strict";
    $(document).ready(function() {
        console.debug("dataview.js ready()");
        $.fn.dataview.loadConfig()
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