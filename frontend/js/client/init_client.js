let client = new zerorpc.Client()

client_port = 4242

client.connect("tcp://127.0.0.1:" + client_port.toString())