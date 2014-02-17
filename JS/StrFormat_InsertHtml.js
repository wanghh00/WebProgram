//// '{1} is {0}, {2} is {0} too'.format('red', 'apple', 'oracle')

/*
var divPos = document.getElementById(div_id);
divPos.insertAdjacentHTML('beforeend', strHTML);
*/

//// window.addEventListener('DOMContentLoaded', genLinks);

if (!String.prototype.format) {
  	String.prototype.format = function() {
    	var args = arguments;
    	return this.replace(/{(\d+)}/g, function(match, number) { 
      		return typeof args[number] != 'undefined' ? args[number] : match;
    	});
  	};
};

var genStockChartImgLnk = function(symbol) {
	//return '<img class="chart1" src="http://stockcharts.com/c-sc/sc?s={0}&p=D&b=5&g=0&i=t45406117198&r={1}"/>'.format(symbol, Date.now());
	imghtml = '<img class="chart1" src="http://stockcharts.com/c-sc/sc?s={0}&p=D&b=5&g=0&i=t45406117198&r={1}"/>'.format(symbol, Date.now());
	return '<a href="http://stockcharts.com/h-sc/ui?s={0}" target="_blank">{1}</a>'.format(symbol, imghtml);
};

var genFinvizImgLnk = function(symbol) {
	//return '<img class="chart1" src="http://finviz.com/chart.ashx?t={0}&ty=c&ta=1&p=d&s=l"/>'.format(symbol);
	imghtml = '<img class="chart1" src="http://finviz.com/chart.ashx?t={0}&ty=c&ta=1&p=d&s=l"/>'.format(symbol);
	return '<a href="http://finviz.com/quote.ashx?t={0}&ty=c&ta=1&p=d" target="_blank">{1}</a>'.format(symbol, imghtml);
};

var genHtml4LstSymbol = function(lstSymbol, div_id) {
	var divPos = document.getElementById(div_id);

	var lst = []
	for (var x in lstSymbol) {
		htmlImg = genStockChartImgLnk(lstSymbol[x])+genFinvizImgLnk(lstSymbol[x]);
		//console.log("let me see", genFinvizImgLnk(lstSymbol[x]));
		lst.push('<div class="one_row"><p>{0}</p>{1}</div>'.format(lstSymbol[x], htmlImg));
	};
	divPos.insertAdjacentHTML('beforeend', lst.join(""));
};

var genLinks = function(event) {
	//alert("Hello...");
	var lstCurPos = ['SPY', "VJET", "FXI", "DCTH","OPK","ASTM",'DNDN','GERN'];
	var lstSimulation = ['LUV','OIS','PLUG'];
	var lstTopWatch =   ['KNDI','HIMX','FCEL','MEI','MNKD','DRYS','NOW','MCK','ETFC', 'CAF','LITB', 'MU', 'MDBX', 'ANV', 'GS', 'DIS',  'GMCR', 'HPQ','SCTY', 
						'FNMA','DDD','SSYS','EWZ','PBR','JCP','CAMT','TSLA',"CECE"];
	var lstTech = ["GOOG", "AAPL", 'YHOO', "FB", "TWTR", "LNKD","AMZN", "EBAY","GRPN", "YOKU", "Z", "TRLA",'Yelp','SINA','SOHU','BIDU','SYNA','MU',
					'MSFT','FSL','MXL','AMD','IBM','NFLX'];
    
	genHtml4LstSymbol(lstCurPos, 'cur_pos');
	genHtml4LstSymbol(lstTopWatch, 'top_watch');
	genHtml4LstSymbol(lstTech, 'tech');
	genHtml4LstSymbol(lstSimulation, 'simulation');

};

window.addEventListener('DOMContentLoaded', genLinks);
