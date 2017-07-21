from paramiko import client
'''
ssh class is use to connect to server using paramiko module.
Used client library
after connection method sendCommand is used to send the command using ssh.
servers.csv is input file having info like serverIP,serverUserName,serverPassword
This code handles ssh connection using password and it automatically adds server in know-hosts file.
Code handles many execution of commands on remote server 

'''
class ssh:

    client=None
    def __init__(self, address, username, key_name):

        print("Connecting to server.")

        self.client = client.SSHClient()

        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
    #for password base
        #self.client.connect(address, username=username, password=key_name , look_for_keys=False)
    #for key based
        self.client.connect(address, username=username, key_filename=key_name , look_for_keys=True)

        print 'Successfully connected :'+address

    def sendCommand(self,command):
        print 'Executing commands'
        # Check if connection is made previously
        if (self.client):
            stdin,stdout,stderr = self.client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                # Print stdout data when available
                if stdout.channel.recv_ready():
                    # Retrieve the first 1024 bytes
                    alldata=stdout.channel.recv(1024)
                    while stdout.channel.recv_ready():
                        # Retrieve the next 1024 bytes
                        alldata+=stdout.channel.recv(1024)
                    print str(alldata)
                    # Print as string with utf8 encoding
                    if str(alldata)is not None:
                        print 'command executed successfully'
        else:
            print("Connection not opened.")


if __name__ == '__main__':
    serverFile = 'servers.csv'
    with open(serverFile,'r') as file:
        content=file.read()
        servers=content.split('\n')
        for server in servers:
            if not server.__eq__(''):
                values=server.split(',')
                serverIP=values[0]
                serverUserName=values[1]
                serverPassword=values[2]
                connection=ssh(serverIP, serverUserName, serverPassword)
                while True:
                    command = raw_input("Enter the command to execute :")
                    connection.sendCommand(command)
                    option = raw_input("Want to execute more command ?(y/n):")
                    if option.__ne__('y'):
                        break;







