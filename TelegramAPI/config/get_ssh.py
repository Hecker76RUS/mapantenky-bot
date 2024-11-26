def get_ssh_key():
	ssh_key = open('SSHKEY.txt', 'r')
	is_get_ssh_key = ssh_key.read()
	ssh_key.close()
	return is_get_ssh_key