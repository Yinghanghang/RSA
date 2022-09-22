import math
import random


def is_prime(n):# check if a number is a prime
    if n == 2: return True
    if n % 2 == 0:
        return False
    for p in range(3, int(math.sqrt(n) + 1), 2):
        if n % p == 0:
            return False
    return True


def ran_prime():# randomly generate a prime number within a certain range
    num = 0
    while True:
        num = random.randint(1e13,1e14)
        if is_prime(num):
            break
    return num


def gcd(p,q): # find the gcd and coefficients of the linerar combination of the gcd
    if p == 0:
        return (q, 0, 1)
    else:
        g, s, t = gcd(q % p, p)
        return (g, t - (q // p) * s, s) # s * p + t * q = g

    
def key(): # generate a public key and a private key
    p = ran_prime()
    while True:
        q = ran_prime()
        if p != q:
            break
        
    print("Two prime numbers are: p =", p, ", q =",q)      
    n = p * q
    m = (p-1) * (q-1)
    # print("m is: ", m)
    
    while True:
        e = random.randint(1e3,1e4)
        g, s, t = gcd(e, m)
        if g == 1: break # e is relatively prime to m

    d = mod_inverse(e, m) # d is the positive inverse to e module m       
    return((e, n), (d, n),(p,q))


def mod_inverse(e, m): # Return a positive number d such that, (e * d) ≡ 1 (mod m)
    g, s, t = gcd(e, m)
    return s % m # get a positive inverse

def powers_finder(num, base):# decompose a number into a sum of powers of base and return the powers
    powers = [] 
    while num >= 1:
        index = int(math.floor(math.log(num,base)))
        num = num - (base ** index) 
        powers.append(index) 
    return powers

def mod_temp(c, n, k): # compute c^(2^i) % n for i = 1,2...k, and put the results in an array
    array = [c % n]
    for i in range(1, k+1):
        array.append(array[-1] * array[-1] % n)
    return array

def mod(d, base, c, n):  # use the modular arithmetic property to simplify the computation: c ** d % n 
    array1 = powers_finder(d, 2)
    high = array1[0] # get the highest power of base 2 for number d
    array2 = mod_temp(c, n, high)
    
    result = 1
    for i in array1:
        result = result * array2[i] # multiply the needed elements in array2
    return result % n 


def encrypt(publickey,msg): # encrypt a message using public key
    e,n = publickey    
    encrypted_msg = [(ord(char) ** e) % n for char in msg]
    # print(encrypted_msg)
    return encrypted_msg
    

def decrypt(privatekey,encrypted_msg): # decrypt a message using private key
    d,n = privatekey
    decrypted_msg = [chr(mod(d,2,c,n)) for c in encrypted_msg]
    # print(decrypted_msg)
    return ''.join(decrypted_msg)
    
msg = input("Please enter a message: ")
publickey,privatekey,prime = key()
e,n = publickey
d,n = privatekey
p,q = prime

print("The public key is: e =", e, ", n =",n)
print("The private key is: d =", d,", n =",n)
encrypted_msg = encrypt(publickey,msg)
print ("The encrypted message is: ", "".join(map(str,encrypted_msg)))
decrypted_msg = decrypt(privatekey,encrypted_msg)
print ("The decrypted message is: ", decrypted_msg)


