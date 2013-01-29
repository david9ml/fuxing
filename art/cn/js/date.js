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
					alert("block clicked");
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
					alert(date.toLocaleDateString());
					return true; 
				},
				onDayCellClick: function(date) { 
					alert(date.toLocaleDateString());
					return true; 
				}
			};
			
			/************************Andy Yan***********************************/
			
			var events = [ 	{ "EventID": 1, "StartDateTime": new Date(2013, 0, 18), "Title": "19:30——联客答谢会", "URL": "http://www.douban.com/event/18121298/", "Description": "This is a sample event description", "CssClass": "Meeting" },
							{ "EventID": 2, "Date": "2013-01-27T00:00:00.0000000", "Title": "迎春联欢会", "URL": "http://www.douban.com/event/18146349/", "Description": "This is a sample event description", "CssClass": "Meeting" },
							{ "EventID": 3, "StartDateTime": new Date(2013, 1, 20), "Title": "9:30 pm - this is a much longer title", "URL": "#", "Description": "This is a sample event description", "CssClass": "Meeting" },
							{ "EventID": 4, "StartDateTime": "2013-04-14", "Title": "9:30 pm - this is a much longer title", "URL": "#", "Description": "This is a sample event description", "CssClass": "Meeting" }
			];
			
			//var newoptions = { };
			//var newevents = [ ];
			//$.jMonthCalendar.Initialize(newoptions, newevents);

			
			$.jMonthCalendar.Initialize(options, events);
			
			
			
			
			var extraEvents = [	{ "EventID": 5, "StartDateTime": new Date(2013, 0, 11), "Title": "10:00 pm - EventTitle1", "URL": "#", "Description": "This is a sample event description", "CssClass": "Birthday" },
								{ "EventID": 6, "StartDateTime": new Date(2013, 0, 20), "Title": "9:30 pm - this is a much longer title", "URL": "#", "Description": "This is a sample event description", "CssClass": "Meeting" }
			];
			
			$("#Button").click(function() {					
				$.jMonthCalendar.AddEvents(extraEvents);
			});
			
			$("#ChangeMonth").click(function() {
				$.jMonthCalendar.ChangeMonth(new Date(2013, 1, 1));
			});
        });
		
/*</script>*/