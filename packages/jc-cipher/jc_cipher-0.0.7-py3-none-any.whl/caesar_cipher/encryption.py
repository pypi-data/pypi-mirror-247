def encrypt_letter(letter, shift, alphabets):
    """ Returns the cipher letter based on the encryption formular En(x) = (x + n) mod 26. """
    if letter == " ":
        encrypted_letter = letter
    else:
        encrypted_letter_index = (alphabets.index(letter) + shift) % 26
        encrypted_letter       = alphabets[encrypted_letter_index]
    return encrypted_letter
 
def encrypt_text(plain_text, shift, alphabets):
    """ Returns the cipher text based on the output of encrypt_letter function """      
    # Get the cipher text from the plain text input
    encrypted_text_list = [encrypt_letter(letter, shift, alphabets) for letter in plain_text]
    encrypted_text      = ''.join(encrypted_text_list)
    return encrypted_text

