from app_api.AppAPI import AppAPI
import zerorpc

def main():
    localhost = '127.0.0.1'
    server_port = 4242
    client_port = 4243

    s = zerorpc.Server(AppAPI(localhost, str(client_port)))
    server_addr = 'tcp://' + localhost + ':' + str(server_port)
    s.bind(server_addr)

    print('start running on {}'.format(server_addr))
    s.run()

if __name__ == '__main__':
    main()