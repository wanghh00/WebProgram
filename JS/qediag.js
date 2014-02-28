window.objDiag = {
    lstAjaxReq: [],
    lstJsErr: [],
    xmlhttprequest_open: XMLHttpRequest.prototype.open,
    jsonp_req: function (event) {
        if (event.target.nodeName == 'SCRIPT' && event.target.src) {
            objDiag.lstAjaxReq.push('jsonp ' + event.target.src);
        }
    }
};

XMLHttpRequest.prototype.open = function(method,url) {
    objDiag.xmlhttprequest_open.apply(this, arguments);
    objDiag.lstAjaxReq.push(method + ' ' + url);
}

window.onerror = function(msg, url, line_num) {
    objDiag.lstJsErr.push(msg + ' <' + url + ':' + line_num+'>');
    return false;
}
//window.addEventListener('DOMNodeInserted', objDiag.jsonp_req, false);
document.getElementsByTagName("head")[0].addEventListener('DOMNodeInserted', objDiag.jsonp_req, false);

