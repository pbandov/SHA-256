'''SHA-256 OPTIMIZED '''

import os, time

#Constants, strings and working variables:
K_64 = ("0x428a2f98", "0x71374491", "0xb5c0fbcf", "0xe9b5dba5", "0x3956c25b", "0x59f111f1",
        "0x923f82a4", "0xab1c5ed5", "0xd807aa98", "0x12835b01", "0x243185be", "0x550c7dc3",
        "0x72be5d74", "0x80deb1fe", "0x9bdc06a7", "0xc19bf174", "0xe49b69c1", "0xefbe4786",
        "0x0fc19dc6", "0x240ca1cc", "0x2de92c6f", "0x4a7484aa", "0x5cb0a9dc", "0x76f988da",
        "0x983e5152", "0xa831c66d", "0xb00327c8", "0xbf597fc7", "0xc6e00bf3", "0xd5a79147",
        "0x06ca6351", "0x14292967", "0x27b70a85", "0x2e1b2138", "0x4d2c6dfc", "0x53380d13",
        "0x650a7354", "0x766a0abb", "0x81c2c92e", "0x92722c85", "0xa2bfe8a1", "0xa81a664b",
        "0xc24b8b70", "0xc76c51a3", "0xd192e819", "0xd6990624", "0xf40e3585", "0x106aa070",
        "0x19a4c116", "0x1e376c08", "0x2748774c", "0x34b0bcb5", "0x391c0cb3", "0x4ed8aa4a",
        "0x5b9cca4f", "0x682e6ff3", "0x748f82ee", "0x78a5636f", "0x84c87814", "0x8cc70208",
        "0x90befffa", "0xa4506ceb", "0xbef9a3f7", "0xc67178f2")

init_hash = ("0x6a09e667", "0xbb67ae85", "0x3c6ef372", "0xa54ff53a", "0x510e527f",
             "0x9b05688c", "0x1f83d9ab", "0x5be0cd19")


#FUNCTIONS (4.1.2)

def SHR_1(x, n):
    shr_block = []
    for i in range(n):
        shr_block += '0'
    for i in range(len(x)-n):
        shr_block += x[i]
     #   print(shr_block[i], end="")
    return shr_block

def SHL_1(x, n):
    shl_block = []
    bit_size = len(x)
    for i in range(bit_size-n, bit_size):
        shl_block += x[i]
    for i in range(n, len(x)):
        shl_block += '0'
    return shl_block

def OR_1(shr_block, shl_block):
    or1_block = []
    i = 0
    shr_block = list(map(int, shr_block))
    shl_block = list(map(int, shl_block))
    while i < len(shr_block):
        or1_block += [shr_block[i] | shl_block[i]]
        i = i + 1
        if i >= len(shr_block):
            break
   # print("OR_1 FUNC: ", or1_block)
    return or1_block


#ROTR_1 returns INT list:

def ROTR_1(x, n):
    shr_block = SHR_1(x,n)
    shl_block = SHL_1(x,n)
    rotr_block = OR_1(shr_block, shl_block)
    #print("ROTR_1 FUNC: ", rotr_block)
    return rotr_block

#SUM_0(x) = ROTR2(x) XOR ROTR13(x) XOR ROTR22(x):

def SUM_0(x):
    sum0_block = []
    temp1 = []
    rotr_2 = ROTR_1(x, 2)
    rotr_13 = ROTR_1(x, 13)
    rotr_22 = ROTR_1(x, 22)
    i = j = 0
    
    while i < len(rotr_2):
        temp1 += [rotr_2[i] ^ rotr_13[i]]
        i = i+1
        if i >= len(rotr_2):
            break
    temp1 = list(map(int, temp1))
    rotr_22 = list(map(int, rotr_22))
    while j < len(rotr_13):
        sum0_block += [temp1[j] ^ rotr_22[j]]
        j = j+1
        if j >= len(rotr_13):
            break    
    #print("SUM_0 BLOCK: ", sum0_block)
    return sum0_block

#SUM_1(x) = ROTR6(x) XOR ROTR11(x) XOR ROTR25(x):

