from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.encoding import force_bytes, force_str, force_text
from django.conf import settings
import hashlib
import logging

class LhSHA1PasswordHasher(BasePasswordHasher):
    """
    The SHA1 password hashing algorithm 
    """
    algorithm = "sha1"
    def encode(self, password, salt):
        assert password is not None
        salt = settings.LHC_SECRET
        first = hashlib.sha1(force_bytes(password)).hexdigest()
        hash = hashlib.sha1(force_bytes(password+salt+first)).hexdigest()
        return "%s$%s$%s" % (self.algorithm, salt, hash)
    
    def verify(self, password, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt)
        return encoded == encoded_2 

    def safe_summary(self, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        assert algorithm == self.algorithm
        return OrderedDict([
            (_('algorithm'), algorithm),
            (_('salt'), mask_hash(salt, show=2)),
            (_('hash'), mask_hash(hash)),
        ])