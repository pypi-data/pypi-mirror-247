import time

from caesar_cipher \
import quotes as cq

def welcome():
    """Displays the welcome mesaage"""
    welcome_message = f"😇 Welcome! This is Caesar Cipher program- a substitution cipher."
    for char in welcome_message:
        print(f"{char}", end="")
        time.sleep(0.05)
        
def menu():
    """Display main menu"""
    print(f"\n1. Encryption \
            \n2. Decryption \
            \n3. Exit       \
        ")

        
def results(plain_text, shift, cipher_text, job):
    """Handles display of results"""
    # Dynamically know how to print top border.
    border_length = len(plain_text) + 14      # len("Plain text :  ")  = 14

    # Dynamically know where to display plain text and cipher text
    slot_1 = f"Plain text :  {plain_text}"
    slot_2 = f"Ciphertext :  {cipher_text}"

    if job == "decryption":
        # Change slot
        slot   = slot_1
        slot_1 = slot_2
        slot_2 = slot


    # Display the text result to the user  
    print(f"\n{'>' * border_length}          \
            \n{slot_1}                       \
            \nShift text :  {shift}          \
            \n{slot_2}\n                     \
    ")

def quote(plain_text):
    """Handles display of quotes and lower border of results"""
    # Get a Julius Caesar quote
    quote = cq.quote()
    
    # Dynamically know how to print bottom border.
    quote_length = len(quote)      + 16      # len(" ― Julius Caesar") = 16
    plain_length = len(plain_text) + 14      # len("Plain text :  ")  = 14
    if quote_length > plain_length:
        border_length = quote_length
    else:
        border_length = plain_length 
        
    # Display the quote and bottom border to the user  
    print(f"{quote} ― Julius Caesar        \
            \n{'>' * border_length}        \
    ")
    

def outro(user):
    """Displays outro message if wants to exit the program."""
    if user == "3":         
        good_bye = "👋 Good bye"
        print(f"\n{good_bye}")
        return "break" 
    
    
        