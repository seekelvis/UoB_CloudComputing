import hashlib

def hexstr2binstr(h):
    b = ""
    for x in h:
        if x == "0":
            b += "0000"
        elif x == "1":
            b += "0001"
        elif x == "2":
            b += "0010"
        elif x == "3":
            b += "0011"
        elif x == "4":
            b += "0100"
        elif x == "5":
            b += "0101"
        elif x == "6":
            b += "0110"
        elif x == "7":
            b += "0111"
        elif x == "8":
            b += "1000"
        elif x == "9":
            b += "1001"
        elif x == "a":
            b += "1010"
        elif x == "b":
            b += "1011"
        elif x == "c":
            b += "1100"
        elif x == "d":
            b += "1101"
        elif x == "e":
            b += "1110"
        elif x == "f":
            b += "1111"
    return b

# x = hashlib.sha256()
# y = hashlib.sha256()
found = 0
block = "COMSM0010cloud"
nonce = 65536
i = -1
for j in range (0,nonce,1):
    if found == 1 :
        break
    for k in range(0,nonce,1):
        i = i+1

        # print ("i=", i)

        x = hashlib.sha256()
        y = hashlib.sha256()
        code = block + str(i)
        # code = block+"0000000000"
        # print ("code= ",code)
        x.update(code.encode("utf-8"))
        temstr = x.hexdigest()
        # print("temstr= ",temstr)

        y.update(temstr.encode("utf-8"))
        result = y.hexdigest()
        bin_result = hexstr2binstr(result)

        # print("result= ", result)
        # print("bin_reslut = ", bin_result)
        # print("result[d] = ", result[0:2])
        if result[0:4] == "0000":
            found = 1
            break
nonce = i
# print >> "./out.txt", "nonce = ", nonce

# print("nonce = ", nonce,file=f)

f = open("./out.txt","w")
f.write("nonce = "+str(nonce))
f.close()
