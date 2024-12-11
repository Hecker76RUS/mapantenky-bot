def get_token():
	token = open('C:\\Users\\kudrii\\PycharmProjects\\Mapantenky_bot\\TelegramAPI\\config\\APIKEY.txt', 'r')
	get_token_api = token.read()
	token.close()
	return get_token_api

def get_superuser_id():
	find_id = open('C:\\Users\\kudrii\\PycharmProjects\\Mapantenky_bot\\TelegramAPI\\config\\SUPERUSERID.txt', 'r')
	get_superuser_id_api = find_id.read()
	find_id.close()
	return get_superuser_id_api
