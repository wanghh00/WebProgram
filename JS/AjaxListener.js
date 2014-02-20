// Reference
// http://stackoverflow.com/questions/3596583/javascript-detect-an-ajax-event
var ajaxListener = {
	lstReq: []	
	orgOpen: XMLHttpRequest.prototype.open,
};

XMLHttpRequest.prototype.open = function(method,url) {
	ajaxListener.orgOpen.apply(this, arguments);
	self.lstReq.push('Method:' + method + ' Url:'+url);
}

