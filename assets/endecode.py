import sys
import base64
from Crypto.Cipher import AES


class AESCipher(object):
    def __init__(self):
        self.bs = 16
        self.key = '`?.F(fHbN6XK|j!t'
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def encrypt(self, raw):
        raw = self._pad(raw)
        encrypted = self.cipher.encrypt(raw)
        encoded = base64.b64encode(encrypted)
        return str(encoded, 'utf-8')

    def decrypt(self, raw):
        decoded = base64.b64decode(raw)
        decrypted = self.cipher.decrypt(decoded)
        return str(self._unpad(decrypted), 'utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


if __name__ == '__main__':
    plaintext = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTMxNjM3NTMyLCJlbWFpbCI6Imh0Y3Z0YzU5QGdtYWlsLmNvbSIsIm9yaWdfaWF0IjoxNTMxNjM3NTAyfQ.G2Gp3Kfx--mI3MQf_L0aet4_Wq-oQvqK_mdPuXhIX0g'

    encrypted = AESCipher().encrypt(plaintext)
    print('Encrypted: %s' % encrypted)

    decrypted = AESCipher().decrypt(encrypted)
    print('Decrypted: %s' % decrypted)