def SUM_1(x):
    sum1_block = []
    temp1 = []
    rotr_6 = ROTR_1(x, 6)
    rotr_11 = ROTR_1(x, 11)
    rotr_25 = ROTR_1(x, 25)
    i = j = 0
    
    while i < len(rotr_6):
        temp1 += [rotr_6[i] ^ rotr_11[i]]
        i = i+1
        if i >= len(rotr_6):
            break
    temp1 = list(map(int, temp1))
    rotr_25 = list(map(int, rotr_25))
    while j < len(rotr_11):
        sum1_block += [temp1[j] ^ rotr_25[j]]
        j = j+1
        if j >= len(rotr_11):
            break
    #print("SUM_1 BLOCK: ", sum1_block)
    return sum1_block

#SIGMA_0(x) = ROTR7(x) XOR ROTR18(x) XOR SHR3(x):

def SIGMA_0(x):
    sigma0_block = []
    temp1 = []
    rotr_7 = ROTR_1(x, 7)
    rotr_18 = ROTR_1(x, 18)
    shr_3 = SHR_1(x, 3)
    i = j = 0
    
    while i < len(rotr_7):
        temp1 += [rotr_7[i] ^ rotr_18[i]]
        i = i+1
        if i >= len(rotr_7):
            break
    temp1 = list(map(int, temp1))
    shr_3 = list(map(int, shr_3))
    while j < len(rotr_18):
        sigma0_block += [temp1[j] ^ shr_3[j]]
        j = j+1
        if j >= len(rotr_18):
            break        
    #print("SIGMA_0 BLOCK: ", sigma0_block)
    return sigma0_block

#SIGMA_1(x) = ROTR17(x) XOR ROTR19(x) XOR SHR10(x):

def SIGMA_1(x):
    sigma1_block = []
    temp1 = []
    rotr_17 = ROTR_1(x, 17)
    rotr_19 = ROTR_1(x, 19)
    shr_10 = SHR_1(x, 10)
    i = j = 0
    
    while i < len(rotr_17):
        temp1 += [rotr_17[i] ^ rotr_19[i]]
        i = i+1
        if i >= len(rotr_17):
            break
    temp1 = list(map(int, temp1))
    shr_10 = list(map(int, shr_10))
    while j < len(rotr_19):
        sigma1_block += [temp1[j] ^ shr_10[j]]
        j = j+1
        if j >= len(rotr_19):
            break     
    #print("SIGMA_0 BLOCK: ", sigma1_block)
    return sigma1_block


#Ch(x,y,z) = (e ^ f) XOR (~e ^ g):

def CH_1(e,f,g):
    e = list(map(int, e))
    f = list(map(int, f))
    g = list(map(int, g))
    ch_block = []
    temp1 = []
    temp2 = []
    temp3 = []
    i = i1 = i2 = i3 = 0
    while i < len(e):
        temp1 += [e[i] & f[i]]
        i = i + 1
        if i >= len(e):
            break
    while i1 < len(e):
        temp2 += [0 if e[i1] == 1 else 1]
        i1 = i1 + 1
        if i1 >= len(e):
            break
    while i2 < len(g):
        temp3 += [temp2[i2] & g[i2]]
        i2 = i2 + 1
        if i2 >= len(g):
            break
    while i3 < len(f):
        ch_block += [temp1[i3] ^ temp3[i3]]
        i3 = i3 + 1
        if i3 >= len(f):
            break
    ch_block = ''.join(map(str, ch_block))
   # print("CH final: \n", ch_block)
    return ch_block

#MAJ(a,b,c) = (a ^ b) XOR (a ^ c) XOR (b ^ c):

def MAJ_1(a,b,c):
    a = list(map(int, a))
    b = list(map(int, b))
    c = list(map(int, c))
    maj_block = []
    temp1 = []
    temp2 = []
    temp3 = []
    i = 0
    while i < len(a):
        temp1 += [a[i] & b[i]]
        i = i + 1
        if i >= len(a):
            i = 0
            break
    while i < len(b):
        temp2 += [a[i] & c[i]]
        i = i + 1
        if i >= len(b):
            i = 0
            break
    while i < len(c):
        temp3 += [b[i] & c[i]]
        i = i + 1
        if i >= len(c):
            i = 0
            break
    while i < len(a):
        maj_block += [temp1[i] ^ temp2[i] ^ temp3[i]]
        i = i + 1
        if i >= len(c):
            i = 0
            break
    maj_block = ''.join(map(str, maj_block))
    #print("MAJ final: \n", maj_block)

    return maj_block


