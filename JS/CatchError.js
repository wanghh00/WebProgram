
/*

function recordJSError(msg, url, line_num) {
	var divJSErr = document.getElementById("js_err");
    if (!divJSErr) {
        divJSErr = document.createElement("div");
        divJSErr.id = "js_err";
        divJSErr.style.display = "none";
        document.body.appendChild(divJSErr);
    }
    divJSErr.innerHTML += "<p>" + url + ":" + line_num + " " + msg + "</p>";
    return false;
}

window.onerror = recordJSError;
*/


window.onerror = function(msg, url, line_num) { document.write('hehe...'); return false; }
