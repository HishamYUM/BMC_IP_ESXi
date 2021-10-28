import re  
import os
import paramiko
import openpyxl


 
def login_and_execute(host, username="admin", password="pass"):

				#ssh_server, username, password = ('kali-linux.me', 'kali', 'kali')
				ssh = paramiko.SSHClient()
				paramiko.util.log_to_file('log_filename')
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				# In case the server's key is unknown,
				# we will be adding it automatically to the list of known hosts
				ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
				# Loads the user's local known host file.
				ssh.connect(host, username=username, password=password)
				ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("esxcli hardware ipmi bmc get | greap IPv4 | cut -d ':' -f 2 ")
				BMC_IP = ssh_stdout.readlines() 
				#print(BMC_IP)
			
				second_command = 'nslookup {}'.format(server)
				ssh_stdin2, ssh_stdout2, ssh_stderr2 = ssh.exec_command(second_command)
				with open('final_output.txt', 'a+') as f:
								out_ = ssh_stdout2.readlines()
								for line in out_:
								    y = re.search("^Server", line)
								    if y:
								        f.write(line.replace("Server", "IP"))
								        break
								
								f.write("BMC IP: {}\n".format(BMC_IP))
								
								for line in out_:
								    x = re.search("^Name", line)
								    if x:
								        f.write("{}\n\n".format(line.replace("Name", "BMC Hostname")))
								        break
								

				ssh.close()
				
wookbook = openpyxl.load_workbook("Project1.xlsx")


worksheet = wookbook.active
hosts = worksheet['A']

for i in range(len(hosts)):

    login_and_execute(i)
