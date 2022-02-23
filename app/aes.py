from Cryptodome.Cipher.AES import new
from Cryptodome.Cipher.AES import block_size
from Cryptodome.Cipher.AES import MODE_CBC
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
from Cryptodome.Random import get_random_bytes

# aes option
MODE = MODE_CBC

# padding option
STYLE = "pkcs7"
BLOCK_SIZE = block_size


def _get_secret() -> bytes:
    try:
        with open(".MEMO_SECRET", mode="rb") as key_reader:
            memo_secret = key_reader.read()
            if len(memo_secret) != 32:
                raise TypeError
    except (FileNotFoundError, TypeError):
        with open(".MEMO_SECRET", mode="wb") as key_writer:
            memo_secret = get_random_bytes(32)
            key_writer.write(memo_secret)

    return memo_secret


def _get_cipher(iv: bytes):
    return new(
        key=_get_secret(),
        mode=MODE,
        iv=iv,
    )


def encrypt(text: str) -> str:
    cipher = _get_cipher(
        iv=get_random_bytes(16)
    )

    return ".".join(
        (
            cipher.iv.hex(),
            cipher.encrypt(
                plaintext=pad(
                    data_to_pad=text.encode("utf8"),
                    block_size=BLOCK_SIZE,
                    style=STYLE
                )
            ).hex()
        )
    )


def decrypt(payload: str) -> str:
    iv, text = payload.split(".")

    cipher = _get_cipher(iv=bytes.fromhex(iv))

    return unpad(
        padded_data=cipher.decrypt(
            bytes.fromhex(text)
        ),
        block_size=BLOCK_SIZE,
        style=STYLE
    ).decode("utf8")
