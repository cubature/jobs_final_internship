/*
* Test.
* 
* @param {Object} req Cloud Function request context.
* @param {Object} res Cloud Function response context.
*/
'use strict';

exports.helloHttp = function helloHttp () {
	response = "Sample res from webhook"

	res.setHeader('Content-Type', 'application/json');
	res.send(JSON.stringify({
		'speech' : response, 
		'displayText' : response
	}));
}