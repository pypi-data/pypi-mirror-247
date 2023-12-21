"""
    Play by Play- Caesar's Cipher Program
    Substitution cipher
    By Gabriel Okundaye, gabriel.okundaye@statogale.com 🌍
"""
from caesar_cipher \
import alphabets as ca, get_input as gi, encryption as ce, decryption as de, messages as m

def main():
    """The Main program"""
    jobs = ("encryption", "decryption")
    
    # Display welcome message
    m.welcome()
    
    # Display Menu
    m.menu()
    
    while True:
        # Ask user if they want to do an encryption or a decryption or exit the program.
        user = gi.ask_user()
        
        # Display outro message and quit program if user response was not yes
        if(m.outro(user)) == "break":
            break
        
        # What job? 1=1-1=0=encryption, 2=2-1=1=decryption
        job = jobs[int(user) - 1]
        
        
        # Get text, shift and validate input from user
        text, shift = tuple(gi.text_shift(ca.alphabets, job))

        # Caesar cipher encryption/decryption
        if job == jobs[0]:        
            # Get the cipher text from the plain text input
            plain_text  = text
            cipher_text = ce.encrypt_text(plain_text, shift, ca.alphabets)
        else:
            # Get the plain text from the cipher text input
            cipher_text = text
            plain_text  = de.decrypt_text(cipher_text, shift, ca.alphabets) 
        

        # Display the text message result to the user 
        m.results(plain_text, shift, cipher_text, job)
        
        # Render the caesar cipher quote and bottom border separately
        # Avoids blocking display of results when quote is not yet available
        # Although quote is faster after first load
        m.quote(plain_text)

        # Clear variables from the local namespace
        del plain_text
        del cipher_text
        del text
        del shift

if __name__ == "__main__":
    main()