import socket
import datetime
from email.base64mime import body_encode as encode_base64

class KSMTPException(OSError):
    """Base class for all exceptions raised by this module."""

class KSMTPServerDisconnected(KSMTPException):
    """Not connected to any SMTP server.

    This exception is raised when the server unexpectedly disconnects,
    or when an attempt is made to use the SMTP instance before
    connecting it to a server.
    """

class KSMTPResponseException(KSMTPException):
    """Base class for all exceptions that include an SMTP error code.

    These exceptions are generated in some instances when the SMTP
    server returns an error code.  The error code is stored in the
    `smtp_code' attribute of the error, and the `smtp_error' attribute
    is set to the error message.
    """

    def __init__(self, code, msg):
        self.smtp_code = code
        self.smtp_error = msg
        self.args = (code, msg)

class KSMTP(object):
    def __init__(self, debug_level = 0):
        self.timeout = socket._GLOBAL_DEFAULT_TIMEOUT
        self.debug_level = debug_level
    
    def debug(self, *args):
        if self.debug_level>0:
            print(datetime.datetime.now(), end=' ')
            for arg in args:
                print(arg.replace('\r\n', '\\r\\n'), end=' ')
            print()

    def connect(self, server : str, port : int):
        self.debug('connecting: %s:%d' %(server, port))
        self.sock = socket.create_connection((server, port), self.timeout)
    
    def send(self, s):
        cmd = s.encode('ascii')
        self.debug('send: %s' %(s))
        if self.sock:
            try:
                self.sock.sendall(cmd)
            except OSError as e:
                raise e
        else:
            raise KSMTPException('socket no found')

    def getreply(self):
        """Get a reply from the server.

        Returns a tuple consisting of:

          - server response code (e.g. '250', or such, if all goes well)
            Note: returns -1 if it can't read response code.

          - server response string corresponding to response code (multiline
            responses are converted to a single, multiline string).

        Raises SMTPServerDisconnected if end-of-file is reached.
        """
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
                self._print_debug('reply:', repr(line))
            if len(line) > _MAXLINE:
                self.close()
                raise KSMTPResponseException(500, "Line too long.")
            resp.append(line[4:].strip(b' \t\r\n'))
            code = line[:3]
            # Check that the error code is syntactically correct.
            # Don't attempt to read a continuation line if it is broken.
            try:
                errcode = int(code)
            except ValueError:
                errcode = -1
                break
            # Check if multiline response.
            if line[3:4] != b"-":
                break

        errmsg = b"\n".join(resp)
        if self.debuglevel > 0:
            self._print_debug('reply: retcode (%s); Msg: %a' % (errcode, errmsg))
        return errcode, errmsg


        errmsg = b"\n".join(resp)
        self.debug('reply: retcode (%s); Msg: %a' % (errcode, errmsg))
        return errcode, errmsg
    
    def putcmd(self, *args : str):
        cmd = ' '.join(args) + '\r\n'
        # self.debug(cmd)
        self.send(cmd)
        return cmd

    def login(self, user, password):
        cmd = 'AUTH PLAIN'
        secret = '\0%s\0%s' %(user, password)
        verify = encode_base64(secret.encode('ascii'), eol = '')
        # finalcmd = cmd + ' ' + verify + '\r\n'
        self.challenge_time = 5
        
        while(self.challenge_time > 0):
            # self.send(finalcmd)
            finalcmd = self.putcmd(cmd, verify)
            self.file = None
            code, msg = self.getreply()
            if code in (235, 503):
                return (code, msg)
            self.challenge_time -= 1
        self.debug('verify token: %s' %finalcmd)
        raise SMTPError('could not login')
    
    def sendmail(self, dst, body):
        # cmd format to send a mail:
        # rcpt TO:<addr@sth.sth[.sth]> *options
        pass





    