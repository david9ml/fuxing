;(function($, undef) {
    $(function(){
        /*
           $("div.ui-corner-tl").prepend(
           '<div class="zone_opt_btn">' +
           '<div class="opt_btn">Year:<input type="text" id="param1" class="stext ui-widget-content ui-corner-all" maxlength="20" /> Level:<input type="text" id="param2" maxlength="20" class="stext ui-widget-content ui-corner-all" /> Subject:<select id="param3" class="stext ui-widget-content ui-corner-all"></select></div>' +
           '<div class="clear"></div>' +
           '</div>'
           );
           $("#data_list_filter").css({ "display": "none" });
           $("#data_list_filter").css({ "float": "left", "text-align": "left" });
           $("#data_list_filter button[class='btn_search']").css("margin-top", "10px");
           */
        oTable = $('#data_list').dataTable(
            {
                "bJQueryUI": true,
               "bProcessing": true,
               "sAjaxSource": "/paper/getall/?forwhat=teacher_report",
               "width":"80px",
            });

        $("#data_list_filter").css({ "display": "none" });

        $('#id_level').attr({'onBlur':'submitform'});
    });

})(jQuery);

function submitform(){
    var oTable = $('#data_list').dataTable();
    var year = $('#id_year').val();
    var subject = $('#id_subject').val();
    var level = $('#id_level').val();
    console.log(year + ' ' + subject + ' ' + level);
    oTable.fnFilter(year,0);
    oTable.fnFilter(subject,1);
    oTable.fnFilter(level,2);
}

function checkdetailmark(){
 //   var checkedpaperid = document.getElementById("data_list").getElementsByTagName("input");
    var paperids = [];

    $('input', oTable.fnGetNodes()).each(function(){
        if($(this).attr('checked') === 'checked'){
            paperids.push($(this).attr('name'));
        }
    });

    $('#paperids').val(paperids);
    document.formx1.submit();
}

function selectall(){
    oTable = $('#data_list').dataTable();
    $('input', oTable.fnGetNodes()).each(function(){
        $(this).attr('checked',!$(this).attr('checked'));
    });
} 

