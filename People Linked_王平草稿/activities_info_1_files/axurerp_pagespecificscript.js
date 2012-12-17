for(var i = 0; i < 34; i++) { var scriptId = 'u' + i; window[scriptId] = document.getElementById(scriptId); }

$axure.eventManager.pageLoad(
function (e) {

});
gv_vAlignTable['u31'] = 'center';gv_vAlignTable['u21'] = 'top';gv_vAlignTable['u15'] = 'top';gv_vAlignTable['u13'] = 'top';gv_vAlignTable['u11'] = 'top';gv_vAlignTable['u3'] = 'top';gv_vAlignTable['u7'] = 'top';gv_vAlignTable['u23'] = 'top';gv_vAlignTable['u25'] = 'center';document.getElementById('u18_img').tabIndex = 0;

u18.style.cursor = 'pointer';
$axure.eventManager.click('u18', u18Click);
InsertAfterBegin(document.body, "<div class='intcases' id='u18LinksClick'></div>")
var u18LinksClick = document.getElementById('u18LinksClick');
function u18Click(e) 
{
windowEvent = e;


	ToggleLinks(e, 'u18LinksClick');
}

InsertBeforeEnd(u18LinksClick, "<div class='intcaselink' onmouseout='SuppressBubble(event)' onclick='u18Clicku5b73aee6722c45d4a9c35bfdc08d05cb(event)'>Case 1</div>");
function u18Clicku5b73aee6722c45d4a9c35bfdc08d05cb(e)
{

	self.location.href=$axure.globalVariableProvider.getLinkUrl('home_admin.html');

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

InsertBeforeEnd(u20LinksClick, "<div class='intcaselink' onmouseout='SuppressBubble(event)' onclick='u20Clicku13eba0aebf234f9cb17b74f70959afa0(event)'>Case 1</div>");
function u20Clicku13eba0aebf234f9cb17b74f70959afa0(e)
{

	self.location.href=$axure.globalVariableProvider.getLinkUrl('rooms_admin.html');

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

InsertBeforeEnd(u22LinksClick, "<div class='intcaselink' onmouseout='SuppressBubble(event)' onclick='u22Clicku075144e0eb854814af2b48cd2943b603(event)'>Case 1</div>");
function u22Clicku075144e0eb854814af2b48cd2943b603(e)
{

	self.location.href=$axure.globalVariableProvider.getLinkUrl('activities_admin.html');

	ToggleLinks(e, 'u22LinksClick');
}
