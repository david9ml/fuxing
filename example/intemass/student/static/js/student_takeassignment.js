/*
 * yanchao727@gmail.com
 * 15/06/2012
 *
 */

var stuthumbnail_ids = '';

;(function($, undef) {

    var timeoutTimer = setInterval(refreshtimeout, 60000);
    var config = {
        toolbar: [],
        height: 500,
        toolbarStartupExpanded: false,
        readOnly: true
    };

    $(function(){
        $("#question_name_show").text(qnames[0]);
        $("#question_process_show").text(1 + "/" + qids.length);
        $("#question_editor").ckeditor(config);
        loadquestion(qids[0]);
        pullThumbnails(qids[0]);
        $("#answer_editor").ckeditor();
        refreshtimeout();
        $(window).bind('beforeunload', function(){
            $.post("/student/checktime/",
                {
                    'save':true,
                    'paperid':paperid,
                    'csrfmiddlewaretoken':csrfvalue
                },
                function(payload) {
                        console.log('time saved');
                },'json');
        }); 

        var count = qids.length -1;
        var i = 0;
        $("#previous").click(function(){
            submitanswer(qids[i]);
            if(i !== 0){
                i -= 1;
                $("#answer_editor").val("");
                $("#question_name_show").text(qnames[i]);
                $("#question_process_show").text(i+1+"/"+qids.length);
                loadquestion(qids[i]);
                pullThumbnails(qids[i]);
            }
        });

        $("#next").click(function(){
            submitanswer(qids[i]);
            if(i !== count){
                i += 1;
                $("#answer_editor").val("");
                $("#question_name_show").text(qnames[i]);
                $("#question_process_show").text(i+1+"/"+qids.length);
                loadquestion(qids[i]);
                pullThumbnails(qids[i]);
            }
        });

        $("#first").click(function(){
            submitanswer(qids[i]);
            $("#answer_editor").val("");
            $("#question_name_show").text(qnames[0]);
            $("#question_process_show").text(1+"/"+qids.length);
            loadquestion(qids[0]);
            pullThumbnails(qids[0]);
            i = 0;
        });

        $("#last").click(function(){
            submitanswer(qids[i]);
            $("#answer_editor").val("");
            $("#question_name_show").text(qnames[count]);
            $("#question_process_show").text(count+1+"/"+qids.length);
            loadquestion(qids[count]);
            pullThumbnails(qids[count]);
            i = count;
        });

        $("#submit1").click(function(){
            submitpaper(qids[i], paperid);
        });

        // resolve the icons behavior with event delegation
        $("ul.gallery > li").click(function(event) {
            var $item = $( this );
            var $target = $( event.target );

            if ($target.is("a.ui-icon-check")){
                selectImage($item);
            }else if ($target.is("a.ui-icon-zoomin")){
                viewLargerImage( $target );
            }else if ($target.is("a.ui-icon-closethick")){
                unselectImage($item);
            }
            return false;
        });
    });

    var getProcessDialog = function(){

      var processing_dialogue = $( "#dialog-process" ).dialog({
        autoOpen: false,
        resizable: false,
        height:150,
        width:550,
        modal: true
      });

      $("#progressbar").progressbar({
        value: 100 
      });
      return processing_dialogue;
    };

    var submitanswer = function(questionid){
        getProcessDialog().dialog('open');
        answer_html = $("#answer_editor").val();
        $("#selected_diagrams li img").each(function(){
            stuthumbnail_ids += $(this).attr("id") + ",";
        });
        if (stuthumbnail_ids !== ''){
            stuthumbnail_ids = stuthumbnail_ids.substring(0, stuthumbnail_ids.length - 1);
        }
        $.ajax({type: "POST",
            url: "/student/submitanswer/",
            dataType: "json",
            data: {
                "answer_html": answer_html, 
                "stuthumbnail_ids": stuthumbnail_ids,
                "csrfmiddlewaretoken": csrfvalue,
                "questionid": questionid,
            },
            success: function(payload){
                getProcessDialog().dialog('close');
            },
            error: function(MLHttpRequest, textStatus, errorThrown){
                getProcessDialog().dialog('close');
            }
        });
    };

    var submitpaper = function(questionid, paperid){
        getProcessDialog().dialog('open');
        answer_html = $("#answer_editor").val();
        $("#selected_diagrams li img").each(function(){
            stuthumbnail_ids = $(this).attr("id");
        });
        $.ajax(
            {
                type: "POST",
                url: "/student/submitanswer/",
                dataType: "json",
                data: {
                    "answer_html": answer_html, 
                    "stuthumbnail_ids": stuthumbnail_ids,
                    "csrfmiddlewaretoken": csrfvalue,
                    "questionid": questionid,
            },
            success: function(payload){
                $.ajax(
                    {
                        type: "POST",
                        url: "/student/submitpaper/",
                        dataType: "json",
                        data: {
                            "paperid": paperid,
                            'csrfmiddlewaretoken': csrfvalue
                    },
                    success: function(payload){
                        getProcessDialog().dialog('close');
                        if(payload['state'] === 'passed'){
                            gotosummarize(paperid, true);
                        }else if (payload['state'] === 'failed'){
                            gotosummarize(paperid, false);
                        }
                    },
                    error: function(MLHttpRequest, textStatus, errorThrown){
                            getProcessDialog().dialog('close');
                        }
                });
            },
            error: function(MLHttpRequest, textStatus, errorThrown){}
        });
    };


    var loadquestion = function(questionid){
        if(questionid != -1){
            $.post("/question/stuget/",
            {
                'questionid': questionid,
                'csrfmiddlewaretoken': csrfvalue
            },
            function(payload){
                if(payload.state === "success"){
                    $("#question_editor").val(payload['question_content']);
                    $("#answer_editor").val(payload['question_stuanswer']);
                    if (payload['question_canvas'] && payload['question_canvas'].length > 0){
                        loadcanvasbtngroup(payload['question_canvas'], questionid, payload['stuanswerid']);
                    }
                }
            },
            'json');
        }
    };


    var loadcanvasbtngroup = function(canvaslist, questionid, stuanswerid){
        if($('#canvas').length === 0){
            $(".btngroup").before("<div><h5 style='margin:0 10em 0 0'>Graph Test:</h5><p class='longp btngroup' id='canvas'></p><p /><div>");
        }
        for (var i = 0; i < canvaslist.length; i += 1){
            var canvasname = canvaslist[i];
            $('#canvas').append("<a class='nyroModal blueBtn' id='canvas" + canvasname + "'>" + canvasname + "</a>");
            pullcanvas(canvasname, questionid, stuanswerid);
        }        
    
    };


    var pullcanvas = function(canvasname, questionid, stuanswerid){
        var width = 1330;
        var height = 700;
        var nmopts = {
            sizes: { 
                initW: width,
                initH: height,
                w: width,
                h: height,
                minW: width,
                minH: height
            },
            callbacks: {
                beforeShowCont: function() { 
                    width = $('.nyroModalCont').width();
                    height = $('.nyroModalCont').height();
                    $('.nyroModalCont iframe').css('width', width);
                    $('.nyroModalCont iframe').css('height', height);
                }
            }
        };

        var canvasid = '#canvas' + canvasname;
        $(canvasid).attr({
                'href': '/canvas/?canvasname=' + canvasname + '&questionid=' + questionid + '&stuanswerid=' + stuanswerid + '&view=undefined',
                'target': '_blank',
        });
        $(canvasid).nm(nmopts);
    };


    var pullThumbnails = function(questionid){
        $.post("/question/studentthumbnails/",
        {
            'questionid': questionid,
            'csrfmiddlewaretoken': csrfvalue
        },
        function(payload) {
            if(payload.state === "success"){
                thumbnails = payload['thumbnails'];
                stuthumbnails = payload['stuthumbnails'];
                thumbhtml = makeimagethumbnailhtml(thumbnails, false);
                stuthumbhtml = makeimagethumbnailhtml(stuthumbnails, true);
                var $list = $( "ul", $("#thumbnails"));
                $( "#thumbnails li").remove();
                $(thumbhtml).appendTo($list);
                $list = $( "ul", $("#stuthumbnails"));
                $( "#stuthumbnails li").remove();
                $(stuthumbhtml).appendTo($list);
                bindImageIconClick();
            }
        }, 'json');
    };


    var makeimagethumbnailhtml = function(thumbnails, selected){
        var thumbhtml = '';
        for (var t in thumbnails){
            thumbhtml+='<li class="ui-widget-content ui-corner-tr">';
            thumbhtml+='<h6 class="ui-widget-header">' + thumbnails[t][1].slice(0,5) + '...' + '</h6>';
            thumbhtml+='<img src="/static/' + thumbnails[t][0] + '" id=' + thumbnails[t][3] +' alt="' + thumbnails[t][1] + '" width="96" height="72"></img>';
            thumbhtml+='<a href="/static/' + thumbnails[t][2] + '" title="View Larger Image" class="ui-icon ui-icon-zoomin">View Larger</a>';
            if (selected){
                thumbhtml += '<a href="#" title="Unselect Image" class="ui-icon ui-icon-closethick">unselect</a>';
            }else{
                thumbhtml += '<a href="#" title="Select Image" class="ui-icon ui-icon-check">select</a>';
            }
        }
        return thumbhtml;
    };


    var bindImageIconClick = function(){

        var $imagesfrom = $( "#possible_diagrams" );
        var $imagesto = $( "#stuthumbnails" );

        $( "li", $imagesfrom ).draggable({
            cancel: "a.ui-icon", // clicking an icon won't initiate dragging
            revert: "invalid", // when not dropped, the item will revert back to its initial position
            helper: "clone",
        });

        $imagesto.droppable({
            accept: "#possible_diagrams > li",
            activeClass: "ui-state-highlight",
            drop: function(event, ui){
                selectImage(ui.draggable);
            }
        });

        $imagesfrom.droppable({
            accept: "#selected_diagrams li",
            activeClass: "ui-state-highlight",
            drop: function(event, ui) {
                unselectImage(ui.draggable);
            }
        });

        var unselect_icon = "<a href='#' title='Unselect this image' class='ui-icon ui-icon-closethick'>Unselect</a>";
        var selectImage = function( $item ) {
            $item.fadeOut(function() {
                var thumbnails = [];
                /*
                   var $list = $( "ul", $imagesto ).length ?
                   $( "ul", $imagesto ) :
                   $( "<ul class='gallery ui-helper-reset'/>" ).appendTo( $imagesto );
                   */
                var $list = $( "ul", $imagesto );

                $item.find( "a.ui-icon-check" ).remove();
                $item.append( unselect_icon ).appendTo( $list ).fadeIn();
            });
        };

        // image recycle function
        var check_icon = "<a href='#' title='Select this image' class='ui-icon ui-icon-check'>Select image</a>";
        var unselectImage = function( $item ) {
            $item.fadeOut(function() {
                $item
                .find( "a.ui-icon-closethick" )
                .remove()
                .end()
                .css( "width", "96px")
                .append( check_icon )
                .find( "img" )
                .css( "height", "72px" )
                .end()
                .appendTo( $imagesfrom )
                .fadeIn();
            });
        };

        var viewLargerImage = function( $link ) {
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
        };

        // resolve the icons behavior with event delegation
        $( "ul.gallery > li" ).click(function( event ) {
            var $item = $( this );
            var $target = $( event.target );
            if ( $target.is( "a.ui-icon-check" ) ) {
                selectImage( $item );
            } else if ( $target.is( "a.ui-icon-zoomin" ) ) {
                viewLargerImage( $target );
            } else if ( $target.is( "a.ui-icon-closethick" ) ) {
                unselectImage( $item );
            }
            return false;
        });
    } 


    var gotosummarize = function(paperid, passed){
        if (passed){
            timeused = $('#time_show').text().split('/')[0];
            clearInterval(timeoutTimer);
            url = "/student/summarize/?paperid=" + paperid + "&time=" + timeused;
        }else{
            clearInterval(timeoutTimer);
            url = "/student/summarize/?paperid=" + paperid + "&passed=0";
        }
        window.location.href = url;
    };


    function refreshtimeout(){
        $.post("/student/checktime/",
        {
            'paperid':paperid,
            'csrfmiddlewaretoken':csrfvalue
        },
        function(payload) {
            if(payload['timeout'] === "yes"){
                var process = $("#question_process_show").text().split('/');
                var index = Number(process[0]);
                var total = Number(process[1]);
                submitpaper(qids[index], paperid);
            }else if (payload){
                $("#time_show").text(payload['timeleft'] + '/' + payload['totaltime']);
            }
        }, 'json');
    }

    refreshtimeout();

})(jQuery);

