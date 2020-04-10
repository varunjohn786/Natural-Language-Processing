Title - Substituition Cipher Decoder

What is a Substituition Cipher - 
A substitution cipher is a method of encrypting by which units of plaintext are replaced with ciphertext, according to a fixed system. The "units" may be single letters (the most common and the one used in the code), pairs of letters, triplets of letters, mixtures of the above, and so forth. The receiver deciphers the text by performing the inverse substitution. Substitution ciphers can be compared with transposition ciphers.

What is a Substituition Cipher Decoder -
A substitution cipher decoder decodes a cipher text to some meaningful text.

Logic used in Code -
Code for the decoder uses Markov Model as base to decode the cipher text. According to Markov Model probability of occurence of a letter at nth position of a word depends on letters which came before it in the word like letters a n-1th position, n-2th position.
Using the same logic code calculates probability of all letters in form of unigrams, bigrams and trigrams using a training dataset and then use this probability to decode a completely new dataset.

List Of codes -
Code repositry consists of 2 codes namely Encoder and Decoder. Encoder helps in creating an substitution cipher after taking input from user what text should be encoded. 
Decoder code also takes in input from user. This input should be an encoded string (substitution cipher) which needs to be decoded.

Drawback -
For the code to be accurate and encoded message having more than 6 lines should be use. As the code wont be able to create an accurate word map with small encoded text.