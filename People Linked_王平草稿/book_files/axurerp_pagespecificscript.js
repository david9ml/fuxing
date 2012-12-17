for(var i = 0; i < 40; i++) { var scriptId = 'u' + i; window[scriptId] = document.getElementById(scriptId); }

$axure.eventManager.pageLoad(
function (e) {

});
gv_vAlignTable['u17'] = 'top';gv_vAlignTable['u21'] = 'top';gv_vAlignTable['u15'] = 'top';gv_vAlignTable['u13'] = 'top';gv_vAlignTable['u1'] = 'center';gv_vAlignTable['u39'] = 'top';gv_vAlignTable['u9'] = 'top';gv_vAlignTable['u7'] = 'top';gv_vAlignTable['u23'] = 'top';document.getElementById('u24_img').tabIndex = 0;

u24.style.cursor = 'pointer';
$axure.eventManager.click('u24', u24Click);
InsertAfterBegin(document.body, "<div class='intcases' id='u24LinksClick'></div>")
var u24LinksClick = document.getElementById('u24LinksClick');
function u24Click(e) 
{
windowEvent = e;


	ToggleLinks(e, 'u24LinksClick');
}

InsertBeforeEnd(u24LinksClick, "<div class='intcaselink' onmouseout='SuppressBubble(event)' onclick='u24Clickufc742ae03ea9494dbbad8fb798917d20(event)'>Case 1</div>");
function u24Clickufc742ae03ea9494dbbad8fb798917d20(e)
{

	self.location.href=$axure.globalVariableProvider.getLinkUrl('activities.html');

	ToggleLinks(e, 'u24LinksClick');
}
gv_vAlignTable['u25'] = 'top';document.getElementById('u20_img').tabIndex = 0;

u20.style.cursor = 'pointer';
$axure.eventManager.click('u20', u20Click);
InsertAfterBegin(document.body, "<div class='intcases' id='u20LinksClick'></div>")
var u20LinksClick = document.getElementById('u20LinksClick');
function u20Click(e) 
{
windowEvent = e;


	ToggleLinks(e, 'u20LinksClick');
}

InsertBeforeEnd(u20LinksClick, "<div class='intcaselink' onmouseout='SuppressBubble(event)' onclick='u20Clicku0076afb0091d41d88ea95a69d9eef2cf(event)'>Case 1</div>");
function u20Clicku0076afb0091d41d88ea95a69d9eef2cf(e)
{

	self.location.href=$axure.globalVariableProvider.getLinkUrl('Home.html');

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

InsertBeforeEnd(u22LinksClick, "<div class='intcaselink' onmouseout='SuppressBubble(event)' onclick='u22Clicku0ecdb9c73add4e3aac1b2cc1f6a453e1(event)'>Case 1</div>");
function u22Clicku0ecdb9c73add4e3aac1b2cc1f6a453e1(e)
{

	self.location.href=$axure.globalVariableProvider.getLinkUrl('rooms.html');

	ToggleLinks(e, 'u22LinksClick');
}
