import os
import sys

#function convert number from Decimal to Binary. Ex: 3 -> "00000011"
def decimalToBinary(num):  
    binary_string = bin(num).replace("0b", "")  
    #if len of binary string < 8 --> fill '0' on the left to get full 8 bits
    while len(binary_string) != 8:
        binary_string = "0" + binary_string
    return binary_string

#function convert number from Binary to Decimal. Ex: `11` -> 3
def binaryToDecimal(binary_string):
    return int(binary_string,2) 

#function to calculate broadcask base on ip and submaks
def calcBroadcast(ip_binary_string, submask_bit_octet_string):
    '''
    Input: IP bit string (Ex: "10010110.10010110.10010110.00000010"), Submask bit string (Ex: " 11111111.11111111.11111111.10000000")
    Output: broadcast address (Ex: 150.150.150.127), broadcast bit address (Ex: "10010110.10010110.10010110.01111111")
    '''
    #Calculate broadcast address
    #1. invert all bit of submask
    inv_submask_string = ""
    for i in range(len(submask_bit_octet_string)):
        if submask_bit_octet_string[i] == "0": 
            inv_submask_string += "1"
        elif submask_bit_octet_string[i] == "1":
            inv_submask_string += "0"
        else:
            inv_submask_string += "."
    
    #2. method "OR" between invert submask with IP address (binary)
    broadcast_binary = ""
    for i in range(len(inv_submask_string)):
        if inv_submask_string[i] == ".":
            broadcast_binary += "."
        elif inv_submask_string[i] == "0" and ip_binary_string[i] == "0":
            broadcast_binary += "0"
        else:
            broadcast_binary += "1"

    #convert broadcast binary to decimal
    broadcast_string_list = []
    broadcast_split = broadcast_binary.split(".")

    for i in range(len(broadcast_split)):
        dec = binaryToDecimal(broadcast_split[i])
        broadcast_string_list.append(str(dec))
    broadcast_string = ".".join(broadcast_string_list)
    return broadcast_string, broadcast_binary

#Input IP address and check if IP valid
def inputIP():      #return IP and IP in binary string
    '''
    Input: IP string (Ex: 192.168.1.1)
    Output: ip (string, ex: 192.168.1.1), 
            ip_number_list (ex: [192,168,1,1])
            ip_bit_string  (ex: "11000000.10101000.00000001.00000001")
    Press C (or c) to exit program
    '''
    while True:
        ip = input("Input IP address (Press C to exit): ")
        if ip.lower() == "c":
            print("Exit program")
            sys.exit(0)
        #print("IP: {}".format(ip))
        #Split IP address
        ip_split = ip.split(".")
        
        #Check if IP include 4 octets
        if len(ip_split) != 4:
            print("Invalid IP, length of the list must be 4 octets. Try again")
            continue
        
        #check the IP address can not begin with "0"
        if ip_split[0] == "0":
            print("IP address can not begin with 0. Try again")
            continue

        #check the last octet IP address can not be 0
        if ip_split[-1] == "0":
            print("The last octet of IP address can not be 0. Try again")
            continue

        #convert IP string to list of int number
        ip_number_list = []     #list of number of IP octet
        ip_bit_list = []        #list of binary of IP octet
        isInvalid = False
        for i in range(len(ip_split)):
            try:
                ip_int = int(ip_split[i])
                #check if any octet greater than 255
                if ip_int>=255 or ip_int<0:
                    print("Octet can not be greater than 255 or smaller than 0")
                    isInvalid = True
                    continue
                ip_number_list.append(ip_int)
                binary = decimalToBinary(ip_int)        #convert octet number to binary (Ex: 2 -> "00000010")
                ip_bit_list.append(binary)
            except:
                isInvalid = True
                break
        if isInvalid:
            print("Invalid IP. Try again")
            continue

        #check if IP belong class D or E
        if ip_number_list[0]>=240:
            print("Invalid IP. IP can not in class E")
            continue
        elif ip_number_list[0]>=224:
            print("Invalid IP. IP can not in class D")
            continue
        #check if IP is loopback address (127.x.x.x.x)
        if ip_number_list[0]==127:
            print("Invalid IP. IP can not be loopback adress")
            continue

        break   #all above condition is valid --> get valid IP, exit loop
    
    ip_bit_string = ".".join(ip_bit_list)
    return ip, ip_number_list, ip_bit_string

