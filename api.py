import re, time, random
import requests

bad_strings = ['3some']
good_strings = []

def delete_thread(session, content):
	form_start = content.find('id="delete_button"')
	form = content[form_start:content.find('</form>', form_start)]
	hidden_values = re.findall('type="hidden" name="([^"]+)" (?:id="[^"]+" )?value="([^"]+)"', form)
	form_data = {'deletethread':'DELETE'}
	for h in hidden_values:
		form_data[ h[0] ] = h[1]
	delete_response = session.post('http://www.okcupid.com/mailbox', data=form_data, params=thread_data)

def login(username, password):
	session = requests.Session()
	credentials = {'username': username, 'password': password, 'dest': '/home'}
	login_response = session.post('https://www.okcupid.com/login', data=credentials)
	return session


session = login('', '')

time.sleep(1+random.random()*2)
messages_response = session.get('http://www.okcupid.com/messages')

thread_ids = re.findall('threadid="([^"]+)"', messages_response.content)

for thread in thread_ids:
	thread_data = {'readmsg': 'true', 'threadid': thread, 'folder': 1}
	time.sleep(1+random.random()*2)
	get_thread = session.get('http://www.okcupid.com/messages', params=thread_data)
	message_start = get_thread.content.find('<div class="message_body">')
	message = get_thread.content[message_start:get_thread.content.find('</div>', message_start)]
	message = message.lower()
	score = 0
	
	for string in bad_strings:
		if string in message: score -= 10
	for string in good_strings:
		if string in message: score += 10
	
	if score < 0:
		delete_thread(session, get_thread.content)


