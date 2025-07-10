import matplotlib.pyplot as plt
import numpy as np
import sympy as sy
from collections import defaultdict



alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ,.-'

def n_gram(data, n) -> dict:
    result = defaultdict(int)
    for i in range(0, len(data) - n + 1, n):  # Step `n` at a time
        key = ''.join(data[i:i + n])
        result[key] += 1
    return dict(result)



def cipher_distribution(file, number_one, number_di, number_tri):

    with open(file, 'r') as f:
        data = f.read().strip()
        onegram = {k:v for k, v in n_gram(data, 1).items() if v > number_one}
        digram = {k:v for k, v in n_gram(data, 2).items() if v > number_di}
        trigram = {k:v for k, v in n_gram(data, 3).items() if v > number_tri}

    return file, onegram, digram, trigram


def print_diagrams(file, onegram, digram, trigram) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # 1 row, 3 columns

    # Plot Onegram
    axes[0].bar(list(onegram.keys()), list(onegram.values()), color='blue')
    axes[0].set_title('Onegram')
    axes[0].set_xlabel('Keys')
    axes[0].set_ylabel('Values')

    # Plot Digram
    axes[1].bar(list(digram.keys()), list(digram.values()), color='green')
    axes[1].set_title('Digram')
    axes[1].set_xlabel('Keys')

    # Plot Trigram
    axes[2].bar(list(trigram.keys()), list(trigram.values()), color='red')
    axes[2].set_title('Trigram')
    axes[2].set_xlabel('Keys')

    fig.suptitle(file, fontsize = 16, fontweight = 'bold')

    plt.tight_layout()
    plt.show()


def caesar_cipher(file) -> tuple[str, int]: 
    jump = 6
    result = ''
    with open(file, 'r') as f:
        data = f.read()
    
    for character in data:
        index1 = alphabet.index(character)
        result += alphabet[(index1 - jump) % 29]
    
    return result, jump



def caesar_cipher2(data, jump) -> str:
    result = ''
    for character in data:
        index1 = alphabet.index(character)
        result += alphabet[(index1 - jump) % 29]
    return result


def length_texts(file) -> int:
    with open(file, 'r') as f:
        data = f.read().strip()
        return len(data)
    


def frequency_string(string, one, two, three) -> None:
    onegram = {k:v for k, v in n_gram(string, 1).items() if v > one}
    digram = {k:v for k, v in n_gram(string, 2).items() if v > two}
    trigram = {k:v for k, v in n_gram(string, 3).items() if v > three}

    axes = plt.subplots(1, 3, figsize=(15, 5))  # 1 row, 3 columns

    # Plot Onegram
    axes[0].bar(list(onegram.keys()), list(onegram.values()), color='blue')
    axes[0].set_title('Onegram')
    axes[0].set_xlabel('Keys')
    axes[0].set_ylabel('Values')

    # Plot Digram
    axes[1].bar(list(digram.keys()), list(digram.values()), color='green')
    axes[1].set_title('Digram')
    axes[1].set_xlabel('Keys')

    # Plot Trigram
    axes[2].bar(list(trigram.keys()), list(trigram.values()), color='red')
    axes[2].set_title('Trigram')
    axes[2].set_xlabel('Keys')

    plt.tight_layout()
    plt.show()



def vigenere(file) -> str:
    streams = [''] * 5
    jumps = [13, 19, 3, 9, 27]
    
    with open(file, 'r') as f:
        data = f.read().strip()
        for i in range(len(data)):
            streams[i % 5] += (data[i])

    """ for stream in streams:
        frequency_string(stream, 0, 1,1) """  #Her sjekket jeg frekvensen til alle bokstavene per stream, som resulterte i jumps-lista

    results = [caesar_cipher2(streams[i], jumps[i]) for i in range(len(streams))]

    string_results = [0] * len(data)

    for i in range(len(results)):
        for j in range(len(results[i])):
            string_results[(j * 5) + i] = results[i][j]

    return ''.join(string_results)


def hill_cipher_key(digram_one, digram_two) -> np.array:
    cipher_text = np.array([digram_one, digram_two])
    plain_text = np.array([[19,7], [7,4]]) 
    plain_text_sympy = sy.Matrix(plain_text)
    plain_text_inversed = np.array(plain_text_sympy.inv_mod(29))
    key = np.dot(cipher_text, plain_text_inversed) % 29
    
    return key