#Var type conversions (not in use):

def dec_convert(schedule_sublists):
    for i in range(0, len(schedule_sublists)):
        for j in range(0, len(schedule_sublists[i][:])):
            dec_word += [int(schedule_sublists[i][j], 2)]
    return dec_word

def hex_convert(schedule_sublists):
    for i in range(0, len(schedule_sublists)):
        for j in range(0, len(schedule_sublists[i][:])):
            hex_word += [hex(int(schedule_sublists[i][j], 2))]
    return hex_word



    #PPREPROCESSING (5.1.1):

def preprocessing():

    #Input message conversion to binary:
    input_message = input("Enter a value to hash: ")
    input_message_in_ascii = ''.join(format(ord(i), '08b') for i in input_message)
    print("INPUT MESSAGE:  " + str(input_message_in_ascii))

    #Counting the number of bits:
    message_length = len(input_message_in_ascii)

    #Appending the bit "1":
    input_message_in_ascii+= "1"

    #Returning the final input value in ASCII/binary:

    return input_message_in_ascii, message_length



def message_padding(input_message_in_ascii, message_length):

    print("Zero padded message: {0}" .format(input_message_in_ascii))

    print("MESSAGE LENGTH: ", message_length)
    
    #Last pad size conversion to binary:
    
    last_pad_size = format(message_length, 'b')
    last_pad_zeroes = 64 - message_length
    last_padded_zeroes = ""
    for i in range(last_pad_zeroes):
        last_padded_zeroes += "0"
    print("Padding message length: {0}" .format(last_padded_zeroes))
    print("The size of the last padded message is: {0} bits!" .format(len(last_padded_zeroes)))
    append_remaining_zeroes = last_padded_zeroes
    last_padded_zeroes += last_pad_size
    print("Right padded message: {0}".format(last_padded_zeroes))

    temp_length = len(last_padded_zeroes)
    if temp_length <= 64:
        temp_length = 64 - temp_length
        for i in range(temp_length):
            append_remaining_zeroes += "0"
    append_remaining_zeroes += last_pad_size
    print("Zero padding + message length: {0}".format(append_remaining_zeroes))

    #Concetanate original padded message with the zero padded message size:
    input_message_in_ascii += append_remaining_zeroes
    print("PADDED MESSAGE: {0} \n".format(input_message_in_ascii))
    for i in range(len(input_message_in_ascii)):            #Matrix drama
        print(input_message_in_ascii[i], end="")
   # print("\n")
    print("\nMessage size is {0} bits!" .format(len(input_message_in_ascii)))
    print("\n")
    padded_message = input_message_in_ascii
    file_lst = padded_message

    return file_lst



#Message parsing (5.2.1):


def message_parsing(file_lst):
    parsed_list = [] 
    def split_batches(batch_size, batch_lst):
        for i in range(0, len(batch_lst), batch_size):
            yield file_lst[i:i + batch_size]

    for batch in split_batches(32, file_lst):
        #print(batch)
        parsed_list += [batch]
    print(parsed_list, "# of words:", len(parsed_list))

    return parsed_list


def modulus_zero_checker(input_message_in_ascii, modulus_remainder):
    
    zero_block = "0"
    print("MOD = ", modulus_remainder)
    if modulus_remainder > 0 and modulus_remainder < 448:
        zero_length = 448 - modulus_remainder
        for i in range(zero_length):
            input_message_in_ascii += "0"
        print("MOD > 0 < 512 bits")
        #message_padding(input_message_in_ascii, modulus_remainder)
    elif modulus_remainder == 0:
        zero_length = 448 - len(input_message_in_ascii)
        for i in range(zero_length):
            input_message_in_ascii += "0"
        print("MOD = 0")
    elif modulus_remainder > 448 and modulus_remainder < 512:
        zero_length = 512 - modulus_remainder
        for i in range(zero_length):
            input_message_in_ascii += "0"
        print("MOD > 448 bits")
        print("Extended input message with zeroes: ", input_message_in_ascii)
        for i in range(447):
            zero_block += "0"
        input_message_in_ascii += zero_block
        #message_padding(input_message_in_ascii, modulus_remainder)

    print("MODULUS ZERO CHECKER after function call: ", input_message_in_ascii, "and mod div: ", modulus_remainder)

    return input_message_in_ascii, modulus_remainder



