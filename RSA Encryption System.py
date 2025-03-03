import random
import math

def generatePseudoPrime(n1, n2, k):
    #find a pseudo Prime number.
    p = random.randint(n1, n2)
    pseudo_prime = False 
    while not pseudo_prime:
        for i in range(k):
            j = random.randint(2, p)
            if pow(j, p-1, p) > 1:
                p = random.randint(n1, n2)
                break
        pseudo_prime = True
    return p

def testPrime(p):
    if p == 2:
        return True
    else:
        for b in range(2, math.floor(math.sqrt(p))):
            if math.gcd(p, b) > 1:
                return False
            else:
                continue
        return True
    
def genPrime(n1, n2, k):
    prime = False
    while not prime:
        p = generatePseudoPrime(n1,n2,k)
        prime = testPrime(p)
    return p

def extended_gcd(a,b):
    if b == 0:
        return (1, 0, a)
    (x, y, d) = extended_gcd(b, a%b)
    return y, x - a//b*y, d

def genPublicKey(phi):
    e = random.randint(2, phi)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi)
    return e

def genPrivateKey(e, phi):
    x = extended_gcd(e, phi)
    d_ = x[0] %  phi
    return d_

def printDisplay1():
     print("Please select your user type: ")
     print("    1. A public user")
     print("    2. The owner of the keys")
     print("    3. Exit\n")

def printPublicUserDisplay():
    print("As a public user, what would you like to do?")
    print("     1. Send an encrypted message ")
    print("     2. Authenticate a digital signature ")
    print("     3. Exit ")
    print(" ")

def printPrivateUserDisplay():

    print("As the owner of the keys, what would you like to do?")
    print("     1. Decrypt a received message")
    print("     2. Digitally sign a message")
    print("     3. Show the keys")
    print("     4. Generating a new set of the keys")
    print("     5. Exit")
    print("")

def encrypt(message, e, n):
    return pow(message, e, n)

def decrypt(message, d, n): 
    return pow(message, d, n)

def printEncryptedMessages(messages):
    i = 1
    for item in messages:
        print(i,". (Length = ",len(item),")")
        i += 1

def printSignatures(signatures):
    i = 1
    for item in signatures:
        print(i,".", item)
        i += 1

def main():
    print("Generating the Keys, this may take a moment.")
    #generate prime numbers between 1 billion and 10 billion
    p = genPrime(1000000000, 10000000000, 1000000)
    q = genPrime(1000000000, 10000000000, 1000000)
    
  
  

    #calculate n and phi
    n = p * q
    phi = (p - 1) * (q - 1)

    #generate the public key
    publicKey = genPublicKey(phi)

    #generate the private key
    privateKey = genPrivateKey(publicKey, phi)

    #print that the keys have been generated
    print("RSA keys have been generated.")

    #create a list for the encrypted messages and the signature
    messages = [] 
    signatures = []
    verifySig = []


    #start the user inputs
    exitAll = 0
    while exitAll != '3':
        #print the display
        printDisplay1()
        #get the input
        exitAll = input("Enter your choice: ")
        #action depending on the input
        if exitAll == '1':
            #if the user clicked 1, display the options
            exitPublicUser = 0
            while exitPublicUser != '3':
                printPublicUserDisplay()
                exitPublicUser = input("Enter your choice: ")

                if exitPublicUser == '1':
                    #if the user clicks 1, have them enter a message.
                    soonEncrypted = input("Enter a message: ")
                    encryptNum = []
                    #encrypt the message
                    for item in soonEncrypted:
                        char = ord(item)
                        encryptNum.append(encrypt(char, publicKey, n))
                    messages.append(encryptNum)
                    print("Message encrypted and sent.")

                elif exitPublicUser == '2':
                    #if the user enters 2, have them validate a signature
                    if len(signatures) == 0:
                        print("There are no signatures to authenticate.")
                    else:
                        #prints the signatures that can be verified
                        printSignatures(signatures)
                        pickSig = int(input("Enter your choice: "))
                        #if a number that is not an option is picked, then say it is not an option.
                        if (pickSig) > len(signatures) and pickSig > 0:
                            print("Not a valid option")
                        else:
                            #verifys the signature that the user picked
                            verify = ""
                            soonVerified = verifySig[pickSig-1]
                            for item in soonVerified:
                                y = pow(item, publicKey, n)
                                y = chr(y)
                                verify += y
                            if verify == signatures[pickSig-1]:
                                print("Signature is Valid.")
                            else:
                                print("Signiture is invalid")
                        
                elif exitPublicUser != '3':
                    #if there is an input that is not one of the options, have the user try again.
                    print("Invalid input, try again.")

        elif exitAll == '2':
            #private user selections
            exitPrivateUser = 0
            while exitPrivateUser != '5':
                #enter the choice for the private user menu
                printPrivateUserDisplay()
                exitPrivateUser = input("Enter your choice: ")

                if exitPrivateUser == '1':
                    #if private user enters 1, pick a message to decode
                    printEncryptedMessages(messages)
                    pickOne = int(input("Enter your choice: "))
                    if (pickOne) > len(messages) and pickOne > 0:
                        print("Not a valid option")
                    else:
                        #decode the message
                        word = ""
                        soonDecrypted = messages[pickOne-1]
                        for item in soonDecrypted:
                            x = decrypt(item, privateKey, n)
                            x = chr(x)
                            word += x
                        print(word)

                elif exitPrivateUser == '2':
                    #if private user picks 2, sign a message
                    soonSigned = input("Enter a message: ")
                    signedNum = []
                    for item in soonSigned:
                        char = ord(item)
                        signedNum.append(pow(char, privateKey, n))
                    verifySig.append(signedNum)
                    signatures.append(soonSigned)
                    print("Message signed and sent.")


                elif exitPrivateUser == '3':
                    #if picks 3, print the public and private key.
                    print("Public key: " + str(publicKey) + ", " + str(n))
                    print("Private key: " + str(privateKey) + ", " + str(n))


                elif exitPrivateUser == '4':
                    #if picks 4, generates a new public and private key between 1 billion and 10 billion
                    p = genPrime(1000000000, 10000000000, 1000000)
                    q = genPrime(1000000000, 10000000000, 1000000)
                    #calculate n and phi
                    n = p * q
                    phi = (p - 1) * (q - 1)
                    publicKey = genPublicKey(phi)
                    privateKey = genPrivateKey(publicKey, phi)
                    print("New keys have been generated!")

                elif exitPrivateUser != '5':
                    #if an number that is not an option is picked, have the user try again.
                    print("Invalid input, try again.")

        elif exitAll != '3':
            #if an number that is not an option is picked, have the user try again.
            print("Invalid input, try again.")

    #print a goodbye message
    print("Bye for Now!")
    
main()

    


