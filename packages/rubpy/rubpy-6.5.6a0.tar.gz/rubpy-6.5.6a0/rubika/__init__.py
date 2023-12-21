import base64
from json import dumps, loads
from random import randint, choice
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from requests import post


class Encryption:
    def __init__(self, auth: str, private_key: str = None):
        self.key = bytearray(self._secret(auth), "UTF-8")
        self.iv = bytearray.fromhex('00000000000000000000000000000000')
        if private_key:
            self.keypair = RSA.import_key(private_key.encode("utf-8"))

    def _secret(self, e):
        t = e[0:8]
        i = e[8:16]
        n = e[16:24] + t + e[24:32] + i
        s = 0
        while s < len(n):
            c = n[s]
            if c.isdigit():
                t = chr((ord(c) - ord('0') + 5) % 10 + ord('0'))
                n = self._replace_char_at(n, s, t)
            else:
                t = chr((ord(c) - ord('a') + 9) % 26 + ord('a'))
                n = self._replace_char_at(n, s, t)
            s += 1
        return n

    def _replace_char_at(self, s, index, new_char):
        return s[0:index] + new_char + s[index + len(new_char):]

    def encrypt(self, text):
        raw = pad(text.encode('UTF-8'), AES.block_size)
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        enc = aes.encrypt(raw)
        result = base64.b64encode(enc).decode('UTF-8')
        return result

    def decrypt(self, text):
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        dec = aes.decrypt(base64.urlsafe_b64decode(text.encode('UTF-8')))
        result = unpad(dec, AES.block_size).decode('UTF-8')
        return result

    def make_sign_from_data(self, data_enc: str):
        sha_data = SHA256.new(data_enc.encode("utf-8"))
        signature = pkcs1_15.new(self.keypair).sign(sha_data)
        return base64.b64encode(signature).decode("utf-8")

    def decrypt_rsa_oaep(self, private: str, data_enc: str):
        key_pair = RSA.import_key(private.encode("utf-8"))
        return PKCS1_OAEP.new(key_pair).decrypt(base64.b64decode(data_enc)).decode("utf-8")

class Bot:
    def __init__(self, auth, private_key=None, is_auth_send=True, base64decode_private=False, user_agent=None):
        if is_auth_send:
            self.auth = Encryption.change_auth_type(auth)
            self.auth_send = auth
        else:
            self.auth = auth
            self.auth_send = Encryption.change_auth_type(auth)
        if base64decode_private:
            private_key = loads(base64.b64decode(private_key).decode("utf-8"))['d']
        self.enc = Encryption(self.auth, private_key if private_key else None)
        self.default_client = {
            "app_name": "Main",
            "app_version": "4.3.1",
            "platform": "Web",
            "package": "web.rubika.ir",
            "lang_code": "fa"
        }
        self.default_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"

    @staticmethod
    def change_auth_type(auth_enc):
        n = ""
        lowercase = "abcdefghijklmnopqrstuvwxyz"
        uppercase = "abcdefghijklmnopqrstuvwxyz".upper()
        digits = "0123456789"
        for s in auth_enc:
            if s in lowercase:
                n += chr(((32 - (ord(s) - 97)) % 26) + 97)
            elif s in uppercase:
                n += chr(((29 - (ord(s) - 65)) % 26) + 65)
            elif s in digits:
                n += chr(((13 - (ord(s) - 48)) % 10) + 48)
            else:
                n += s
        return n

    def get_url(self):
        p = None
        while 1:
            try:
                datax = {"api_version": "4", "method": "getDCs", "client": self.default_client}
                p = post(json=datax, url='https://getdcmess.iranlms.ir/', headers={
                    'User-Agent': self.default_agent,
                    'Origin': 'https://web.rubika.ir',
                    'Referer': 'https://web.rubika.ir/',
                    'Host': 'getdcmess.iranlms.ir'
                }).json()
                p = p['data']['default_api_urls'][1]
                break
            except Exception as e:
                print(e)
                continue
        return p

    def send_data(self, input_data, method, client=None, api_version="6", tmp=False):
        p = None
        while 1:
            try:
                data_ = {
                    "api_version": api_version,
                    "auth" if not tmp else "tmp_session": self.auth_send if not tmp else self.auth,
                    "data_enc": self.enc.encrypt(dumps({
                        "method": method,
                        "input": input_data,
                        "client": client if client else self.default_client
                    })),
                }
                if api_version == "6" and not tmp:
                    data_["sign"] = self.enc.make_sign_from_data(data_["data_enc"])
                url = "https://messengerg2c" + str(randint(1, 69)) + ".iranlms.ir/"
                p = post(json=data_, url=url, headers={
                    'User-Agent': self.default_agent,
                    'Origin': 'https://web.rubika.ir',
                    'Referer': 'https://web.rubika.ir/',
                    'Host': url.replace("https://", "").replace("/", "")
                })
                p = p.json()
                break
            except Exception as e:
                print(e)
                continue
        p = loads(self.enc.decrypt(p["data_enc"]))
        return p

    def send_message(self, chat_id, text, message_id=None):
        input_data = {
            "object_guid": chat_id,
            "rnd": f"{randint(100000, 900000)}",
            "text": text,
        }
        method = "sendMessage"
        if message_id:
            input_data["reply_to_message_id"] = message_id
        return self.send_data(input_data, method)

    @staticmethod
    def make_random_tmp_session():
        chars = "abcdefghijklmnopqrstuvwxyz"
        tmp = "".join(choice(chars) for _ in range(32))
        return tmp

    def send_code(self, phone, pass_key=None, send_type="SMS"):
        input_data = {
            "phone_number": phone,
            "send_type": send_type
        }
        if pass_key:
            input_data['pass_key'] = pass_key
        method = "sendCode"
        tmp = self.make_random_tmp_session()
        b = Bot(tmp, False)
        return tmp, b.send_data(input_data, method, tmp=True)

    @staticmethod
    def rsa_key_generate():
        key_pair = RSA.generate(1024)
        public = Encryption.change_auth_type(base64.b64encode(key_pair.publickey().export_key()).decode("utf-8"))
        private = key_pair.export_key().decode("utf-8")
        return public, private

    def sign_in(self, tmp, phone, phone_code, hash_val, public_key=None):
        public, private = self.rsa_key_generate()
        input_data = {
            "phone_number": phone,
            "phone_code_hash": hash_val,
            "phone_code": str(phone_code),
            "public_key": public if not public_key else public_key
        }
        method = "signIn"
        b = Bot(tmp, is_auth_send=False)
        request = b.send_data(input_data, method, tmp=True)
        print(request)
        if request['status'] == "OK" and request['data']['status'] == "OK":
            auth = self.enc.decrypt_rsa_oaep(private, request['data']['auth'])
            user_guid = request['data']['user']['user_guid']
            return auth, user_guid, private
        else:
            return None

    def register_device(self, system_version, device_model, device_hash):
        input_data = {
            "token_type": "Web",
            "token": "",
            "app_version": "WB_4.3.1",
            "lang_code": "fa",
            "system_version": system_version,
            "device_model": device_model,
            "device_hash": device_hash
        }
        method = "registerDevice"
        return self.send_data(input_data, method)

    def get_my_sticker_sets(self):
        input_data = {}
        method = "getMyStickerSets"
        return self.send_data(input_data, method)