def mod_and_block_count(input_message_in_ascii, message_length):

    #Checking the message length for modulus 448mod512:
    modulus_remainder = 0
    message_length = len(input_message_in_ascii)
    
    #Checking and counting the number of blocks:
    if message_length > 448:
        print("Message size is: {0} bits - over 1 block!".format(message_length))
        number_of_blocks = divmod(message_length, 512)
        print("Number of blocks in a message: {0}" .format(number_of_blocks[0]+1))
        print("Modulus remainder: {0}" .format(number_of_blocks[1]))
        block_count = number_of_blocks[0] + 1
        modulus_remainder = number_of_blocks[1]
        if number_of_blocks[1] <= 448:
            print("Modulus under 448 - eligable for padding!")            
            
            input_message_in_ascii, modulus_remainder = \
                                    modulus_zero_checker(input_message_in_ascii, modulus_remainder)

            
        elif number_of_blocks[1] > 448:
            print("Modulus over 448!")   
            
            input_message_in_ascii, modulus_remainder = \
                                    modulus_zero_checker(input_message_in_ascii, modulus_remainder)
            
    elif message_length <= 448 and message_length > 0:
        print("Message size is: {0} bits - within 1 block!".format(message_length))
        modulus_remainder = 448 - len(input_message_in_ascii)
        print("Under 448, diff is: ", modulus_remainder)
        for i in range(modulus_remainder):
            input_message_in_ascii += "0"
            
        #message_padding(input_message_in_ascii, modulus_remainder)
    else:
        print("Message size is: {0} bits - within 1 block!".format(message_length))
        
        #message_padding(input_message_in_ascii, modulus_remainder)
    
    number_of_blocks = divmod(len(input_message_in_ascii), 512)
    block_count = number_of_blocks[0] + 1
    print("MOD AND BLOCK COUNT after function call: ", input_message_in_ascii)
    print("BLOCK COUNT: ", block_count)
    
    return input_message_in_ascii, block_count



def message_schedule(parsed_list):
    chunk_block = []
    schedule_array = []
    increment = 0
    schedule_number = int(len(parsed_list) / 16)
    print(schedule_number)
    
    for j in range(0, schedule_number):
        if increment < schedule_number:
            for i in range(0,48):
                chunk_block += ['00000000000000000000000000000000']
            if increment == 0:
                schedule_array += [parsed_list[0:16]]
                schedule_array += [chunk_block]
                print("INCR == 0, increment: ", increment)
            elif increment == 1:
                schedule_array += [parsed_list[16:32]]
                schedule_array += [chunk_block]
                print("INCR == 1, increment: ", increment)
            elif increment > 1:
                schedule_array += [parsed_list[increment * 16 : increment * 16 + 16]]
                schedule_array += [chunk_block]
                print("INCR > 1, increment: ", increment)
            chunk_block = []
            increment += 1
            print(schedule_array, len(schedule_array))
    # if increment >= 2:
       # schedule_array = schedule_array[:-2 or None]
       # print("\n Zero parsed list with Wt: \n:", schedule_array, len(schedule_array))
     #   completed_message = message_scheduler(parsed_schedule_array)
     #   return completed_message
    print("\n Zero parsed list with Wt FINAL: \n:", schedule_array, len(schedule_array))
   # message_scheduler(schedule_array)
   # completed_message = message_scheduler(schedule_array)

    return schedule_array

#6.2.2.:

