from Cryptodome.Cipher.AES import new
from Cryptodome.Cipher.AES import block_size
from Cryptodome.Cipher.AES import MODE_CBC
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
from Cryptodome.Random import get_random_bytes


def get_secret() -> bytes:
    try:
        with open(".MEMO_SECRET", mode="rb") as key_reader:
            memo_secret = key_reader.read()
    except FileNotFoundError:
        with open(".MEMO_SECRET", mode="wb") as key_writer:
            memo_secret = get_random_bytes(16)
            key_writer.write(memo_secret)

    return memo_secret


class MemoAES:
    # aes option
    MODE = MODE_CBC

    # padding option
    STYLE = "pkcs7"
    BLOCK_SIZE = block_size

    def __init__(self, key: bytes or str = None, iv: hex or str = None, text: str or bytes = ""):
        if key is None:
            self.key = get_random_bytes(16)
        else:
            self.key = key if isinstance(key, bytes) else bytes.fromhex(key)

        if iv is None:
            self.iv = get_random_bytes(16)
        else:
            self.iv = iv if isinstance(iv, bytes) else bytes.fromhex(iv)

        self.text = text
        self.payload = None
        if isinstance(self.text, str):
            self.encrypt()
        else:
            self.decrypt()

    @property
    def cipher(self):
        return new(
            key=self.get_key(),
            mode=self.MODE,
            iv=self.iv,
        )

    def get_key(self) -> bytes:
        return get_secret() + self.key

    def encrypt(self) -> None:
        self.text = self.cipher.encrypt(
            pad(
                data_to_pad=self.text.encode("utf8"),
                block_size=self.BLOCK_SIZE,
                style=self.STYLE
            )
        )
        self.payload = ".".join([
            self.key.hex(),
            self.iv.hex(),
            self.text.hex(),
        ])

    def decrypt(self) -> None:
        self.payload = self.text = unpad(
            padded_data=self.cipher.decrypt(self.text),
            block_size=self.BLOCK_SIZE,
            style=self.STYLE
        ).decode("utf8")

    def __repr__(self):
        return f"<MemoAES text='{self.text!r}'>"
