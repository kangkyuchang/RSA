import base64

def encryption(key, mod, plain_text):
    plain_text_bytes = plain_text.encode("utf-8")
    m = int.from_bytes(plain_text_bytes, byteorder="big")

    encrypted_num = pow(m, key, mod)
    byte_data = encrypted_num.to_bytes((encrypted_num.bit_length() + 7) // 8, byteorder="big")
    cipher_text = base64.b64encode(byte_data).decode('utf-8')

    return cipher_text

def decryption(key, mod, cipher_text):
    byte_data = base64.b64decode(cipher_text).decode("utf-8")
    encrypted_num = int.from_bytes(byte_data, byteorder="big")

    m = pow(encrypted_num, key, mod)
    byte_length = (m.bit_length + 7) // 8
    text_bytes = m.to_bytes(byte_length, byteorder="big")
    plain_text = text_bytes.decode("utf-8")

    return plain_text