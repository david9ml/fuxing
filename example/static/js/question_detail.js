var questionid = intemass.util.getUrl('questionid');
var itempoolid = intemass.util.getUrl('itempoolid');
var view = intemass.util.getUrl('view');
var stdthumbnail_ids = [];
var config = {
    toolbar:[],
    height:500,
    toolbarStartupExpanded: false,
    readOnly: true
};
var oCache = {
    iCacheLower: -1
};

var quploadsettings = {
    // Backend Settings
    flash_url : "/static/js/swfupload/swfupload.swf",
    upload_url: "/question/imageupload/",
    custom_settings : {
        progressTarget : "fsUploadProgress",
        upload_target : "divFileProgressContainer",
        cancelButtonId : "btnCancel"
    },

    // File Upload Settings
    file_size_limit : "20 MB",	// 2MB
    file_types : "*.*",
    file_types_description : "Images",
    file_upload_limit : "0",

    //events
    file_queued_handler : fileQueued,
    file_queue_error_handler : fileQueueError,
    file_dialog_complete_handler : fileDialogComplete,
    upload_start_handler : uploadStart,
    upload_progress_handler : uploadProgress,
    upload_error_handler : uploadError,
    upload_success_handler : uploadSuccess,
    upload_complete_handler : uploadComplete,
    queue_complete_handler : queueComplete,

    // Button Settings
    button_image_url : "/static/css/swfimages/XPButtonNoText_61x22x4.png",
    button_placeholder_id : "qupload",
    button_width: 61,
    button_height: 22,
    button_text : '<span class="swfbutton">Upload</span>',
    button_text_style : '.swfbutton {font-family: Arial; font-size:14pt ;text-align:center;background-color:#339933;}',
    button_window_mode: SWFUpload.WINDOW_MODE.TRANSPARENT,
    button_cursor: SWFUpload.CURSOR.HAND
        // Debug Settings
        //debug: true 
}

var suploadsettings = {
    // Backend Settings
    flash_url : "/static/js/swfupload/swfupload.swf",
    upload_url: "/question/imageupload/",
    custom_settings : {
        progressTarget : "fsUploadProgress1",
        upload_target : "divFileProgressContainer1",
        cancelButtonId : "btnCancel1"
    },

    // File Upload Settings
    file_size_limit : "20 MB",	// 2MB
    file_types : "*.*",
    file_types_description : "Images",
    file_upload_limit : "0",

    //events
    file_queued_handler : fileQueued,
    file_queue_error_handler : fileQueueError,
    file_dialog_complete_handler : fileDialogComplete,
    upload_start_handler : uploadStart,
    upload_progress_handler : uploadProgress,
    upload_error_handler : uploadError,
    upload_success_handler : uploadSuccess,
    upload_complete_handler : uploadCompleteForStd,
    queue_complete_handler : queueComplete,

    // Button Settings
    button_image_url : "/static/css/swfimages/XPButtonNoText_61x22x4.png",
    button_placeholder_id : "supload",
    button_width: 61,
    button_height: 22,
    button_text : '<span class="swfbutton">Upload</span>',
    button_text_style : '.swfbutton {font-family: Arial; font-size:14pt ;text-align:center;background-color:#339933;}',
    button_window_mode: SWFUpload.WINDOW_MODE.TRANSPARENT,
    button_cursor: SWFUpload.CURSOR.HAND
        // Debug Settings
        //debug: true 
}

var setEditableText = function(){
    var selquestionname = $('#question_id').children('option:selected').text();
    $("span.editable").text(selquestionname);
};

var updateQuestionName = function(newname){
    var curquestionid = $("#question_id").val();
    var curitempoolid = $("#itempool_id").val();
    $.ajax({
        type: "POST",
        url: "/question/updatename/",
        dataType: "json",
        data: { "questionid":curquestionid,
                "itempoolid":curitempoolid,
                "questionname":newname,
                "csrfmiddlewaretoken":csrfvalue
        },
        success: function(data) {
            if (data['questionid']){
                $("#question_id").children('option:selected').text(newname);
                $("#question_id").children('option:selected').val(data['questionid']);
                $("#question_type").val(data['questiontype']);
                $("$question_description").text(data['questiondescription']);
            }
            pullThumbnails();
            return data;
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            return this;
        }
    });
};

