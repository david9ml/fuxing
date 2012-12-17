for(var i = 0; i < 34; i++) { var scriptId = 'u' + i; window[scriptId] = document.getElementById(scriptId); }

$axure.eventManager.pageLoad(
function (e) {

});
gv_vAlignTable['u31'] = 'center';gv_vAlignTable['u21'] = 'top';gv_vAlignTable['u15'] = 'top';gv_vAlignTable['u13'] = 'top';gv_vAlignTable['u11'] = 'top';gv_vAlignTable['u3'] = 'top';gv_vAlignTable['u27'] = 'center';gv_vAlignTable['u7'] = 'top';gv_vAlignTable['u23'] = 'top';document.getElementById('u18_img').tabIndex = 0;

u18.style.cursor = 'pointer';
$axure.eventManager.click('u18', u18Click);
InsertAfterBegin(document.body, "<div class='intcases' id='u18LinksClick'></div>")
var u18LinksClick = document.getElementById('u18LinksClick');
function u18Click(e) 
{
windowEvent = e;


	ToggleLinks(e, 'u18LinksClick');
}

InsertBeforeEnd(u18LinksClick, "<div class='intcaselink' onmouseout='SuppressBubble(event)' onclick='u18Clicku266f91b94db34d98983c816fd35cd559(event)'>Case 1</div>");
function u18Clicku266f91b94db34d98983c816fd35cd559(e)
{

	self.location.href=$axure.globalVariableProvider.getLinkUrl('Home.html');

	ToggleLinks(e, 'u18LinksClick');
}
gv_vAlignTable['u19'] = 'top';document.getElementById('u20_img').tabIndex = 0;

u20.style.cursor = 'pointer';
$axure.eventManager.click('u20', u20Click);
InsertAfterBegin(document.body, "<div class='intcases' id='u20LinksClick'></div>")
var u20LinksClick = document.getElementById('u20LinksClick');
function u20Click(e) 
{
windowEvent = e;


	ToggleLinks(e, 'u20LinksClick');
}

InsertBeforeEnd(u20LinksClick, "<div class='intcaselink' onmouseout='SuppressBubble(event)' onclick='u20Clicku3053600468bb482dab8f9aa1aaed4e66(event)'>Case 1</div>");
function u20Clicku3053600468bb482dab8f9aa1aaed4e66(e)
{

	self.location.href=$axure.globalVariableProvider.getLinkUrl('rooms.html');

	ToggleLinks(e, 'u20LinksClick');
}
gv_vAlignTable['u5'] = 'top';document.getElementById('u22_img').tabIndex = 0;

u22.style.cursor = 'pointer';
$axure.eventManager.click('u22', u22Click);
InsertAfterBegin(document.body, "<div class='intcases' id='u22LinksClick'></div>")
var u22LinksClick = document.getElementById('u22LinksClick');
function u22Click(e) 
{
windowEvent = e;


	ToggleLinks(e, 'u22LinksClick');
}

InsertBeforeEnd(u22LinksClick, "<div class='intcaselink' onmouseout='SuppressBubble(event)' onclick='u22Clicku989c3bff6afc4636b515fd54760e9fc6(event)'>Case 1</div>");
function u22Clicku989c3bff6afc4636b515fd54760e9fc6(e)
{

	self.location.href=$axure.globalVariableProvider.getLinkUrl('activities.html');

	ToggleLinks(e, 'u22LinksClick');
}