def message_scheduler(parsed_list_final):
    schedule_block = []
    word_1 = parsed_list_final
    print("Passed schedule array from block_counter function: \n", word_1)
    for k in range(len(word_1[0][:])):
        print("k = ",k)
        if k == len(word_1):
            break
        for m in range(len(word_1[k][:])):
            schedule_block += [word_1[k][m]]
            print(m, schedule_block[m])
    word = schedule_block
    i = 16
    print(schedule_block)
  #  print("Schedule block before 16-64 loop: ",schedule_block)
    for i in range(16, 64):
        sigma_1 = SIGMA_1(list(word[i-2]))   #from ['0110'] to ['0','1','1','0'] SIGMA_1 takes, then  
        sigma_0 = SIGMA_0(list(word[i-15]))  #     returns [0,1,1,0]
        word_0 = list(word[i-7])             #from ['0110'] to ['0','1','1','0']
        word_1 = list(word[i-16])
        sigma_1 = ''.join(str(e)for e in sigma_1)  #from [0,1,1,0] to '0110' 
        sigma_0 = ''.join(str(e)for e in sigma_0)
        word_0 = ''.join(str(e)for e in word_0)    #from ['0','1','1','0'] to '0110'
        word_1 = ''.join(str(e)for e in word_1)
        hex_sum_0 = hex(int(sigma_1, 2) + int(word_0, 2))   #from '0110' to 0xff
        hex_sum_1 = hex(int(sigma_0, 2) + int(word_1, 2))
        hex_sum_0_mod = int(hex_sum_0, 16) % 2**32          #from 0xff to 656 (type:int)  
        hex_sum_1_mod = int(hex_sum_1, 16) % 2**32
        hex_final_sum = (hex_sum_0_mod + hex_sum_1_mod) % 2**32
        hex_final_mod = hex(hex_final_sum)                  #from 656 to 0xff
        bin_final = format(int(hex_final_mod, 16), "032b")  #from 0xff to '0110' (type:str) 
         
        schedule_block[i] = bin_final
    print("Schedule block: \n", schedule_block)
    
    return schedule_block


def block_counter(block_count, schedule_array):
    i = 0
    schedule_block = []
    while i < block_count:
        if i == 0:
            schedule_block += [message_scheduler(schedule_array[0:2])]
        elif i == 1:
            schedule_block += [message_scheduler(schedule_array[2:4])]
        elif i > 1:
            schedule_block += [message_scheduler(schedule_array[i*2:i*2+2])]
        i = i + 1
        print("i is: ", i)

    print("Block counter engine result: \n", schedule_block)
    return schedule_block

def initial_hashes(init_hash):
    h0 = format(int(init_hash[0], 16), "032b")
    h1 = format(int(init_hash[1], 16), "032b")
    h2 = format(int(init_hash[2], 16), "032b")
    h3 = format(int(init_hash[3], 16), "032b")
    h4 = format(int(init_hash[4], 16), "032b")
    h5 = format(int(init_hash[5], 16), "032b")
    h6 = format(int(init_hash[6], 16), "032b")
    h7 = format(int(init_hash[7], 16), "032b")
    return h0,h1,h2,h3,h4,h5,h6,h7


def engine(block_count, schedule_block, init_hash):
    count = 0
    h0,h1,h2,h3,h4,h5,h6,h7 = initial_hashes(init_hash)
    for i in range(block_count):                         #Last entry 23.01.2022.
       # count = count + 1       
        #a,b,c,d,e,f,g,h = working_variables(block_count, h0,h1,h2,h3,h4,h5,h6,h7, count, init_hash)
        print("h0 is: ", hex(int(h0, 2)))
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        print("a is: ", hex(int(a, 2)))
        
        a,b,c,d,e,f,g,h = compression(schedule_block[i], a,b,c,d,e,f,g,h, K_64)

        print("a is: ", hex(int(a,2)))
        
        h0,h1,h2,h3,h4,h5,h6,h7 = compute_hash(a,b,c,d,e,f,g,h, h0,h1,h2,h3,h4,h5,h6,h7)
        print("Var 'A' after hash compute: ", hex(int(a, 2)))
        print("H0 after hash compute (a+h0): ", hex(int(h0, 2)))
        
    print("Final hash values: ", h0,h1,h2,h3,h4,h5,h6,h7) 
    return h0,h1,h2,h3,h4,h5,h6,h7