var pullQuestionDetail = function(){
    var questionid = parseInt($("#question_id").val());
    if(questionid != '-1'){
        $.post("/question/get/",
                {
                    'questionid': questionid,
                    'csrfmiddlewaretoken':csrfvalue
                },
                function(payload) {
                    if(payload.state === "success"){
                        $('#question_editor').val(payload['question_content']);
                        $('#standard_editor').val(payload['standard_content']);
                        $("#question_description").val(payload['question_desc']);
                        $("#question_type").val(payload['question_type']);
                        $("#itempool_id").val(payload['question_item']);

                        $("#templates_table #tbody tr").remove();
                        var templatelist = payload['question_markscheme'];
                        if (view){
                            for (var i = 0; i < templatelist.length; i+=1){
                                $("#templates_table #tbody").append("<tr><td>" +unchangePoint(templatelist[i][0])+"</td><td>"+ templatelist[i][1]+"</td><td></td></tr>");
                            }
                        }else{
                            for (var i = 0; i < templatelist.length; i+=1){
                                $("#templates_table #tbody").append("<tr><td>" + unchangePoint(templatelist[i][0])+"</td><td>"+ templatelist[i][1]+"</td><td class='action'><input type=button value='delete' class='delete' onclick='javascript:deletetr(this)'></input></td></tr>");
                            }
                        }

                        $('#rulecount').text("Converted Rules(" + payload['rulecount'] + " rules total)");
                        $("#rules_table #rulestbody tr").remove();
                        for (ruleidx in payload['rulelist']){
                            rule = payload['rulelist'][ruleidx];
                            $("#rules_table #rulestbody").append("<tr><td>" + rule['Point'] + "</td><td>" + rule['Mark'] + "</td></tr>");
                        }
                    }else if(payload.state === "failure"){
                        var dialogue = $( "#dialog-failure" ).dialog({
                            resizable: false,
                            height:150,
                            modal: true,
                            buttons: {
                                OK: function() {
                                    $( this ).dialog( "close" );
                                }
                            }});
                    }
                },'json');

    }else{
        console.log("question id:-1,ignore!");
    }
};

var bindImageIconClick = function(){
    function deleteImage( $item ) {
        var id = parseInt($item.children("a:last").attr( "id" ));
        //alert(id);
        $.post("/question/deleteimage/",
                {
                    'imageid': id,
                    'csrfmiddlewaretoken':csrfvalue
                },
                function(payload) {
                    if(payload.state=="success"){
                        $item.remove();
                    }
                },'json');
    }
    function viewLargerImage( $link ) {
        var src = $link.attr( "href" ),
            title = $link.siblings( "img" ).attr( "alt" ),
            $modal = $( "img[src$='" + src + "']" );

        if ( $modal.length ) {
            $modal.dialog( "open" );
        } else {
            var img = $( "<img alt='" + title + "' width='768' height='576' style='display: none; padding: 8px;' />" )
                .attr( "src", src ).appendTo( "body" );
            setTimeout(function() {
                img.dialog({
                    title: title,
                    width: 960,
                    modal: true
                });
            }, 1 );
        }
    }

    // resolve the icons behavior with event delegation
    $( "#thumbnails li" ).click(function( event ) {
        var $item = $( this );
        var $target = $( event.target );

        if ( $target.is( "a.ui-icon-zoomin" ) ) {
            viewLargerImage( $target );
        } else if ( $target.is( "a.ui-icon-closethick" ) ) {
            deleteImage( $item );
        }
        return false;
    });
};

var bindImageIconClickForStd = function(){
    function deleteImage( $item ) {
        var id = parseInt($item.children("a:last").attr( "id" ));
        $.post("/question/deleteimage/",
                {
                    'imageid': id,
            'csrfmiddlewaretoken':csrfvalue
                },
                function(payload) {
                    if(payload.state=="success"){
                        $item.remove();
                    }
                },'json');
        for (var i=0; i < stdthumbnail_ids.length; i++){
            if ( id === stdthumbnail_ids[i]){
                stdthumbnail_ids.splice(i,1);
            }
        }
    }
    function viewLargerImage( $link ) {
        var src = $link.attr( "href" ),
            title = $link.siblings( "img" ).attr( "alt" ),
            $modal = $( "img[src$='" + src + "']" );

        if ( $modal.length ) {
            $modal.dialog( "open" );
        } else {
            var img = $( "<img alt='" + title + "' width='768' height='576' style='display: none; padding: 8px;' />" )
                .attr( "src", src ).appendTo( "body" );
            setTimeout(function() {
                img.dialog({
                    title: title,
                    width: 960,
                    modal: true
                });
            }, 1 );
        }
    }

    // resolve the icons behavior with event delegation
    $( "#std_thumbnails li" ).click(function( event ) {
        var $item = $( this );
        var $target = $( event.target );

        if ( $target.is( "a.ui-icon-zoomin" ) ) {
            viewLargerImage( $target );
        } else if ( $target.is( "a.ui-icon-closethick" ) ) {
            deleteImage( $item );
        }
        return false;
    });
};

