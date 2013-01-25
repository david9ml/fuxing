// JavaScript Document

//	<script type="text/javascript">
        $().ready(function() {
			var options = {
				height: 650,
				width: 980,
				navHeight: 25,
				labelHeight: 25,
				onMonthChanging: function(dateIn) {
					//this could be an Ajax call to the backend to get this months events
					//var events = [ 	{ "EventID": 7, "StartDate": new Date(2009, 1, 1), "Title": "10:00 pm - EventTitle1", "URL": "#", "Description": "This is a sample event description", "CssClass": "Birthday" },
					//				{ "EventID": 8, "StartDate": new Date(2009, 1, 2), "Title": "9:30 pm - this is a much longer title", "URL": "#", "Description": "This is a sample event description", "CssClass": "Meeting" }
					//];
					//$.jMonthCalendar.ReplaceEventCollection(events);
					return true;
				},
				onEventLinkClick: function(event) {
					//alert("event link click");
					return true;
				},
				onEventBlockClick: function(event) {
					//alert("block clicked");
					return true;
				},
				onEventBlockOver: function(event) {
					//alert(event.Title + " - " + event.Description);
					return true;
				},
				onEventBlockOut: function(event) {
					return true;
				},
				onDayLinkClick: function(date) {
					//alert(date.toLocaleDateString());
					return true;
				},
				onDayCellClick: function(date) {
					//alert(date.toLocaleDateString());
					return true;
				}
			};

			/************************Andy Yan***********************************/

            var events = null;

            $.ajax({
                type: "get",
                url: "/activity/getall_activities/",
                datatype: "json",
                success: function(data){
                    console.log(data);
                    var data_json = eval('(' + data + ')');
                    events = data_json;
                    console.log(events);
			        $.jMonthCalendar.Initialize(options, events);
                    $("#Button").click(function() {
                        $.jMonthCalendar.AddEvents(extraEvents);
                    });

                    $("#ChangeMonth").click(function() {
                        $.jMonthCalendar.ChangeMonth(new Date(2013, 1, 1));
                    });

                },
                error:function(xmlhttprequest, textstatus, errorthrown) {
                    return this;
                }

            });
            /***************************
			var events = [ 	{ "EventID": 1, "Date": "2013-01-12T00:00:00.0000000", "Title": "10:00 pm - 微软ceo做客", "URL": "/", "Description": "This is a sample event description", "CssClass": "Meeting" },
							{ "EventID": 2, "Date": "2013-01-28T00:00:00.0000000", "Title": "9:30 pm - this is a much longer title", "URL": "events_info.html", "Description": "This is a sample event description", "CssClass": "Meeting" },
							{ "EventID": 3, "StartDateTime": new Date(2013, 0, 20), "Title": "9:30 pm - this is a much longer title blah blah blah", "URL": "events_info.html", "Description": "This is a sample event description", "CssClass": "Meeting" },
							{ "EventID": 4, "StartDateTime": "2013-04-14", "Title": "9:30 pm - this is a much longer title", "URL": "events_info.html", "Description": "This is a sample event description", "CssClass": "Meeting" }
			];
            ****************************/

/***************************
            var events = [
    {
        "EventID": 1,
        "Date": "2013-01-12T00:00:00.0000000",
        "Title": "10:00 am-微软ceo做客",
        "URL": "/activity/info",
        "description": "",
        "CssClass": "Meeting"
    },
    {
        "EventID": 2,
        "Date": "2013-01-12T00:00:00.0000000",
        "Title": "1:00 pm-oracle lecture",
        "URL": "/activity/info",
        "description": "",
        "CssClass": "Meeting"
    },
    {
        "EventID": 3,
        "Date": "2013-01-12T00:00:00.0000000",
        "Title": "talk show contest3",
        "URL": "/activity/info",
        "description": "",
        "CssClass": "Meeting"
    },
    {
        "EventID": 4,
        "Date": "2013-01-12T00:00:00.0000000",
        "Title": "talk show contest4",
        "URL": "/activity/info",
        "description": "",
        "CssClass": "Meeting"
    }];
****************************/
			//var newoptions = { };
			//var newevents = [ ];
			//$.jMonthCalendar.Initialize(newoptions, newevents);



            /*************
			var extraEvents = [	{ "EventID": 5, "StartDateTime": new Date(2013, 0, 11), "Title": "10:00 pm - EventTitle1", "URL": "#", "Description": "This is a sample event description", "CssClass": "Birthday" },
								{ "EventID": 6, "StartDateTime": new Date(2013, 0, 20), "Title": "9:30 pm - this is a much longer title", "URL": "#", "Description": "This is a sample event description", "CssClass": "Meeting" }
			];
            ***************/

});
/*</script>*/