def hill_cipher_solve(key) -> str:
    result = ''
    key_sympy = sy.Matrix(key)
    key_inverse = np.array(key_sympy.inv_mod(29))
    with open('text_files/3.txt', 'r') as f:
        cipher = f.read().strip()

        for i in range(0, len(cipher) - 3, 4):
            char1 = alphabet.index(cipher[i])
            char2 = alphabet.index(cipher[i + 1])
            char3 = alphabet.index(cipher[i + 2])
            char4 = alphabet.index(cipher[i + 3])
            cipher_part = np.array([[char1, char3],[char2, char4]])
            plain_text = np.dot(key_inverse, cipher_part) % 29

            result += alphabet[plain_text[0][0]]
            result += alphabet[plain_text[1][0]]
            result += alphabet[plain_text[0][1]]
            result += alphabet[plain_text[1][1]]

    
    return result


        


def main():

    while True:
        answer = input('Want to see distributions (1), caesar (2), simple substitution (3), Vigenere (4), or Hill cipher (5), or quit (6) ? (1, 2, 3, 4, 5, 6) ')

        match answer:
            case '1':
                file, onegram, digram, trigram = cipher_distribution('text_files/0.txt', 0, 2, 1)
                print_diagrams(file, onegram, digram, trigram)
                file, onegram, digram, trigram = cipher_distribution('text_files/1.txt', 0, 5, 2)
                print_diagrams(file, onegram, digram, trigram)
                file, onegram, digram, trigram = cipher_distribution('text_files/2.txt', 0, 6, 2)
                print_diagrams(file, onegram, digram, trigram)
                file, onegram, digram, trigram = cipher_distribution('text_files/3.txt', 0, 5, 1)
                print_diagrams(file, onegram, digram, trigram)
            
            case '2':
                jump, result = caesar_cipher('text_files/2.txt')
                print(f'The following plaintext occurs when shifting the alphabet with {jump} letters\n')
                print(result) 
                cipher_distribution('text_files/2.txt', 0, 6, 2)
                print()
                

            case '3':
                print('Only caesar cipher and simple substitution cipher has defined some letters that occur at the same rate. The most common will map to E and T for example. When looking at the trigrams, on can see that "EHR" is the most used. E,H and R is also much used in monograms and digrams. "EHR" = "THE" and it is the first text that is theanswer.\n')
                cipher_distribution('text_files/1.txt', 0, 5, 2)
                print()

            case '4':
                result = vigenere('text_files/0.txt')
                print(f'Text 0 is the answer. The five streams are shifted with the key: LRBHZ, result in the following plaintext\n')
                print(result)
                print()

            case '5':
                #key_possibillities = [['G','Y'], ['E','Z'], ['E','F'], ['B', 'V'], ['U', 'B'], ['X', '-'], ['E', 'N']]
                file, onegram, digram, trigram = cipher_distribution('text_files/3.txt', 1, 9, 2)
                key_possibillities = list(digram)

                print(f'After doing a frequenzy analysis on the digrams of text 3, the following key digrams are a possible solution:\n')
                print(key_possibillities)
                print()
                print(f'After iterating through every possibility, one of the keys will lead to a plaintext\n')

                for element in key_possibillities:
                    for element2 in key_possibillities:
                        if element2 == element:
                            continue
                        key = hill_cipher_key([alphabet.index(element[0]), alphabet.index(element2[0])],[alphabet.index(element[1]), alphabet.index(element2[1])])
                        print(f'key = {key}')
                        print([alphabet.index(element[0]), alphabet.index(element2[0])],[alphabet.index(element[1]), alphabet.index(element2[1])])
                        
                        try:
                            print(hill_cipher_solve(key))
                        except:
                            continue

                print()
                print('AHA! I see the right one\n')
                right_key = hill_cipher_key([alphabet.index('X'), alphabet.index('G')], [alphabet.index('-'), alphabet.index('Y')])
                print(f'Right key = {right_key}\n')
                print(f'Plaintext:\n {hill_cipher_solve(right_key)}\n')

            case '6':
                break

            

    
main()





        

    





