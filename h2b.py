name = ".MEMO_SECRET"

try:
    stream = open(name, mode="rb").read()
    print(stream.hex())
except FileNotFoundError:
    stream = bytes.fromhex(input("hex="))
    with open(name, mode="wb") as q:
        q.write(stream)
