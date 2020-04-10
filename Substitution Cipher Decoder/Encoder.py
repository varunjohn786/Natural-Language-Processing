import string
from random import shuffle


#### Encoder Functin ####
def create_encoder(message):
    message = message.lower()
    alphabet1 = list(string.ascii_lowercase)
    alphabet2 = list(string.ascii_lowercase)
    encoded = ""
    shuffle(alphabet2)

    word_map ={}

    for k,i in zip(alphabet1,alphabet2):
        word_map[k]=i

    for words in message.split():
        for letter in words:
            if letter in word_map.keys():
                encoded += word_map[letter]
            else:
                encoded += letter
        encoded += " "

    print(encoded)


### Taking Input from User ###
encoder = input("Enter the statement which needs to be encoded- ")
create_encoder(encoder)