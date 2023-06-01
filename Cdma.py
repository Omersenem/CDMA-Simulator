import numpy as np
import math
import random

#Constantes

Walsh = np.array([[1,  1,  1,  1,  1,  1,  1,  1],
    [1, -1,  1, -1,  1, -1,  1, -1],
    [1,  1, -1, -1,  1,  1, -1, -1],
    [1, -1, -1,  1,  1, -1, -1,  1],
    [1,  1,  1,  1, -1, -1, -1, -1],
    [1, -1,  1, -1, -1,  1, -1,  1],
    [1,  1, -1, -1, -1, -1,  1,  1],
    [1, -1, -1,  1, -1,  1,  1, -1]])

Walsh_16=np.array([[1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1],
   [1,  -1,   1,  -1,   1,  -1,   1,  -1,   1,  -1,   1,  -1,   1,  -1,   1,  -1],
   [1,   1,  -1,  -1,   1,   1,  -1,  -1,   1,   1,  -1,  -1,   1,   1,  -1,  -1],
   [1,  -1,  -1,   1,   1,  -1,  -1,   1,   1,  -1,  -1,   1,   1,  -1,  -1,   1],
   [1,   1,   1,   1,  -1,  -1,  -1,  -1,   1,   1,   1,   1,  -1,  -1,  -1,  -1],
   [1,  -1,   1,  -1,  -1,   1,  -1,   1,   1,  -1,   1,  -1,  -1,   1,  -1,   1],
   [1,   1,  -1,  -1,  -1,  -1,   1,   1,   1,   1,  -1,  -1,  -1,  -1,   1,   1],
   [1,  -1,  -1,   1,  -1,   1,   1,  -1,   1,  -1,  -1,   1,  -1,   1,   1,  -1],
   [1,   1,   1,   1,   1,   1,   1,   1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1],
   [1,  -1,   1,  -1,   1,  -1,   1,  -1,  -1,   1,  -1,   1,  -1,   1,  -1,   1],
   [1,   1,  -1,  -1,   1,   1,  -1,  -1,  -1,  -1,   1,   1,  -1,  -1,   1,   1],
   [1,  -1,  -1,   1,   1,  -1,  -1,   1,  -1,   1,   1,  -1,  -1,   1,   1,  -1],
   [1,   1,   1,   1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,   1,   1,   1,   1],
   [1,  -1,   1,  -1,  -1,   1,  -1,   1,  -1,   1,  -1,   1,   1,  -1,   1,  -1],
   [1,   1,  -1,  -1,  -1,  -1,   1,   1,  -1,  -1,   1,   1,   1,   1,  -1,  -1],
   [1,  -1 , -1,   1,  -1,   1,   1,  -1,  -1,   1,   1,  -1,   1,  -1,  -1,   1]])

Key_1=Walsh[1]
Key_2=Walsh[2]

Key_16_1=Walsh_16[1]
Key_16_2=Walsh_16[2]

#------------------------------------------------------------------------------#

def Message_Spreader(message,size):
    #Etale le message sur longeur message * longueur code de Walsh
    Spreaded = []
    for i in range (len(message)):
        for j in range (0,size):
            Spreaded.append(message[i])
    return Spreaded

def Message_Encoder (Spreaded , key):
    #fait un XOR entre le message etale et le code de Walsh de l'utilisateur
    Encoded = []
    for i in range (len(Spreaded)):
       result = xor(Spreaded[i] , key[i% len(key)])
       Encoded.append(result)
    return Encoded

def xor (a,b):
    #Redefinition de l'operation xor en tenant compte des "-1"
    if a == 0 or b == 0:
        return 0
    elif (a == b):
        return -1
    return 1

def Volt_Encoder(Encoded):
    #Permet de faire le mapping entre une valeur binaire et une plage de volt
    Volt_Encoded = []
    for i in range (len(Encoded)):
        volt = random.uniform(0.05,1)#(0.5,1.5)
        if Encoded[i]==1:
            volt = -volt
        Volt_Encoded.append(volt)
    return Volt_Encoded
        

def Noise_Generator(size, niveau_bruit):
    #Genere un bruit aleatoire de la meme longueur que le message
    Noise = []
    for i in range (0,size):
        Noise.append(niveau_bruit*random.uniform(-1,1))
    return Noise

def Multiplexing (User_1 , Noise):
    Traffic = []
    Traffic = AddVector(User_1,Noise)
    return Traffic



def BER (Input , Output):
    #Calcule le Bit Error Rate
    error = 0
    for i in range (0,len(Output)):
        if Input[i] != Output[i]:
            error  += 1
    return error

#--------------------------------------------------------------------------------------#

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    #Convertit un texte en train binaire
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    #Convertit un train binaire en texte
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def binaire_to_ternaire(binaire):
    #Convertit un train binaire en train ternaire (-1,0,1)
    temp  = [int(x) for x in  list(binaire)]
    Ternaire = [-1 if x==0 else 1 for x in temp]    
    return Ternaire


def ternaire_to_binaire (ternaire):
    #Convertit un train ternaire en train binaire
    temp = pop_zeros(ternaire)
    temp1 = [0 if x==-1 else x for x in temp] 
    temp2 = [str(i) for i in temp1]
    ternaire = ''
    ternaire = ternaire.join(temp2)
    return ternaire

#__________________________________________________________________________________________________#


def User_sending (txt,key):    
    return Volt_Encoder(Message_Encoder(Message_Spreader(binaire_to_ternaire(text_to_bits(txt)),len(key)),key))

def Back_to_text(received):
    temp1 = [0 if x==-1 else 1 for x in received]
    temp2 = [str(i) for i in temp1]
    ternaire = ''
    ternaire = ternaire.join(temp2)
    return(text_from_bits(ternaire))

def Decoder_1(Traffic,key):
    Decoded = []
    Received = []
    for i in range(0, len(Traffic), len(key)):
        temp= Traffic[i:i + len(key)]
        result = np.inner(temp,key)
        Decoded.append(result/len(key))  
    for x in range (len(Decoded)):
            if (Decoded[x]>0):
                i=1
            elif (Decoded[x]<0):
                i=-1
            else :
                i=random.randint(-1,1)
            Received.append(i)
  
    return Received

def AddVector(a, b):
    added = []
    for i in range(min(len(a), len(b))):
        added.append(a[i]+b[i])
    if (len(a) > len(b)):
        added = added + a[i+1:]        
    elif (len(b) > len(a)):
        added=added + b[i+1:]       
    return added


