var page = require('webpage').create(),
	system = require('system'),
	fname;

if (system.args.length !== 2) {
	console.log('Usage: '+system.args[0]+' url');
	phantom.exit(1);
} else {
	url = system.args[1];
	url = 'https://signin.ebay.com/ws/eBayISAPI.dll?SignIn'
	page.open(url, function() {

	});
}