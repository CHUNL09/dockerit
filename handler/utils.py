import pycurl
import os

def encrypt_pass(password,iterations=1000,salt=-1):
    import hashlib, binascii
    import os
    salt_len = 24
    iterations = int(iterations)
    dk_len = 24
    if salt == -1:
        salt = binascii.hexlify(os.urandom(salt_len))
    else:
        salt = salt.encode('utf8')
    encrypted_pass = binascii.hexlify(hashlib.pbkdf2_hmac('sha256',password.encode('utf8'),salt,iterations,dk_len))
    return '%d:%s:%s' % (iterations, salt.decode('utf8'), encrypted_pass.decode('utf8'))

def validate_pass(db_password,raw_password):
    iterations,salt,_ = db_password.split(':')
    print(iterations,salt)
    raw_encrypted_pass = encrypt_pass(raw_password,iterations,salt)
    if db_password == raw_encrypted_pass:
        return True
    else:
        return False

def ping_port(ip,port):
    import socket
    cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cs.settimeout(2)
    address = (str(ip),int(port))
    try:
        cs.connect((address))
    except socket.error as e:
        print("ping port error: %s" %e)
        return -1 # means error
    cs.close()
    return 0

class HTTP(object):

    @staticmethod
    def get(reqUrl):
        import urllib.request
        get_req = urllib.request.Request(reqUrl)
        response = urllib.request.urlopen(get_req)
        ret = response.read().decode('utf8')
        return ret

    @staticmethod
    def post(reqUrl):
        import urllib.request
        get_req = urllib.request.Request(reqUrl,method='POST')
        response = urllib.request.urlopen(get_req)
        ret = response.read().decode('utf8')
        return ret

    @staticmethod
    def post_file(reqUrl,data,hedaders):
        import urllib.request
        get_req = urllib.request.Request(reqUrl, method='POST',data=data,headers=hedaders)
        try:
            response = urllib.request.urlopen(get_req,timeout=300)
            ret = response.read().decode('utf8')
        except Exception as e:
            print(e)
            ret = e
        return ret

    @staticmethod
    def delete(reqUrl):
        import urllib.request
        get_req = urllib.request.Request(reqUrl, method='DELETE')
        response = urllib.request.urlopen(get_req)
        ret = response.read().decode('utf8')
        return ret

class TemplateFunc(object):

    @staticmethod
    def substr(strings,start,length):
        str_temp = strings

        return str_temp[int(start)-1,int(start)+int(length)-1]

class MyCurl(object):
    @staticmethod
    def get(self):
        pass
    @staticmethod
    def post_file(url,file_path):
        curl_obj = pycurl.Curl()
        curl_obj.setopt(curl_obj.URL, url)

        curl_obj.setopt(curl_obj.HTTPPOST, [
            ('fileupload', (
                # upload the contents of this file
                curl_obj.FORM_FILE,file_path,
            )),
        ])
        curl_obj.setopt(pycurl.HTTPHEADER, ['Content-Type:application/tar'])
        filesize = os.path.getsize(file_path)
        curl_obj.setopt(curl_obj.POSTFIELDSIZE, filesize)
        fin = open(file_path, 'rb')
        curl_obj.setopt(curl_obj.READFUNCTION, fin.read)

        res = curl_obj.perform()
        curl_obj.close()
        return res