from cryptography.fernet import Fernet


def main() -> None:
    key = Fernet.generate_key()
    print(str(key, encoding='utf-8'))
    b = bytes(u'你好!', encoding='utf-8')
    ferr = Fernet(key)
    cipher = ferr.encrypt(b)
    ciphertext = str(cipher, encoding='utf-8')
    print(str(ciphertext))
    print(str(ferr.decrypt(cipher), encoding='utf-8'))


if __name__ == '__main__':
    main()
