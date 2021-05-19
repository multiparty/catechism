import base64
import json


def decode_file(filename):
	base64_text = open(filename)
	base64_text = base64_text.readlines()

	base64_bytes = base64_text[0].encode('ascii')
	str_bytes = base64.b64decode(base64_bytes)
	final = str_bytes.decode('ascii')

	return final


if __name__ == "__main__":

	# decode and store config of credentials for curia
	curia_config = decode_file('/config/curia_config')
	f = open("/data/curia_config.txt", "w")
	f.write(curia_config)
	f.close()

	# decode and store congregation config
	congregation_config = decode_file('/config/config')
	f = open("/data/congregation_config.json", "w")
	f.write(congregation_config)
	f.close()

	# decode and store congregation protocol
	protocol = decode_file('/config/protocol')
	f = open("/data/protocol.py", "w")
	f.write(protocol)
	f.close()
