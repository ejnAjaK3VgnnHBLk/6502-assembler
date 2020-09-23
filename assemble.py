import sys, os, re

asLineN = 0

def write(filename, opArray):
    swagarray = bytearray(opArray)
    with open(filename, "wb") as file:
        file.write(swagarray)

def flRead(filename):
    lineArray = []
    with open(filename, "r") as fp:
        lines = fp.readlines()
        for line in lines:
            lineArray.append(line.strip())
    return lineArray

def leng(n):
    count = 0
    while(n>0):
        n=n//10
        count = count + 1
    return count

def numberOps(line):
    addrStr = re.sub("\(", "", re.search(".[0-9a-fA-F]{1,}", line).group())
    addr = 0x00
    if "$" in addrStr:
        addr = int(re.sub("\$", "", addrStr), base=16) # Hex
    elif "%" in addrStr:
        addr = int(re.sub("\%", "", addrStr), base=2) # Bin
    else:
        addr = int(addrStr, base=10) # Decimal
    return addr.to_bytes(2, 'little')

def ascessorLine(line):
    if "nop" in line:
        print("Line", asLineN,", is asking for a no operation instruction.")
        return [0xea]
    elif "jmp" in line:
        # Check for absolute (JMP $5597) vs indirect (JMP ($5597)) jump.
        # Absolute jump transferrs program execution to the specified address and
        # Indirect jump jumps to the locaiton contained in the specified jump.
        #
        # An indriect jump must never use a vector beginning on the last bye of a page!!
        if "(" in line and ")" in line:
            # Indirect jump
            print("Line", asLineN, ", is asking for an indirect jump.")
            toRet = [0x6C]
            numbers = numberOps(line)
            for number in numbers:
                toRet.append(number)
            return toRet
        elif "(" in line or ")" in line:
            print("Indirect jump on line ", asLineN, " requires two parenthesis!")
            sys.exit()
        elif "(" not in line and ")" not in line:
            # absolute jump
            print("Line ", asLineN, ", is asking for an absolute jump.")
            toRet = [0x4C]
            numbers = numberOps(line)
            for number in numbers:
                toRet.append(number)
            return toRet
        else: 
            # what
            print("What")
    return [0x00]



flin = sys.argv[1]

if not os.path.isfile(flin):
    print("File does not exist, exiting....")
    sys.exit()

lineArray = flRead(flin)

opArray = []

for swag in lineArray:
    poggers = ascessorLine(swag)
    for pog in poggers:
        opArray.append(pog)
    asLineN += 1

print("The contents of opArray:")
for amazing in opArray:
    print(hex(amazing))