def compute_hash(a,b,c,d,e,f,g,h, h0,h1,h2,h3,h4,h5,h6,h7):

    print("In compute hash, 'A' value before computation: \n", hex(int(a, 2)))
    print("In compute hash, 'H0'value before computation: \n", hex(int(h0, 2)))    
    
    h0 = hex(int(a, 2) + int(h0, 2))
    h0 = int(h0, 16) % 2**32
    h0 = hex(h0)
    h0 = format(int(h0, 16), "032b")
    
    h1 = hex(int(b, 2) + int(h1, 2))
    h1 = int(h1, 16) % 2**32
    h1 = hex(h1)
    h1 = format(int(h1, 16), "032b")
    
    h2 = hex(int(c, 2) + int(h2, 2))
    h2 = int(h2, 16) % 2**32
    h2 = hex(h2)
    h2 = format(int(h2, 16), "032b")

    h3 = hex(int(d, 2) + int(h3, 2))
    h3 = int(h3, 16) % 2**32
    h3 = hex(h3)
    h3 = format(int(h3, 16), "032b")

    h4 = hex(int(e, 2) + int(h4, 2))
    h4 = int(h4, 16) % 2**32
    h4 = hex(h4)
    h4 = format(int(h4, 16), "032b")

    h5 = hex(int(f, 2) + int(h5, 2))
    h5 = int(h5, 16) % 2**32
    h5 = hex(h5)
    h5 = format(int(h5, 16), "032b")

    h6 = hex(int(g, 2) + int(h6, 2))
    h6 = int(h6, 16) % 2**32
    h6 = hex(h6)
    h6 = format(int(h6, 16), "032b")

    h7 = hex(int(h, 2) + int(h7, 2))
    h7 = int(h7, 16) % 2**32
    h7 = hex(h7)
    h7 = format(int(h7, 16), "032b")

    print("In compute hash, values H0 after computation: \n", hex(int(h0, 2)))
    print("In compute hash, values 'A' after computation: \n", hex(int(a, 2)))
    
    return h0,h1,h2,h3,h4,h5,h6,h7

def hex_bin(a,b,c,d,e,f,g,h):
    #print("HEX BIN FUNC: \n", a,b,c,d,e,f,g,h)
    if len(a) < 32 or len(a) > 32:
        a = format(int(a, 16), "032b")
        b = format(int(b, 16), "032b")
        c = format(int(c, 16), "032b")
        d = format(int(d, 16), "032b")
        e = format(int(e, 16), "032b")
        f = format(int(f, 16), "032b")
        g = format(int(g, 16), "032b")
        h = format(int(h, 16), "032b")
    print("HEX BIN FUNC TRIGGERED!")
    return a,b,c,d,e,f,g,h


def compression(comp_message,a,b,c,d,e,f,g,h, K_64):
    i = 0
    TEMP_1 = 0                             #last entry 18.01.2022.
    TEMP_2 = 0             
    sum1 = sum2 = sum3 = 0
    a,b,c,d,e,f,g,h = hex_bin(a,b,c,d,e,f,g,h)
    for i in range(64):
        
        K64 = format(int(K_64[i], 16), "032b")
        K_word = comp_message[i]
        SUM1 = SUM_1(e)                                     
        CH1 = CH_1(e,f,g)
        SUM1 = ''.join(str(e)for e in SUM1)
        CH1 = ''.join(str(e)for e in CH1)   
        sum1 = hex(int(h,2) + int(SUM1,2))             #sum1 = h + SUM_1(e)
        sum1_mod = int(sum1, 16) % 2**32               #sum1 = h + SUM_1(e) FINAL (modulo)
        sum2 = hex(int(CH1, 2) + int(K64, 2))          #sum2 = CH_1(e,f,g) + K64
        sum2_mod = int(sum2, 16) % 2**32               #sum2 = CH_1(e,f,g) + K64 FINAL (modulo)
        sum_1_2_mod = (sum1_mod + sum2_mod) % 2**32    #sum_1_2_mod = sum1_mod + sum2_mod in hex -> in DEC(int)

        #print("K_word is: ", K_word)
        
        K_word = hex(int(K_word, 2))
        sum_1_2_mod = hex(sum_1_2_mod)
        sum_1_2_mod = format(int(sum_1_2_mod, 16), "032b")
        K_word = format(int(K_word, 16), "032b")
        
        sum3 = hex(int(sum_1_2_mod, 2) + int(K_word, 2))
        sum3_mod = int(sum3, 16) % 2**32
        sum3_hex = hex(sum3_mod)
        bin_final = format(int(sum3_hex, 16), "032b")
        TEMP_1 = bin_final

        #print("T1: ", TEMP_1)
        
        SUM0 = SUM_0(a)
        SUM0 = ''.join(map(str, SUM0))
        MAJ1 = MAJ_1(a,b,c)
        sum1 = hex(int(SUM0, 2) + int(MAJ1, 2))
        sum1_mod = int(sum1, 16) % 2**32
        sum1_mod = hex(sum1_mod)
        bin_final = format(int(sum1_mod, 16), "032b")
        TEMP_2 = bin_final
        #print("T2: ", TEMP_2)

        h = g
        g = f
        f = e

        sum_e = hex(int(d, 2) + int(TEMP_1, 2))
        sum_e = int(sum_e, 16) % 2**32
        sum_e = hex(sum_e)
        e = format(int(sum_e, 16), "032b")

        d = c
        c = b
        b = a
        
        sum_a = hex(int(TEMP_1, 2) + int(TEMP_2, 2))
        sum_a = int(sum_a, 16) % 2**32
        sum_a = hex(sum_a)
        a = format(int(sum_a, 16), "032b")

        hex_printer(a,b,c,d,e,f,g,h)
        #print("h = ",h, "\ng = ",g,"\nf = ",f,"\ne = ",e,"\nd = ",d,"\nc = ",c,"\nb = ",b,"\na = ",a)
    print("h = ",h, "\ng = ",g,"\nf = ",f,"\ne = ",e,"\nd = ",d,"\nc = ",c,"\nb = ",b,"\na = ",a)
    return a,b,c,d,e,f,g,h


