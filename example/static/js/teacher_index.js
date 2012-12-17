/*
 * yanchao727@gmail.com
 * 15/06/2012
 *
 */
var oTable0=null;
var oTable1=null;
var oTable2=null;
var oTable3=null;
var oTable4=null;

;(function($, undef) {

    $(function(){
			var thisPage = {
				initialize: function () {//加载时执行
					$tabs = $("#tabs3").tabs({
					});
                    var tab = intemass.util.getUrl("tab");
					if(tab==2){
					$tabs.tabs('select', 1);
                    initTab2();
					}
					else if (tab==1){
					$tabs.tabs('select', 0);
                    initTab1();
					}
					else if (tab==3){
					$tabs.tabs('select', 2);
                    }
                    else{
                    initTab1();
                    }
					return false;
				}
			}

			$(thisPage.initialize());
            initTab3();

            $("a[href = '#tabs3-1']").click(function(){

                    if(oTable0===null || oTable1===null){
                        initTab1();
                    }
                    else{
                        oTable0.fnDraw();
                        oTable1.fnDraw();
                    }

            });

            $("a[href = '#tabs3-2']").click(function(){
                    if(oTable2===null || oTable3===null || oTable4===null)
                    {
                        initTab2();
                    }
                    else{
                        oTable2.fnDraw();
                        oTable3.fnDraw();
                        oTable4.fnDraw();
                    }


            });

            function initTab1(){
                    oTable0 = $('#students').dataTable( {
                        "bJQueryUI": true,
                            "bProcessing": true,
                            "sAjaxSource": "/student/getall/",
                            "width":"100px"
                    } );

                    oTable1 = $('#classrooms').dataTable( {
                        "bJQueryUI": true,
                            "bProcessing": true,
                            "sAjaxSource": "/classroom/getall/",
                    });
            }
            function initTab2(){
                    oTable2 = $('#itempools').dataTable( {
                        "bJQueryUI": true,
                            "bProcessing": true,
                            "sAjaxSource": "/itempool/getall/",
                    } );



                    oTable3 = $('#papers').dataTable( {
                        "bJQueryUI": true,
                            "bProcessing": true,
                            "sAjaxSource": "/paper/getall/",
                    } );

                    oTable4 = $('#assignments').dataTable( {
                        "bJQueryUI": true,
                            "bProcessing": true,
                            "sAjaxSource": "/assignment/getall/",
                            "iDisplayLength": 3
                    });
            }

            function initTab3(){
                    $('#id_year').textext({
                            plugins : 'focus tags',
                            prompt : 'Add one...',
                            enabled : true
                        });

                    $('#id_subject').textext({
                            plugins : 'focus tags',
                            prompt : 'Add one...',
                            enabled : true
                        });

                    $('#id_level').textext({
                            plugins : 'focus tags',
                            prompt : 'Add one...',
                            enabled : true
                        });

                    $.get('/entity/get/',function(payload){
                        if(payload['state'] == 'success'){
                        var years = quotation_filter(payload['year']);
                        var subjects = quotation_filter(payload['subject']);
                        var levels = quotation_filter(payload['level']);
                        $('#id_year').textext()[0].tags().addTags(years);
                        $('#id_subject').textext()[0].tags().addTags(subjects);
                        $('#id_level').textext()[0].tags().addTags(levels);

                        //style
                        //$(".text-button").css({ "height": "25px"});
                        //$(".text-level").css({ "height": "25px"});
                        }
                        else{
                        console.log("payloadError happened");
                        }
                    });

            }

			function quotation_filter(obj){
				for(var i in obj){
				obj[i]=obj[i].replace(/\"/g, "");
				}
				return obj;
			}

            $('#optionform').ajaxForm(function(){
                alert('refresh options ok');
            });


	});

})(jQuery);

	function deletestudent(studentid){
		var dialogue = $( "#dialog-confirm" ).dialog({
			resizable: false,
			height:150,
			modal: true,
			buttons: {
				"Delete": function() {
					$.post(STUDENTDELETE_URL,
						{studentid: studentid},
						function(){},
						'json');
					oTable0.fnDestroy();
					oTable0 = $('#students').dataTable({
						"bJQueryUI": true,
							"bProcessing": false,
							"sAjaxSource": "/student/getall/"
					});
					$( this ).dialog( "close" );

				},
			Cancel: function() {
						$( this ).dialog( "close" );
					}
			}});
	}


	function	deleteclassroom(classroomid){
		var dialogue2 = $( "#dialog-confirm2" ).dialog({
			resizable: false,
			height:150,
			modal: true,
			buttons: {
				"Delete": function() {
					$.post(CLASSROOMDELETE_URL,
						{classroomid:classroomid},
						function(){},
						'json');
					oTable1.fnDestroy();
					oTable1 = $('#classrooms').dataTable({
						"bJQueryUI": true,
							"bProcessing": false,
							"sAjaxSource": "/classroom/getall/"
					});

					$( this ).dialog( "close" );

				},
			Cancel: function() {
						$( this ).dialog( "close" );
					}
			}});
	}

	function viewclassroom(classroomid){
		location.href = "teachers/manage/viewclassroom/"+classroomid;
	}

	function deleteitempool(itempoolid){
		var dialogue3 = $( "#dialog-confirm3" ).dialog({
			resizable: false,
			height:150,
			modal: true,
			buttons: {
				"Delete": function() {
					$.post(ITEMPOOLDELETE_URL,
						{itempoolid:itempoolid},
						function(){},
						'json');
					oTable2.fnDestroy();
					oTable2 = $('#itempools').dataTable({
						"bJQueryUI": true,
							"bProcessing": false,
							"sAjaxSource": "/itempool/getall/"
					});
					$( this ).dialog( "close" );
				},
			Cancel: function() {
						$( this ).dialog( "close" );
					}
			}
		});
	}

	function deletepaper(paperid){
		var PAPER_URL;
		var dialogue4 = $( "#dialog-confirm4" ).dialog({
			resizable: false,
			height:150,
			modal: true,
			buttons: {
				"Delete": function() {
					$.post(PAPERDELETE_URL,
						{paperid:paperid},
						function(){},
						'json');
					oTable3.fnDestroy();
					oTable3 = $('#papers').dataTable({
						"bJQueryUI": true,
							"bProcessing": false,
							"sAjaxSource": "/paper/getall/"
					});
					$( this ).dialog( "close" );

				},
			Cancel: function() {
						$( this ).dialog( "close" );
					}
			}
		});
	}

	function deleteassignment(assignmentid){
		var dialogue5 = $( "#dialog-confirm5" ).dialog({
			resizable: false,
			height:150,
			modal: true,
			buttons: {
				"Delete": function() {
					$.post(ASSIGNMENTDELETE_URL,
						{assignmentid:assignmentid},
						function(){},
						'json');
					oTable4.fnDestroy();
					oTable4 = $('#assignments').dataTable({
						"bJQueryUI": true,
							"bProcessing": false,
							"sAjaxSource": "/assignment/getall/"
					});
					$( this ).dialog( "close" );
				},
			Cancel: function() {
						$( this ).dialog( "close" );
					}
			}
		});
	}


