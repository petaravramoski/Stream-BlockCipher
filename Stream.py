import time
import secrets
import string

modNum = 10  # Modulo number that will be used for digits
modChar = 26  # Modulo number that will be used for chars

# Defining ASCII range for digits and chars (lower and upper)
asciiNum = 97  # for digits
asciiUChar = 65  # for upper chars
asciiLChar = 48  # for lower chars


# Generating a random key that will be used for the encryption process
# This is done using the secrets module python provides.
def generate_random_key(length):
    # defining the set of characters that will be used and mixed in the key, in this case its digits and chars
    characters = string.ascii_letters + string.digits

    # Generate random key
    key = ''.join(secrets.choice(characters) for _ in range(length))

    return key


def ifDigit(x, key_char, mod):
    x_char = int(x)
    if key_char.isdigit():
        key_char = int(key_char)
    else:
        key_char = ord(key_char)
    encrypted_char = (x_char + key_char) % modNum
    return chr(encrypted_char + asciiLChar)  # Convert the result back to character


def ifDigitDEC(x, key_char, mod):
    x_char = int(x)
    if key_char.isdigit():
        key_char = int(key_char)
    else:
        key_char = ord(key_char)
    decrypted_char = (x_char - key_char) % modNum
    return chr(decrypted_char + asciiLChar)  # Convert the result back to character


def ifAlpha(x, key_char, mod):
    if x.islower():
        x_char = ord(x) - asciiNum  # Convert character to its position in the alphabet (0-25)
        key_char = ord(key_char) - asciiNum
    else:
        x_char = ord(x) - asciiUChar  # Convert character to its position in the alphabet (0-25)
        key_char = ord(key_char) - asciiUChar
    encrypted_char = (x_char + key_char) % modChar
    if x.islower():
        return chr(encrypted_char + asciiNum)  # Convert the result back to c
    else:
        return chr(encrypted_char + asciiUChar)  # Convert the result back to c


def ifAlphaDEC(x, key_char, mod):
    if x.islower():
        x_char = ord(x) - asciiNum  # Convert character to its position in the alphabet (0-25)
        key_char = ord(key_char) - asciiNum
    else:
        x_char = ord(x) - asciiUChar  # Convert character to its position in the alphabet (0-25)
        key_char = ord(key_char) - asciiUChar

    decrypted_char = (x_char - key_char) % modChar
    if x.islower():
        return chr(decrypted_char + asciiNum)  # Convert the result back to c
    else:
        return chr(decrypted_char + asciiUChar)  # Convert the result back to c


def main():
    val = input("Enter your value or just click enter to use default value: ")

    if val:
        print("You entered:", val)
    else:
        default_value = "Exams are on red USB drive in JO 18.103. Password is CaKe314."
        print("No input provided. Using default string: ", default_value)
        val = default_value

    x = val
    encrypter = ""
    decrypter = ""

    key = generate_random_key(len(x))

    print("Message that will be Encrypted:", x)
    time.sleep(1)
    print("Encryption Process...")
    time.sleep(3)

    # This here is where the encryption takes places
    for i in range(len(x)):
        if x[i].isdigit():  # if char is a digit perform the statement below
            encrypter += ifDigit(x[i], key[i], modNum)  # appending encrypted digit to encrypter var
        elif x[i].isalpha():  # if char is a alphanumeric perform the statement below
            encrypter += ifAlpha(x[i], key[i], modChar)  # appending encrypted char to encrypter var
        else:
            encrypter += x[i]  # if its not a digit or char then just add it in as it is

    print("Encrypted message:", encrypter)
    time.sleep(1.5)



    # Ask the user for decryption key until it's correctly entered
    while True:
        print(key)
        decryption_key = input("Enter decryption key: ")
        if decryption_key == key:
            print("Key matched. Decrypting...")
            break
        else:
            print("Invalid key. Try again.")

    # This here is where the decryption takes places
    for i in range(len(encrypter)):
        if encrypter[i].isdigit():  # if char is a digit perform the statement below
            decrypter += ifDigitDEC(encrypter[i], key[i], modNum)  # appending decrypted digit to decrypted var
        elif encrypter[i].isalpha():  # if char is a alphanumeric perform the statement below
            decrypter += ifAlphaDEC(encrypter[i], key[i], modChar)  # appending decrypted char to decrypter var
        else:
            decrypter += encrypter[i]  # if its not a digit or char then just add it in as it is

    print("Decryption Process...")
    time.sleep(1.5)
    print("Decrypted message:", decrypter)


if __name__ == "__main__":
    main()