$(function(){
	$("#chinese_link").css("cursor","pointer").click(function(){
		var urlString = window.location.toString();
        if(urlString.search("/cn") == -1){
		//location.href = urlString+"cn/";
        //var pos = urlString.search("/");
        //alert(urlString.substring(pos));
        //alert(urlString.substring(0, pos));
		}
		else{
		}
	});
});