#Input SUBMASK address and check if submask valid
def inputSubmask():
    '''
    Input Submask
    Output: submask (string, Ex: 255.255.255.0), 
            submask number list (ex: [255,255,255,0]), 
            submask binary string (Ex: "11111111.11111111.11111111.00000000")
    '''
    while True:
        submask = input("Input submask (Press C to exit): ")
        if submask.lower() == "c":
            print("Exit program")
            sys.exit(0)

        #check subnet mask 255.255.255.255 is not valid
        if submask == "255.255.255.255":
            print("Invalid submask. Submask 255.255.255.255 is not valid. Try again")
            continue

        #split submask
        submask_string_list = submask.split(".")
        #check if submask include 4 octets
        if len(submask_string_list) != 4:
            print("Invalid submask, length of the list must be 4 octets. Try again")
            continue

        #check if first octet must be 255
        if submask_string_list[0] != "255":
            print("Invalid submask. First octet must be 255")
            continue

        #convert submask string list to submask number list
        submask_number_list = []
        bit_octet_list = []   #list of bits octet for subnet. For ex: ['11111111', '11111111', '11111111','00000000']
        isInvalid = False
        for i in range(len(submask_string_list)):
            try:
                submask_int = int(submask_string_list[i])       #convert string to int
                #check if octet greater than 255
                if submask_int>255 or submask_int<0:
                    print("Octet can not be greater than 255 or smaller than 0")
                    isInvalid = True
                    continue
                submask_number_list.append(submask_int)
                
                #convert octet decimal to binary
                binary = decimalToBinary(submask_int)
                bit_octet_list.append(binary)
            except: #if can not convert string -> int mean the input is not valid number (for example character)
                isInvalid = True
                break
        if isInvalid == True:
            print("Invalid submask.")
            continue

        #check if valid mask (bits in octet)
        #join bit octet list
        submask_bit_octet_string = ".".join(bit_octet_list)
        #check if valit network/host bits (all binary 1 on the left --> no case "01" or "0.1")
        if "01" in submask_bit_octet_string or "0.1" in submask_bit_octet_string:
            print("Invalid subnet. All network bit must be in the left")
            continue

        break   #all submask checking condition valid --> get valid submask, exit loop
    return submask, submask_number_list, submask_bit_octet_string

       

if __name__ == "__main__":
    # STEP 1: input IP
    ip, ip_number_list, ip_binary_string = inputIP()

    #STEP 2: input subnet mask
    submask, submask_number_list, submask_bit_octet_string = inputSubmask()

    #count network bits (count how many bit 1 in subnetting string)
    network_bits = submask_bit_octet_string.count("1")
    #count host bits (count how many bit 0 in subnetting string)
    host_bits = submask_bit_octet_string.count("0")

    #STEP 4: Determine the number of valid host
    #calculate number of valid host
    no_valid_host = 2**host_bits - 2

    #STEP 5 : Determine the Wildcard mask
    wildcard_string_list = []     #wildcard mask in Decimal
    wildcard_bin_list = []     #wildcard mask in binary
    for i in range(4):
        sub = 255 - submask_number_list[i]  #subtract subnet mask
        wildcard_string_list.append(str(sub))
        wildcard_binary = decimalToBinary(sub)
        wildcard_bin_list.append(wildcard_binary)
    #convert wildcard mask to string
    wildcard_string = ".".join(wildcard_string_list)
    wildcard_bin_string = ".".join(wildcard_bin_list) 

    #STEP 6: Determine the network address
    #change last octet of IP address to 0 (192.168.1.1 --> 192.168.1.0)
    network_address_list = ip_number_list.copy()
    network_address_list[-1] = 0
    network_address_binary = ip_binary_string[:-8]      #get IP binary string except last 8 bit and change last 8 bits to "00000000"
    network_address_binary += "00000000"
    #convert network address to string
    network_address_string_list = list(map(str, network_address_list))
    network_address_string = ".".join(network_address_string_list)

    #calculate broadcast address
    broadcast_string, broadcast_binary = calcBroadcast(ip_binary_string, submask_bit_octet_string)

    #STEP 3: OUTPUT
    print("\n")
    print("IP address:        {}     {}".format(ip, ip_binary_string))
    print("Subnet Netmask:    {}     {}".format(submask, submask_bit_octet_string))
    print("Network address:   {}     {}".format(network_address_string, network_address_binary))
    print("Broadcast address: {}     {}".format(broadcast_string, broadcast_binary))
    print("Wildcard mask:     {}     {}".format(wildcard_string, wildcard_bin_string))
    print("Number of usable host: {}".format(no_valid_host))