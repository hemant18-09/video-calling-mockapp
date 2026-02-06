
import json
import time
import struct
import base64
import os
import sys
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class TokenInfo:
    def __init__(self, token, error_code, error_message):
        self.token = token
        self.error_code = error_code
        self.error_message = error_message

def make_nonce():
    # Official Zego impl uses random.randint(-2^63, 2^63 - 1)
    # But usually just need 8 bytes random
    # Let's match typical implementation exactly
    return int(time.time() * 1000)

def generate_token04(app_id, secret, user_id, effective_time, payload=""):
    try:
        app_id = int(app_id)
        create_time = int(time.time())
        expire_time = create_time + effective_time
        # Generate a random nonce. 
        # CAUTION: JavaScript backend sometimes uses current time as nonce. 
        # Python Zego assistant uses random.
        nonce = random.randint(100000, 99999999) 
        
        token_data = {
            "app_id": app_id,
            "user_id": user_id,
            "nonce": nonce,
            "ctime": create_time,
            "expire": expire_time,
            "payload": payload
        }
        
        # Compact JSON (no spaces)
        plaintext = json.dumps(token_data, separators=(',', ':'))
        print(f"Debug: Plaintext: {plaintext}")
        
        # Encryption
        # Secret must be 32 bytes.
        if len(secret) != 32:
             print(f"WARNING: Secret length {len(secret)} !- 32")
             # Adjust if needed, but assuming user input is correct 32 chars
             if len(secret) > 32:
                 key = secret[:32].encode("utf-8")
             else:
                 key = (secret + "0" * (32 - len(secret))).encode("utf-8")
        else:
             key = secret.encode("utf-8")
             
        # IV must be 16 bytes.
        # Official Zego Py uses: iv = os.urandom(16)
        iv = os.urandom(16)
        
        # AES CBC
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
        
        # Pack
        # format: [expire (8)] [iv_len (2)] [iv] [content_len (2)] [content]
        # All Big Endian
        
        out = bytearray()
        out.extend(struct.pack("!q", expire_time))
        out.extend(struct.pack("!H", len(iv))) # 'H' is unsigned short (2 bytes)
        out.extend(iv)
        out.extend(struct.pack("!H", len(ciphertext))) # 'H' is unsigned short
        out.extend(ciphertext)
        
        # Base64
        b64 = base64.b64encode(out).decode("utf-8")
        final_token = "04" + b64
        
        print(f"Debug: Token Success. Length: {len(final_token)}")
        return TokenInfo(final_token, 0, "")

    except Exception as e:
        print(f"Error: {e}")
        return TokenInfo("", 1, str(e))
