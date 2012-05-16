(function($){
    $.extend({
        arrayUnique: function(v){
            var i, u=[]
            for(i=v.length;i--;){
                if($.inArray(v[i], u)===-1) u.unshift(v[i])
            }
            return u
        },
    })
    $.fn.extend({
        insertAtCaret: function(text) {
            var txtarea = $(this).get(0);
            if (txtarea) {
                var scrollPos = txtarea.scrollTop;
                var strPos = 0;
                var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ? 
                    "ff" : (document.selection ? "ie" : false ) );
                if (br == "ie") { 
                    txtarea.focus();
                    var range = document.selection.createRange();
                    range.moveStart ('character', -txtarea.value.length);
                    strPos = range.text.length;
                }
                else if (br == "ff") strPos = txtarea.selectionStart;

                var front = (txtarea.value).substring(0,strPos);  
                var back = (txtarea.value).substring(strPos,txtarea.value.length); 
                txtarea.value=front+text+back;
                strPos = strPos + text.length;
                if (br == "ie") { 
                    txtarea.focus();
                    var range = document.selection.createRange();
                    range.moveStart ('character', -txtarea.value.length);
                    range.moveStart ('character', strPos);
                    range.moveEnd ('character', 0);
                    range.select();
                }
                else if (br == "ff") {
                    txtarea.selectionStart = strPos;
                    txtarea.selectionEnd = strPos;
                    txtarea.focus();
                }
                txtarea.scrollTop = scrollPos;
            }
        }
    })
   
    $(function(){
        var list   = $('<ul id="django-courier-vars" class="clearfix"/>').insertAfter('#id_variables')
        var vars   = $.parseJSON($('#id_variables').hide().text())
        var fields = 'input[name^="subject"]:visible, textarea[name^="body"]:visible'
        var updateinserted = function(){
            var vars = []
            $.each($(fields), function(i, f) {
                console.log(i, f)
                var rs = $(f).val().match(/({{\s+?\w+\.?\w+?\s+?}})/gm)
                if (rs) {
                    vars = vars.length && $.merge(vars, rs) || rs
                }
            })
            if (vars) {
                $.each($.arrayUnique(vars), function(i, v){
                    var val = v.replace(/{|}|\s|/g, '').replace(/\./g, ' ')
                    $('#django-courier-vars button').filter(function(){
                        console.log($(this).text(), val, $(this).text() == val)
                        return $(this).text() == val
                    }).addClass('inserted')
                })
            }
        }
        $(fields).bind('focus', function(){
            $(fields).removeClass('courier-lastFocus')
            $(this).addClass('courier-lastFocus')
        }).bind('blur', function() {
        })
        $.each(vars, function(k, props){
            $.each(props, function(i, v){
                var li = $('<li />').appendTo(list)
                var a = $('<button />').appendTo(li)
                a.data('courier-var', '{{ '+k+'.'+v+' }}')
                    .bind('click', function(){
                        $(fields).filter('.courier-lastFocus').focus()
                        $(fields).filter('.courier-lastFocus').insertAtCaret($(this).data('courier-var'))
                        updateinserted()
                        return false
                    }).text(k+' '+v)

            })
        })
        updateinserted()
    })
})(jQuery || django.jQuery)