var pullThumbnails = function(){
    var questionid = parseInt($("#question_id").val());
    $.post("/question/thumbnails/",
            {
                'questionid': questionid,
        'csrfmiddlewaretoken':csrfvalue
            },
            function(payload) {
                if(payload.state=="success"){
                    thumbnails=payload['thumbnails'];
                    var thumbhtml='';
                    for (t in thumbnails){
                        thumbhtml+='<li class="ui-widget-content ui-corner-tr">';
                        thumbhtml+='<h6 class="ui-widget-header">'+thumbnails[t][1].slice(0,5)+'</h6>';
                        thumbhtml+='<img src="/static/'+thumbnails[t][0]+'"  alt="'+thumbnails[t][1]+'" width="96" height="72"></img>';
                        thumbhtml+='<a href="/static/'+thumbnails[t][2]+'" title="View Larger Image" class="ui-icon ui-icon-zoomin">View Larger</a>';
                        if(view==undefined){
                            thumbhtml+='<a href="#" title="Delete Image" id='+ thumbnails[t][3]+ ' class="ui-icon ui-icon-closethick">Delete</a>';
                        }
                    }
                    //$("#thumbnails").html(thumbhtml);
                    var $list = $( "ul", $("#thumbnails"));
                    $( "#thumbnails li").remove();
                    $(thumbhtml).appendTo($list);
                    bindImageIconClick();
                    //console.log(thumbhtml);
                }else{
                    $( "#thumbnails li").remove();
                }
            },'json');
};

var pullThumbnailsForStd = function(){
    //console.log("pull thumbnails for standard");
    var questionid = parseInt($("#question_id").val());
    $.post("/question/thumbnails/",
            {
                'questionid': questionid,
        'iscorrect' : 'yes',
        'csrfmiddlewaretoken':csrfvalue
            },
            function(payload) {
                if(payload.state === "success"){
                    thumbnails = payload['thumbnails'];
                    stdthumbnail_ids = payload['stdthumbnail_ids'];
                    //console.log(thumbnails);
                    var thumbhtml = '';
                    for (t in thumbnails){
                        thumbhtml += '<li class="ui-widget-content ui-corner-tr">';
                        thumbhtml += '<h6 class="ui-widget-header">'+thumbnails[t][1].slice(0,4)+'</h6>';
                        thumbhtml += '<img src="/static/'+thumbnails[t][0]+'"  alt="'+thumbnails[t][1]+'" width="96" height="72"></img>';
                        thumbhtml += '<a href="/static/'+thumbnails[t][2]+'" title="View Larger Image" class="ui-icon ui-icon-zoomin">View Larger</a>';
                        if(!view){
                            thumbhtml+='<a href="#" title="Delete Image" id='+ thumbnails[t][3]+ ' class="ui-icon ui-icon-closethick">Delete</a>';
                        }
                    }
                    var $list = $( "ul", $("#std_thumbnails"));
                    $( "#std_thumbnails li").remove();
                    $(thumbhtml).appendTo($list);
                    bindImageIconClickForStd();
                }else{
                    $( "#std_thumbnails li").remove();
                }
            },'json');
};



