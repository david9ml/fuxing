;(function($, undef) {
    var config = {
        toolbar: [],
        height: 430,
        toolbarStartupExpanded: false,
        readOnly: true,
        font_style: {
			element: 'span',
            styles: {'font-size': '24px'}
		}
    };

    var qids = [];
    var qnames = [];
    var qlength = 0;
    var qindex = 0;
    var pindex = 0;
    var originmark;

    $(function(){
        var ctrlDown = false;
            var ctrlKey = 17, vKey = 86, cKey = 67;

                $(document).keydown(function(e)
                    {
                    if (e.keyCode == ctrlKey) ctrlDown = true;
                    }).keyup(function(e)
                    {
                    if (e.keyCode == ctrlKey) ctrlDown = false;
                    });

                $(document).keydown(function(e)
                {
                if (ctrlDown && (e.keyCode == vKey || e.keyCode == cKey)) return false;
                });

        if(group === 'teachers'){
            studentid = stuids[0];
            $('#backbutton').attr("href", '/report/teacher');
            $('#backbutton').text("Back to Teacher's Assignment Record");
            $('#editmark').editable(function(mark, settings){
                var reg = /^[0-9]*$/;
                if (reg.test(mark)){
                    originmark = mark;
                    $.ajax({
                        type: "post",
                        url: "/teacher/updatemark/",
                        datatype: "json",
                        data: {"studentid": studentid,
                                "questionid": qids[qindex],
                                "mark": mark,
                                "csrfmiddlewaretoken": csrfvalue
                            },
                        success: function(payload) {
                            if(payload['state'] === 'success'){
                                $('#editmark').text(payload['mark']);
                            }
                        },
                        error:function(xmlhttprequest, textstatus, errorthrown) {
                            $('#editmark').text(originmark);
                            return this;
                        }
                    });
                }else{
                    $("#editmark").text(originmark);
                }
            },{
                type:"text",
                onblur:"submit",
                style: 'display:inline'
            });
        }else{
            $('#backbutton').attr("href", '/report/student');
            $('#backbutton').text("Back to Student's Assignment Record");
        }
        $("#question_editor").ckeditor(config);
        $("#stuanswer_editor").ckeditor(config);
        $("#omitted_editor").ckeditor(config);
        if(paperid !== '' && studentid !== ''){
            var questionfound = false;
            for(var k = 0, length = pids.length; k < length; k += 1){
                if(paperid == pids[k] && studentid == stuids[k]){
                    pindex = k;
                    loadpaperinfo(pids[k]);
                    getquestionid(pids[k], stuids[k]);
                    questionfound = true;
                    break;
                }
            }
            if(!questionfound){
                loadpaperinfo(pids[0]);
                getquestionid(pids[0], stuids[0]);
            }
        }else{
            loadpaperinfo(pids[0]);
            getquestionid(pids[0], stuids[0]);
        }
        // resolve the icons behavior with event delegation
        $( "ul.gallery > li" ).click(function( event ) {
            var $item = $( this );
            var $target = $( event.target );

            if ( $target.is( "a.ui-icon-zoomin" )) {
                viewLargerImage( $target );
            }
            return false;
        });

        $("#previous").click(function(){
            if(qindex !== 0){
                qindex -= 1;
                $("#omitted_editor").val("");
                $("#question_name_show").text(qnames[qindex]);
                $("#question_process_show").text(String(qindex+1) + "/" + String(qlength+1));
                loadstuanswer(qids[qindex], stuids[0]);
                pullThumbnails(qids[qindex], stuids[0]);
            }
        });

        $("#next").click(function(){
            if(qindex !== qlength){
                qindex += 1;
                $("#omitted_editor").val("");
                $("#question_name_show").text(qnames[qindex]);
                $("#question_process_show").text(String(qindex+1) + "/" + String(qlength+1));
                loadstuanswer(qids[qindex], stuids[0]);
                pullThumbnails(qids[qindex], stuids[0]);
            }
        });

        $("#first").click(function(){
            if(qindex !== 0){
                $("#omitted_editor").val("");
                $("#question_name_show").text(qnames[0]);
                $("#question_process_show").text(1+"/"+String(qlength+1));
                loadstuanswer(qids[0], stuids[0]);
                pullThumbnails(qids[qindex], stuids[0]);
                qindex = 0;
            }
        });

        $("#last").click(function(){
            if(qindex !== qlength){
                $("#omitted_editor").val("");
                $("#question_name_show").text(qnames[qlength]);
                $("#question_process_show").text(String(qindex+1) + "/" + String(qlength+1));
                loadstuanswer(qids[qlength], stuids[0]);
                pullThumbnails(qids[qlength], stuids[0]);
                qindex = qlength;
            }
        });


        $("#next_paper").click(function(){
            if(pindex !== pids.length - 1){
                pindex += 1;
                loadpaperinfo(pids[pindex]);
                getquestionid(pids[pindex], stuids[pindex]);
            }
        });

        $("#pre_paper").click(function(){
            if(pindex !== 0){
                pindex -= 1;
                loadpaperinfo(pids[pindex]);
                getquestionid(pids[pindex], stuids[pindex]);
            }
        });

    });

    var updateomitted = function(){
        var omitted = $('#omitted_editor').val();
        $.post("/teacher/updateomitted/",
            {
                "studentid": studentid,
                "questionid": qids[qindex],
                "omitted": omitted,
                'csrfmiddlewaretoken': csrfvalue
            },
            function(payload) {

            },'json');
    }

    /********************
     *
     * get all the questions'id in the paper of a student
     *
     ********************/
    var getquestionid = function(paperid, student_id){
        $.post("/question/getid/",
                {
                    'paperid': paperid,
                    'csrfmiddlewaretoken': csrfvalue
                },
                function(payload){
                    if(payload.state === "success"){
                        qids = payload['qids'];
                        qnames = payload['qnames'];
                        qlength = qids.length - 1;
                        qindex = 0;
                        $("#question_process_show").text(String(qindex+1)+"/"+String(qlength+1));
                        $("#question_name_show").text(qnames[0]);
                        loadstuanswer(qids[0], student_id);
                        pullThumbnails(qids[0], student_id);
                    }
                },
                'json');
    };

    var loadpaperinfo = function(paperid){
		_getProcessDialog().dialog('open');
        $.post("/paper/info/",
                {
                    'paperid': paperid,
                    'csrfmiddlewaretoken': csrfvalue
                },
                function(payload){
                    if(payload.state === "success"){
		                _getProcessDialog().dialog('close');
                        $("#paper_id_show").text(payload['papername']);
                        $("#year_show").text(payload['year']);
                        $("#subject_show").text(payload['subject']);
                        $("#level_show").text(payload['level']);
                        $("#assignment_show").text(payload['assignment']);
                    }
                },
                'json');
    };

    var loadstuanswer = function(questionid, studentid){
		_getProcessDialog().dialog('open');
        if(questionid !== -1){
            $.post("/question/stuanswer/",
                    {
                        'questionid': questionid,
                        'studentid': studentid,
                        'csrfmiddlewaretoken': csrfvalue
                    },
                    function(payload){
                        if(payload.state === "success"){
                            var omitted = '';
		                    _getProcessDialog().dialog('close');
                            $("#student_name").text(payload['stuname']);
                            $("#question_editor").val(payload['question']);
                            $("#stuanswer_editor").val(payload['stuanswer']);
                            $("#editmark").text(payload['mark']);
                            originmark = payload['mark'];
                            for (var i = 0, length = payload['omitted'].length; i < length; i+=1){
                                if (payload['omitted'][i][0] === 'C'){
                                    omitted += "<span style='color:green'><p>" + payload['omitted'][i].substring(1) + "</p><span>";
                                }else if(payload['omitted'][i][0] === 'W'){
                                    omitted += "<span style='color:red'><p>" + payload['omitted'][i].substring(1) + "</p><span>";
                                }
                                else omitted += "<span style='color:red'><p>" + payload['omitted'][i] + '</p></span>';
                            }
                            $("#omitted_editor").val(omitted);
                        }
                    },
                    'json');
        }
    };

    var loadomittedanswer = function(questionid, studentid){
        if(questionid != -1){
            $.post("/question/omittedanswer/",
            {
                'questionid': questionid,
                'studentid': studentid,
                'csrfmiddlewaretoken': csrfvalue
            },
            function(payload){
                if(payload.state === "success"){
                    $("#omitted_editor").val(payload['answer_content']);
                }
            },
            'json');
        }
    };

    function pullThumbnails(questionid, studentid){
        console.log("pull thumbnails");
        $.post("/question/reportthumbnails/",
                {
                    'questionid': questionid,
                    'studentid': studentid,
                    'csrfmiddlewaretoken':csrfvalue
                },
                function(payload) {
                    if(payload.state === "success"){
                        questionthumbnails = payload['questionthumbnails'];
                        stdthumbnails = payload['stdthumbnails'];
                        stuthumbnails = payload['stuthumbnails'];

                        questionthumbhtml = makeimagethumbnailhtml(questionthumbnails);
                        var $questionlist = $( "ul", $("#questionthumbnails"));
                        $( "#questionthumbnails li").remove();
                        $(questionthumbhtml).appendTo($questionlist);

                        stdthumbhtml = makeimagethumbnailhtml(stdthumbnails);
                        var $stdlist = $( "ul", $("#stdthumbnails"));
                        $( "#stdthumbnails li").remove();
                        $(stdthumbhtml).appendTo($stdlist);

                        stuthumbhtml = makeimagethumbnailhtml(stuthumbnails);
                        var $stulist = $( "ul", $("#stuthumbnails"));
                        $( "#stuthumbnails li").remove();
                        $(stuthumbhtml).appendTo($stulist);
                        bindImageIconClick();
                    }
                },'json');
    }


    function makeimagethumbnailhtml(thumbnails){
        var thumbhtml = '';
        for (t in thumbnails){
            thumbhtml += '<li class="ui-widget-content ui-corner-tr">';
            thumbhtml += '<h6 class="ui-widget-header">'+thumbnails[t][1].slice(0,5)+'...'+'</h6>';
            thumbhtml += '<img src="/static/'+thumbnails[t][0]+'"  alt="'+thumbnails[t][1]+'" width="96" height="72"></img>';
            thumbhtml += '<a href="/static/'+thumbnails[t][2]+'" title="View Larger Image" class="ui-icon ui-icon-zoomin">View Larger</a>';
        }
        return thumbhtml;
    }


    function bindImageIconClick(){

        var $imagesfrom = $( "#selected_diagrams" );
        var $imagesto = $( "#correct_diagrams" );

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
    }

	function _getProcessDialog(){
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
		return processing_dialogue;
	}


})(jQuery);

function submitform(){
    $('#stuids').val(stuids);
    $('#pids').val(pids);
    console.log($('#stuids').val());
    document.forms[0].submit();
}
