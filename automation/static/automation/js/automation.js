(function($) {
    "use strict";
    $(document).ready(function() {
        console.debug("automation.js ready()");
        $().dataview_automation.render_configuration();
        $().dataview_automation.render_operations();
    });

    $.fn.dataview_automation = {};

    $.fn.dataview_automation.render_operations = function() {
        $('textarea#id_operations').each(function() {
            var ops = JSON.parse($(this).text())
            $(this).hide()

            for (var i in ops) {
                var field = ops[i]
                console.log(field)
                $(this).after('<li class="control-label">' + field['method'] + ' <b>-></b> ' + field['params'] + '</li>');
            }
            $(this).after('<br />')


        });
    };
    
    $.fn.dataview_automation.render_configuration = function() {
        $('textarea#id_configuration').each(function() {
            var ob = JSON.parse($(this).text())
            $(this).hide()

            for (var field in ob) {                
                $(this).after('<label class="control-label">' + field + '</label><textarea name="' + field + '"class="autogenerated form-control">' + ob[field] + '</textarea>');
            }
            $(this).after('<br />')
            $(this).parents('form').submit(function() {
                $.fn.dataview_automation.submit_form(this);
            });
        });
    };
    
    $.fn.dataview_automation.submit_form = function(myform) {
        var sel;
        if (arguments.length == 0) {
            console.log("noarg")
            sel = 'textarea#id_configuration';
        } else {
            sel = $(myform).find('textarea#id_configuration');
        }

        $(sel).each(function() {
            var result = {};
            $(this).parent('div').children('textarea.autogenerated').each(function() {
                result[$(this).attr('name')] = $(this).val();
            });
            console.log(result);
            $(this).text(JSON.stringify(result));
            $(this).show()
        });
    };
}(jQuery));
