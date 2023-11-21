import string
import nltk
from nltk.corpus import words
nltk.download('words')

def caesar(message, key, mode, alphabet):
    result = ""
    if(mode == "decrypt"):
        if(key == -1):
            for key in range(26):
                for letter in message:
                    if letter.isalpha():
                        shift = key % 26
                        if letter.isupper():
                            result += chr(((ord(letter) - 65 - shift) % 26) + 65)
                        else:
                            result += chr(((ord(letter) - 97 - shift) % 26) + 97)
                    else:
                        result += letter
                print(result)
                result = ""
        else:
            for letter in message:
                    if letter.isalpha():
                        shift = key % 26
                        if letter.isupper():
                            result += chr(((ord(letter) - 65 - shift) % 26) + 65)
                        else:
                            result += chr(((ord(letter) - 97 - shift) % 26) + 97)
                    else:
                        result += letter
            print(result)
            result = ""

    if(mode == "encrypt"):
        for letter in message:
            if letter.isalpha():
                shift = key % 26
                if letter.isupper():
                    result += chr(((ord(letter) - 65 + shift) % 26) + 65)
                else:
                    result += chr(((ord(letter) - 97 + shift) % 26) + 97)
            else:
                result += letter
        return result
    
def is_coprime(a, m):
    # Function to check if 'a' is coprime to 'm'
    for i in range(2, min(a, m) + 1):
        if a % i == 0 and m % i == 0:
            return False
    return True

def decrypt_affine(ciphertext, a, b, m):
    # Function to decrypt a single ciphertext with given 'a' and 'b'
    a_inv = pow(a, -1, m)
    decrypted_text = ""
    for letter in ciphertext:
        if letter.isalpha():
            y = ord(letter.upper()) - ord('A')
            x = a_inv * (y - b) % m
            decrypted_text += chr(x + ord('A'))
        else:
            decrypted_text += letter
    return decrypted_text

def affine(message, mode, formula):
    result = ""
    for letter in message:
        if letter.isalpha():
            x = 0
            y = 0
            if mode == "encrypt":
                x = ord(letter.upper()) - ord('A') + 1
            elif mode == "decrypt":
                # inverse formula for decryption
                x = 26 - (ord(letter.upper()) - ord('A') + 1)  
            if(formula == "x"):
                common_words = words.words()                
                results = []
                m = 26
                highestGood = 0
                for a in filter(lambda x: is_coprime(x, m), range(1, 27)):
                    for b in range(0, 26):
                        decrypted_text = decrypt_affine(message, a, b, m)
                        words_in_text = decrypted_text.upper().split()
                        goodChars = sum(word.upper() in words_in_text for word in common_words)
                        if(goodChars > highestGood):
                            highestGood = goodChars
                            result_tuple = (a, b, decrypted_text)
                            if result_tuple not in results:
                                results.insert(0, result_tuple)
                return results
            else:
                y = useEquation(x, formula)
            y = (y - 1) % 26 + 1  # Ensure y is within the range 1-26
            result += chr(y + ord('A') - 1)  # Convert back to a character
        else:
            result += letter
    return result
    
def customFormula(message, formula):
    encrypted_message = ""
    for char in message:
        if char.isalpha():  
            x = ord(char.upper()) - ord('A') + 1  # Convert the character to a number (A=1, B=2, etc.)
            y = useEquation(x, formula)
            y = (y - 1) % 26 + 1  # Ensure y is within 1-26 range
            encrypted_message += chr(y + ord('A') - 1)  # Convert back to a character
        else:
            encrypted_message += char
    return encrypted_message

def coding_formula(formula, x):
    for i in range(len(formula)):
        if formula[i] == "x":
            if formula[i - 1].isdigit(): # kind of works? First character of formula MUST be a number (first x must have coefficient of 1 at least)
                formula = formula.replace("x", "*x")
            else:
                pass
    formula = formula.replace("^", "**")
    return eval(formula)

def useEquation(x, equation):
    return coding_formula(equation, x)

def morsecode(message, mode):
    MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
    'Y': '-.--', 'Z': '--..'
}
    result = ""
    if(mode == "encrypt"):
        for letter in message:
            if letter != " ":
                result += MORSE_CODE_DICT[letter] + " "
            else:
                result += " "
    if(mode == "decrypt"):
        # do the reverse
        MORSE_CODE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}
        message = message.split(" ")
        for letter in message:
            if letter in MORSE_CODE_DICT:
                result += MORSE_CODE_DICT[letter]
            else:
                result += letter
    return result
