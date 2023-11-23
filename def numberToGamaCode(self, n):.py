def numberToGamaCode( n):
    binaryNumber = bin(n)[2:]
    ans = ""
    for _ in range (len(binaryNumber)):
        ans+="1"
    ans+="0"+binaryNumber[1:]
    return ans


print (numberToGamaCode(5))