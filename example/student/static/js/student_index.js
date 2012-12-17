$(document).ready(function() {
    if ($("#dialog-warning p").length > 0 ){
        var dialogue = $( "#dialog-warning" ).dialog({
            resizable: false,
            width:300,
            modal: true,
            buttons: {
                OK: function() {
                        $( this ).dialog( "close" );
                    }
            }});
    }
});