def rail(message, rails, mode):
    if(mode == "encrypt"):
        # Initialize rail matrix
        fence = [[' ' for _ in message] for _ in range(rails)]
        
        # Populate the rail matrix with message characters
        row, direction = 0, 1
        for char in message:
            fence[row][0] = char
            row += direction
            if row == rails - 1 or row == 0:
                direction *= -1
        
        # Read the encoded message from the rail matrix
        encoded_message = ''.join(''.join(row) for row in fence)
        return encoded_message
    if(mode == "decode"):
        fence = [[' ' for _ in message] for _ in range(rails)]

        # Initialize the positions where characters will be placed
        row, direction = 0, 1
        for i in range(len(message)):
            fence[row][i] = '*'
            row += direction
            if row == rails - 1 or row == 0:
                direction *= -1

        # Populate the rail matrix with encoded characters
        index = 0
        for r in range(rails):
            for c in range(len(message)):
                if fence[r][c] == '*':
                    fence[r][c] = message[index]
                    index += 1

        # print row 1
        print(''.join(fence[0]))
        # Read the decoded messages from the rail matrix for both rails
        decoded_message1 = ''
        decoded_message2 = ''
        row, direction = 0, 1
        for _ in range(len(message)):
            char = fence[row][_]
            decoded_message1 += char if row == 0 else ''
            decoded_message2 += char if row == 1 else ''
            row += direction
            if row == rails - 1 or row == 0:
                direction *= -1

        return decoded_message1, decoded_message2

def vigenere(text, key, mode, alphabet = string.ascii_uppercase):
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    text_as_int = [ord(i) for i in text]
    result = ""
    for i in range(len(text_as_int)):
        if(mode == "encrypt"):
            result += chr((text_as_int[i] + key_as_int[i % key_length]) % 26 + 65)
        if(mode == "decrypt"):
            result += chr((text_as_int[i] - key_as_int[i % key_length]) % 26 + 65)
    return result

def encrypt(message, cipher, key, formula, alphabet=string.ascii_uppercase):
    if cipher == "c":
        key = int(key)
        return caesar(message, key, "encrypt", alphabet)
    elif cipher == "r":
        key = int(key)
        return rail(message, key, "encrypt")
    elif cipher == "v":
        return vigenere(message, key, "encrypt", alphabet)
    elif cipher == "a":
        return affine(message, "encrypt", formula)
    elif cipher == "f":
        return customFormula(message, formula)
    elif cipher == "m":
        return morsecode(message, "encrypt")

def decrypt(message, cipher, key, formula, alphabet=string.ascii_uppercase):
    if cipher == "c":
        key = int(key)
        return caesar(message, key, "decrypt", alphabet)
    elif cipher == "r":
        key = int(key)
        return rail(message, key, "decrypt")
    elif cipher == "v":
        return vigenere(message, key, "decrypt", alphabet)
    elif cipher == "a":
        return affine(message, "decrypt", formula)
    elif cipher == "f":
        return customFormula(message, formula)
    elif cipher == "m":
        return morsecode(message, "decrypt")

def main():
    print("Welcome to the Cipher program!")
    print("Encrypt / Decrypt? (e/d)")
    choice = input("> ")
    if choice == "e":
        print("Enter the message to encrypt:")
        message = input("> ")
        print("Enter the cipher:")
        print("Caesar (c)")
        print("Rail (r)")
        print("Vigenere (v)")
        print("Affine (a)")
        print("Morse (m)")
        print("Custom Formula (f)")
        cipher = input("> ")
        encrypted = ""
        dKey = -1
        dAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        dFormula = "x"
        if(cipher == "c" or cipher == "r" or cipher == "v"):
            print("Enter the key: (leave blank for default)")
            key = input("> ")
            if(key != ""):
                dKey = key
        if(cipher == "a" or cipher == "c" or cipher == "m"):
            print("Enter the alphabet to use: (leave blank for default)")
            alphabet = input("> ")
            if(alphabet != ""):
                dAlphabet = alphabet
        if(cipher == "a" or cipher == "f"):
            print("Enter the formula to use: (leave blank for default)")
            formula = input("> ")
            if(formula != ""):
                dFormula = formula
        print("Encrypted message:")
        encrypted = encrypt(message, cipher, dKey, dFormula, dAlphabet)
        print(encrypted)
    elif choice == "d":
        print("Enter the message to decrypt:")
        message = input("> ")
        print("Enter the cipher:")
        print("Caesar (c)")
        print("Rail (r)")
        print("Vigenere (v)")
        print("Affine (a)")
        print("Morse (m)")
        print("Custom Formula (f)")
        cipher = input("> ")
        decrypted = ""
        dKey = -1
        dAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        dFormula = "x"
        if(cipher == "c" or cipher == "r" or cipher == "v"):
            print("Enter the key: (leave blank for bruteforce)")
            key = input("> ")
            if(key != ""):
                dKey = key
        if(cipher == "a" or cipher == "c" or cipher == "m"):
            print("Enter the alphabet to use: (leave blank for default)")
            alphabet = input("> ")
            if(alphabet != ""):
                dAlphabet = alphabet
        if(cipher == "a" or cipher == "f"):
            print("Enter the formula to use: (leave blank for bruteforce)")
            formula = input("> ")
            if(formula != ""):
                dFormula = formula
        print("Decrypted message:")
        decrypted = decrypt(message, cipher, dKey, dFormula, dAlphabet)
        print(decrypted)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
