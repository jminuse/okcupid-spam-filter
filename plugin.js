(function(){

function get_string_between(string,a,b){
	var start = string.indexOf(a);
	var end = string.indexOf(b, start);
	return string.slice(start,end);
}

function delete_thread(content) {
	var form = get_string_between(content, 'id="delete_button"', '</form>');
	var form_data = {deletethread:'DELETE'};
	jQuery.each(content.match( /type="hidden" name="([^"]+)" (?:id="[^"]+" )?value="([^"]+)"/g ), function( index, match_string ) {
		var m = match_string.match( /type="hidden" name="([^"]+)" (?:id="[^"]+" )?value="([^"]+)"/ );
		form_data[ m[1] ] = m[2];
	});
	console.log(form_data);
	var thread_params = {readmsg: 'true', threadid: form_data.threadid, folder: '1'};
	jQuery.post('http://www.okcupid.com/mailbox?'+jQuery.param(thread_params), form_data);
}

function score_message(message) {
	var bad_strings = ['oriental', 'exotic'];
	var good_strings = [];
	var score = 0;
	jQuery.each(bad_strings, function( i, string ) {
		if(message.search(new RegExp(string, "i"))!=-1) {
			score -= 10;
		}
	});
	jQuery.each(good_strings, function( i, string ) {
		if(message.search(new RegExp(string, "i"))!=-1) {
			score += 10;
		}
	});
	return score;
}

function process_thread(content) {
	var message = get_string_between(content, '<div class="message_body">', '</div>');
	if(score_message(message) < 0) {
		console.log('Deleting');
		console.log(message);
		setTimeout(function() {
			delete_thread(content);
		}, 500*Math.random() );
	}
}

jQuery.get('http://www.okcupid.com/messages', function(messages_response) {
	jQuery.each(messages_response.match(/threadid="([^"]+)"/g), function( index, m ) {
		thread = m.match(/"([^"]+)"/)[1];
		var thread_params = {readmsg: 'true', threadid: thread, folder: '1'};
		setTimeout(function(){
			jQuery.get('http://www.okcupid.com/messages', thread_params, process_thread );
		}, 500*(index+Math.random()) );
	});
});

})();

