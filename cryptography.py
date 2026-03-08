import base64

byte_length = 6

def encryption(key, mod, plain_text):
    encrypted_str = list()
    for char in plain_text:
        code_point = ord(char)
        encrypted_num = pow(code_point, key, mod)

        byte_data = encrypted_num.to_bytes(byte_length, byteorder="big")
        encode_data = base64.b64encode(byte_data).decode('utf-8')
        encrypted_str.append(encode_data)
    return "".join(encrypted_str)


def decryption(key, mod, cipher_text):
    decrypted_str = list()
    split_length = (byte_length * 8) // 6
    for i in range(0, len(cipher_text), split_length):
        encrypted_data = cipher_text[i:i+split_length]

        decode_data = base64.b64decode(encrypted_data).decode("utf-8")
        encrypted_num = int.from_bytes(decode_data, byteorder="big")

        code_point = pow(encrypted_num, key, mod)

        char = chr(code_point)
        decrypted_str.append(char)
    return "".join(decrypted_str)