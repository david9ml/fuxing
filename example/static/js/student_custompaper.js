/*
 * yanchao727@gmail.com
 * 15/06/2012
 *
 */

;(function($, undef) {

	var setting = {
		check: {
				   enable: true
			   },
		data: {
				  simpleData: {
								  enable: true
							  }
			  },
		callback: {
					  onCheck: zTreeOnCheck 
				  }
	};


    $(function(){
		pullZtreeData();
		var view = intemass.util.getUrl('view');

        $('#id_duration').timepicker({});
		$('#id_papername').hide();
		setEditableText();
		$(".editable").editable(function(value,settings){
			var data = $('#id_papername').val(); 
			$("#id_papername").val(value);
			return $('#id_papername').val();
		},{
			type:"text",
			onblur:"submit",
			tooltip:"Click to Edit...",
			onedit:function(value, settings){
			},
			style: 'width:120px;display:inline'
		});

		$("#id_paperid").change(function(){
			style: 'display:inline;'
			pullZtreeData();
			setEditableText();
		});

		//add some css for select
		$('#id_paperid').css("width","140px");
		$('#id_paperid').css("margin","0");
		$('#id_paperid').css("padding","0");

		if(view){
			$("#id_papername").attr("disabled", true);
			$("#button").hide();
		}

	});
	function setSelectedNodes(zTree){
		var sNodes = zTree.getCheckedNodes();
		var qids = [];
		if (sNodes.length > 0) {
			for (node in sNodes){
				if (sNodes[node].getParentNode() != null)
					qids.push(sNodes[node].qid);
			}
			$("#snum").text(qids.length);
		}else{
			$("#snum").text("0");
		}
		return qids;
	}

	function zTreeOnCheck(event, treeId, treeNode) {
		var treeObj = $.fn.zTree.getZTreeObj("questions");
		var qids=setSelectedNodes(treeObj);
		if (qids.length>0){
			$("#id_questionlist").val(qids);
		}
	}

	function setCheck() {
		var type, zTree;
		zTree = $.fn.zTree.getZTreeObj("questions");
		type = {
			"Y": "ps",
			"N": "ps"
		};
		zTree.setting.check.chkboxType = type;
		setSelectedNodes(zTree);
	}

	function pullZtreeData(){
		var curpaperid=$("#id_paperid").val();
		var view = intemass.util.getUrl('view'); 
		$.ajax({
			type: "POST",
			url: "/paper/getquestions/",
			dataType: "json",
			data: {"paperid":curpaperid,"view":view},
			success: function(data) {
				qnum=data[0]['qnum']
				if (qnum && qnum!=''){
					$("#qnum").text(qnum);
				}else{
					$("#qnum").text("0");
				}
				data.shift();
				$.fn.zTree.init($("#questions"), setting, data);
				return setCheck();
			},
			error:function(XMLHttpRequest, textStatus, errorThrown) {
					  $("#snum").text("0");
					  $("#qnum").text("0");
					  return this;
				  }
		});
	}


	function setEditableText(){
		var selpapername=$('#id_paperid').children('option:selected').text();
		//console.log(selpapername);
		$('#id_papername').val(selpapername);
		$(".editable").text($('#id_papername').val());
	}

})(jQuery);

function submitform(){
    var selqlist=$("#id_questionlist").val();
    if (!selqlist){
        intemass.ui.showclientmsg("You have to choose one question at least!");
    }else{
        var selpapername=$("#id_papername").val();
        if(!selpapername || selpapername ===""){
        intemass.ui.showclientmsg("Paper name cannot be empty");
        }else if (selpapername && selpapername =="New Paper"){
        intemass.ui.showclientmsg("Please choose a better paper name than \"New Paper\"");
        }else{
            document.forms[0].submit();
        }
    }
}

