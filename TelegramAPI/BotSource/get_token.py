def get_token():
	token = open('APIKEY.txt', 'r')
	get_token_api = token.read()
	token.close()
	return get_token_api

def get_superuser_id():
	id = open('SUPERUSERID.txt', 'r')
	get_superuser_id_api = id.read()
	id.close()
	return get_superuser_id_api