$(document).ready(function() {

	var processing_dialogue = $( "#dialog-process" ).dialog({
		autoOpen: false,
		resizable: false,
		height:150,
		width:550,
		modal: true
	});
	$( "#progressbar" ).progressbar({
		value: 100 
	});


    if (!itempoolid){
        itempoolid = -1;
    }
    if (!questionid){
        question_id = -1;
    }

    $tabs3 = $("#question_detail_tabs").tabs({ });
    $("#question_id").val(questionid);
    $("#itempool_id").val(itempoolid);
    //retreive question infomation

    $("span.editable").editable(function(value,settings){
        updateQuestionName(value);
        return value;
    },{
        type:"text",
        onblur:"submit",
        tooltip:"Click to Edit Name...",
        style: 'display:inline'
    });

    if (view){
        $("#question_editor").ckeditor(config);
        $("#standard_editor").ckeditor(config);
        $(".editable").unbind('click.editable');
        $("#submit1").hide(); 
        $("#submit2").hide(); 
        $("#submit3").hide(); 
        $("#choose_some_images_1").hide(); 
        $("#choose_some_images_2").hide(); 
        $("#question_description").attr("disabled", true);
        $("#question_type").attr("disabled", true);
        $("#itempool_id").attr("disabled", true);
        $("#btnCancel").hide();
        $("#btnCancel1").hide();
        $("#rule_templates").hide();
    }else{
        $("#question_editor").ckeditor({readOnly: false});
        $("#standard_editor").ckeditor({readOnly: false});
        swfu = new SWFUpload(quploadsettings);
        swfu1 = new SWFUpload(suploadsettings);

        $("#SWFUpload_0").live("mousedown", function(){
            var curquestionid = $("#question_id").val();
            var postobj = {"questionid": curquestionid};
            swfu.setPostParams(postobj);
        });

        $("#SWFUpload_1").live("mousedown", function(){
            var curquestionid = $("#question_id").val();
            var postobj = {"questionid": curquestionid,'standard_image':'yes'};
            swfu1.setPostParams(postobj);
        });

        $("#sample_template_t1").mask("ALL LESS 9.9 OR 9.9");
        $("#sample_template_t2").mask("All LESS 9.9 AND 9.9");
        $("#sample_template_t3").mask("ALL LESS 2 COMBINATION OF 9.9 AND 9.9 AND 9.9 AND 9.9");
        $("#sample_template_t4").mask("ANY 2 COMBINATIONS OF 9.9;9.9;9.9;9.9");
        $("#rule_templates input").keypress(function(event){
            enterkeyaction(event);
        });
    }

    pullQuestionDetail();
    pullThumbnails();
    pullThumbnailsForStd();
    setEditableText();

    $("#submit1").click(function(){
	    processing_dialogue.dialog('open');
        var question_name = $("#question_name").text();
        var question_content = $('#question_editor').val();
        var question_desc = $("#question_description").val();
        var question_type = $("#question_type").val();
        questionid = $("#question_id").val();
        itempoolid = $("#itempool_id").val();
        $.post("/question/submit/",
            {
                'questionid': questionid,
            'itempoolid': itempoolid,
            'question_name': question_name,
            'question_desc': question_desc,
            'question_content': question_content,
            'question_type': question_type,
            'csrfmiddlewaretoken':csrfvalue
            },
            function(payload) {
                if(payload.state === "success"){
	                processing_dialogue.dialog('close');
                    var dialogue = $( "#dialog-success" ).dialog({
                        resizable: false,
                        height:150,
                        modal: true,
                        buttons: {
                            OK: function() {
                                $( this ).dialog( "close" );
                            }
                        }});
                    $tabs3.tabs('select', 1);
                }else if(payload.state === "failure"){
	                processing_dialogue.dialog('close');
                    var dialogue = $( "#dialog-failure" ).dialog({
                        resizable: false,
                        height:150,
                        modal: true,
                        buttons: {
                            OK: function() {
                                $( this ).dialog( "close" );
                            }
                        }});
                }
            },'json');
    });

    $("#submit2").click(function(){
	 processing_dialogue.dialog('open');
     var questionid = parseInt($("#question_id").val());
        var standard_content=$('#standard_editor').val();
        //console.log("qid:"+questionid);
        //console.log("standard content:"+standard_content);

        $.post("/question/submitstandard/",
            {
                'questionid': questionid,
            'stdthumbnail_ids': stdthumbnail_ids.join(),
            'standard_content': standard_content,
            'csrfmiddlewaretoken':csrfvalue
            },
            function(payload) {
                if(payload.state === "success"){
					processing_dialogue.dialog('close');
                    var dialogue = $( "#dialog-success-stdanswer" ).dialog({
                        resizable: false,
                        height:150,
                        modal: true,
                        buttons: {
                            OK: function() {
                                $( this ).dialog( "close" );
                            }
                        }});
                    $tabs3.tabs('select', 2);
                }else if(payload.state === "failure"){
					processing_dialogue.dialog('close');
                    var dialogue = $( "#dialog-failure" ).dialog({
                        resizable: false,
                        height:150,
                        modal: true,
                        buttons: {
                            OK: function() {
                                $( this ).dialog( "close" );
                            }
                        }});
                }
            },'json');

    });

    $("#question_id").change(function(){
        pullQuestionDetail();
        pullThumbnails();
        pullThumbnailsForStd();
        setEditableText();
    });

    $("#submit3").click(function(){
	    processing_dialogue.dialog('open');
        var arr = new Array();
        tr_size = $("#templates_table #tbody tr").size();
        for(var i = 0; i < tr_size; i+=1 ){
            var selected_td = $("#templates_table #tbody tr").eq(i).find("td");
            var arrayitem = new Array();
            text0 = selected_td.eq(0).text();
            text1 = selected_td.eq(1).text();
            text00 = changePoint(text0);
            arrayitem.push(text00);
            arrayitem.push(text1);
            arr.push(arrayitem);
        }  
        //console.log(arr)
        if (tr_size > 0){
            var questionid = parseInt($("#question_id").val());
            $.post("/question/submitmark/",
                {
                    'questionid': questionid,
                    'schemes': arr.toString(),
                    'csrfmiddlewaretoken':csrfvalue
                },
                function(payload) {
                    if(payload.state === "success"){
	                    processing_dialogue.dialog('close');
                        var dialogue = $( "#dialog-success" ).dialog({
                            resizable: false,
                            height:150,
                            modal: true,
                            buttons: {
                                OK: function() {
                                    $( this ).dialog( "close" );
                                }
                            }});

                        $('#rulecount').text("Converted Rules(" + payload['rulecount'] + " rules total)");
                        //$tabs3.tabs('select', 2);
                        $("#rules_table #rulestbody tr").remove();
                        for (ruleidx in payload['rulelist']){
                            rule=payload['rulelist'][ruleidx];
                            $("#rules_table #rulestbody").append("<tr><td>"+rule['Point']+"</td><td>"+rule['Mark']+"</td></tr>");
                        }
                    }else if(payload.state === "failure"){
	                    processing_dialogue.dialog('close');
                        var dialogue = $( "#dialog-failure" ).dialog({
                            resizable: false,
                            height:150,
                            modal: true,
                            buttons: {
                                OK: function() {
                                    $( this ).dialog( "close" );
                                }
                            }});
                    }
                },'json');
        }
    });

});

