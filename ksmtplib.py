import socket
import datetime
import re
import ssl
from email.base64mime import body_encode as encode_base64

class KSMTPException(OSError):
    """Base class for all exceptions raised by this module."""

class KSMTPServerDisconnected(KSMTPException):
    """Disconnection exception class."""

class KSMTPResponseException(KSMTPException):
    """Response exception class."""
    def __init__(self, code, msg):
        self.smtp_code = code
        self.smtp_error = msg
        self.args = (code, msg)

_MAXLINE = 512

def _fix_eols(data):
    return  re.sub(r'(?:\r\n|\n|\r(?!\n))', '\r\n', data)

class KSMTP(object):
    def __init__(self, debug_level = 0):
        self.timeout = socket._GLOBAL_DEFAULT_TIMEOUT
        self.debuglevel = debug_level
    
    def debug(self, *args):
        if self.debuglevel>0:
            print(datetime.datetime.now(), end=' ')
            for arg in args:
                if isinstance(arg, str):
                    arg = arg.replace('\r\n', '\\r\\n')
                print(arg, end=' ')
            print()

    def getreply(self):
        resp = []
        if self.file is None:
            self.file = self.sock.makefile('rb')
        while 1:
            try:
                line = self.file.readline(_MAXLINE + 1)
            except OSError as e:
                self.close()
                raise KSMTPServerDisconnected("Connection unexpectedly closed: "
                                             + str(e))
            if not line:
                self.close()
                raise KSMTPServerDisconnected("Connection unexpectedly closed")
            if self.debuglevel > 0:
                self.debug('reply:', repr(line))
            if len(line) > _MAXLINE:
                self.close()
                raise KSMTPResponseException(500, "Line too long.")
            resp.append(line[4:].strip(b' \t\r\n'))
            code = line[:3]
            try:
                errcode = int(code)
            except ValueError:
                errcode = -1
                break
            if line[3:4] != b"-":
                break

        errmsg = b"\n".join(resp)
        if self.debuglevel > 0:
            self.debug('reply: retcode (%s); Msg: %a' % (errcode, errmsg))
        return errcode, errmsg

    def close(self):
        self.sock = None
        self.file = None
    
    def get_code(response : tuple):
        return response[0]
    
    def ehlo(self):
        cmd = 'ehlo 1.0.0.127.in-addr.arpa\r\n'
        code, resp = self.sendcmd_getreply(cmd)
        if code != 250:
            return None

    def sendcmd_getreply(self, s : str):
        if self.sock:
            if isinstance(s, str):
                s = s.encode('ascii')
            if self.debuglevel > 0:
                self.debug('send', repr(s))
            self.sock.sendall(s)
        else:
            raise KSMTPException('please connect first.\n')
        return self.getreply()

    def connect(self, host : str, port : int):
        self.host = host
        self.port = port
        self.sock = socket.create_connection((host, port))
        self.file = None
        code, resp = self.getreply()
        if code == 220:
            return (code, resp)
        else:
            raise KSMTPException('can not connect.')
    
    def login(self, user, password):
        self.ehlo()
        chanllenge_times = 1
        userandpass = ('\0%s\0%s' %(user, password))
        userandpass = encode_base64(userandpass.encode('ascii'), eol='') # base64 protocol.
        cmd = 'AUTH PLAIN %s\r\n' %userandpass
        code, resp = self.sendcmd_getreply(cmd)
        while code != 235 and chanllenge_times <= 5: # login poll.
            code, resp = self.sendcmd_getreply(cmd)
        if code == 235 or code == 250: # login successfully or already login.
            return (code, resp)
        else:
            raise KSMTPException('can not login.')
        
    def start_tls(self):
        self.ehlo()
        cmd = 'STARTTLS\r\n'
        self.file = None
        code, repl = self.sendcmd_getreply(cmd)
        if code == 220 or code == 235:
            context = ssl.create_default_context()
            self.sock = context.wrap_socket(self.sock, server_hostname=self.host)
            self.file = None
            return (code, repl)
        else:
            raise KSMTPException('can not start TLS.')

    def check_email_exception(self, code):
        if code != 250 and code != 354:
            raise KSMTPException('can not email.')

    def email(self, From : str, To : list, Content : str):
        Content = (_fix_eols(Content)).encode('ascii') + b"." + b"\r\n"
        cmd = 'mail FROM:<%s> size=%d\r\n' %(From, len(Content))
        code, _ = self.sendcmd_getreply(cmd)
        self.check_email_exception(code)
        for to in To:
            cmd = 'rcpt TO:<%s>\r\n' %(to)
            code, _ = self.sendcmd_getreply(cmd)
        self.check_email_exception(code)
        cmd = 'data\r\n'
        code, _ = self.sendcmd_getreply(cmd)
        self.check_email_exception(code)
        cmd = Content
        code, resp = self.sendcmd_getreply(cmd)
        self.check_email_exception(code)
        return (code, resp)

    





    