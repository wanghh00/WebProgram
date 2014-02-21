// Reference
// http://stackoverflow.com/questions/3596583/javascript-detect-an-ajax-event

var objDiag = {
	lstAjaxReq: [],
	lstJsErr: [],
	xmlhttprequest_open: XMLHttpRequest.prototype.open,
};

XMLHttpRequest.prototype.open = function(method,url) {
	objDiag.xmlhttprequest_open.apply(this, arguments);
	objDiag.lstAjaxReq.push(method + ' ' + url);
}

window.onerror = function(msg, url, line_num) {
	objDiag.lstJsErr.push(msg + ' <' + url + ':' + line_num+'>');
	return false;
}
