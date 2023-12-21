def decrypt_letter(letter, shift, alphabets):
    """ Returns the plain letter based on the decryption formular Dn(x) = (x - n) mod 26. """
    if letter == " ":
        decrypted_letter = letter
    else:
        decrypted_letter_index = (alphabets.index(letter) - shift) % 26
        decrypted_letter       = alphabets[decrypted_letter_index]
    return decrypted_letter
 
def decrypt_text(cipher_text, shift, alphabets):
    """ Returns the plain text based on the output of decrypt_letter function """      
    # Get the plain text from the cipher text input
    decrypted_text_list = [decrypt_letter(letter, shift, alphabets) for letter in cipher_text]
    decrypted_text      = ''.join(decrypted_text_list)
    return decrypted_text