var changePoint = function(text0){
    var rst0 = text0.toLowerCase();
    var reg1 = /(\d+)\.(\d+)/g;
    var rst1 = rst0.replace(reg1,'P$1.$2');
    //console.log(rst1);
    var reg2 = /\.0\b/g;
    var rst2 = rst1.replace(reg2,'');
    //console.log(rst2);
    return rst2;
};

var unchangePoint = function(text0){
    var rst0 = text0.toLowerCase();
    var reg1 = /p(\d+)\.(\d+)/g;
    var rst1 = rst0.replace(reg1,'$1.$2');
    //console.log(rst1);
    var reg2 = /p(\d+)\b/g;
    var rst2 = rst1.replace(reg2,'$1.0');
    //console.log(rst2);
    return rst2;
};


var deletetr = function($obj){
    $($obj).parents("tr").remove();
};

var enterkeyaction = function(evt){
    var evt = (evt) ? evt : ((window.event) ? window.event : "");
    var key = evt.keyCode?evt.keyCode:evt.which; 
    if(key == 13){
        var lastchar = evt.target.id[16];
        var numchar = evt.target.id[17];
        if(lastchar === "t"){  
            $("#sample_template_mark_"+numchar).focus();
        }else if(lastchar === "m") {
            numchar = evt.target.id[21];
            if($("#sample_template_mark_"+numchar).val()!="" && $("#sample_template_t"+numchar).val() !="") 
                $("#templates_table #tbody").append("<tr><td>"+$("#sample_template_t"+numchar).val()+"</td><td>"+
                        $("#sample_template_mark_"+numchar).val()+"</td><td class='action'><input type=button value='delete' class='delete' onclick='javascript:deletetr(this)'></input></td></tr>");
        }else{
            $("#templates_table #tbody").append("<tr><td>"+$("#cust_template").val()+"</td><td>"+
                    $("#cust_template_mark").val()+"</td><td class='action'><input type=button value='delete' class='delete' onclick='javascript:deletetr(this)'></input></td></tr>");

        }

    }
};