def hex_printer(a,b,c,d,e,f,g,h):
    print(hex(int(a,2))[2:], end=" ")
    print(hex(int(b,2))[2:], end=" ")
    print(hex(int(c,2))[2:], end=" ")
    print(hex(int(d,2))[2:], end=" ")
    print(hex(int(e,2))[2:], end=" ")
    print(hex(int(f,2))[2:], end=" ")
    print(hex(int(g,2))[2:], end=" ")
    print(hex(int(h,2))[2:], end=" ")
    print("\n")

def final_SHA256(h0,h1,h2,h3,h4,h5,h6,h7):
    h0 = hex(int(h0, 2))[2:]
    h1 = hex(int(h1, 2))[2:]
    h2 = hex(int(h2, 2))[2:]
    h3 = hex(int(h3, 2))[2:]
    h4 = hex(int(h4, 2))[2:]
    h5 = hex(int(h5, 2))[2:]
    h6 = hex(int(h6, 2))[2:]
    h7 = hex(int(h7, 2))[2:]

    print("Final hash: ", h0,h1,h2,h3,h4,h5,h6,h7)

    final_hash256 = h0 + h1 + h2 + h3 + h4 + h5 + h6 +h7

    print("Final hash: ", final_hash256)
    
    return final_hash256


while 1:

    #Main program:
        #Step 1: Input the ascii message:
    in_message, message_length = preprocessing()
        #Step 2: Count the message and block size, append remainder with zeroes:
    in_message, block_count = mod_and_block_count(in_message, message_length)
        #Step 3: Pad the message with the remaining zeroes:
    file_lst = message_padding(in_message, message_length)
        #Step 4: Parse the whole message into 32bit listed words:
    parsed_list = message_parsing(file_lst)
        #Step 5: Prepare the message schedule:
    schedule_array = message_schedule(parsed_list)
    
    for i in range(len(schedule_array)):
        print("Number of words in the {0} index: {1}" \
              .format(i, len(schedule_array[i][:])))
        
        #Step 6: Compute the message schedule (wt):
    schedule_block = block_counter(block_count, schedule_array)
        #Step 7: Compress the message schedule:
    h0,h1,h2,h3,h4,h5,h6,h7 = engine(block_count, schedule_block, init_hash)
        #Step 8: Concatanate the final hash values:
    final_SHA256(h0,h1,h2,h3,h4,h5,h6,h7)
    
  

    #Last code line:
    os.system("python main.py")
    print("Restarting...")
    time.sleep(0.2) # 200ms to CTR+C twice


    
