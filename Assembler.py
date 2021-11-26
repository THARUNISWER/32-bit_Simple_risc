# write only one instruction per line
# no semicolon after instruction
# label names start with .
# cant debug errors


#s = input("Enter your file path:")
file = open("instructions.txt","r")
h = []
for line in file:
    if(line.isspace()!=True):
        h.append((line.lstrip(" ").rstrip("\n").rstrip(":").lstrip("\t")))

def two_complement(val):
    val2 = "1"
    for c in val:
        if c == "0":
            val2 += "1"
        else:
            val2 += "0"
    val2 = format(int(val2,2)+1,"b")
    return val2
def appendf(inst,num):
    while(len(inst)<num):
        inst = "0" + inst
    return inst
def appendf2(inst,num):
    while(len(inst)<num):
        inst = "1" + inst
    return inst
def appendb(inst,num):
    while (len(inst) < num):
        inst = inst + "0"
    return inst
def find(rest):
    g = 0
    i = 0
    while(h[i]!=rest):
        i = i+1
        if(h[i].startswith(".")!=True and h[i].startswith("#")!=True):
            g = g+1
    return g

binary = ""
opcodes = {"add":"00000","sub":"00001","mul":"00010","div":"00011","mod":"00100","cmp":"00101","and":"00110","or":"00111","not":"01000","mov":"01001","lsl":"01010","lsr":"01011","asr":"01100","nop":"01101","ld":"01110","st":"01111","beq":"10000","bgt":"10001","b":"10010","call":"10011","ret":"10100"}
registers = {"r0":"0000","r1":"0001","r2":"0010","r3":"0011","r4":"0100","r5":"0101","r6":"0110","r7":"0111","r8":"1000","r9":"1001","r10":"1010","r11":"1011","r12":"1100","r13":"1101","r14":"1110","r15":"1111","sp":"1110"}
j = 0
while(j!=len(h)):
    s = h[j]
    parts = s.split(sep = " ")
    op = parts[0];
    if op[0]!="." and op[0]!="\\" and op[0] != "\\*" and op[0]!="#":
        if op[-1]=="u":
            m = "01"
            op = op[:-1]
        elif op[-1] == "h":
            m = "10"
            op = op[:-1]
        else:
            m = "00"
        opcode = opcodes[op];
        if op != "nop" and op != "ret":
            rest = parts[1];
    if(op == "add" or op == "sub" or op == "mul" or op == "div" or op == "mod" or op == "and" or op == "or" or op == "lsl" or op == "lsr" or op == "asr"):  #checked
        rest_parts = rest.split(sep = ",")
        rd = registers[rest_parts[0]]
        rs1 = registers[rest_parts[1]]
        if(rest_parts[2][0]=="r"):
            i = "0"
            rs2 = registers[rest_parts[2]]
            rs2 = rs2 + "00000000000000"
        else:
            i = "1"
            if(int(rest_parts[2])>=0):
                rs2 =  format(int(rest_parts[2]),"b")
                rs2 = m + appendf(rs2,16)
            else:
                binary = format(-int(rest_parts[2]), "b")
                flip_str = two_complement(binary)
                rs2 = m + appendf2(flip_str, 16)
        inst = opcode + i + rd + rs1 + rs2
        print(appendf(format(int(inst,2),"x"),8))
    elif(op == "cmp"):  #checked
        rest_parts = rest.split(sep=",")
        rd = "0000" #anything
        rs1 = registers[rest_parts[0]]
        if (rest_parts[1][0] == "r"):
            i = "0"
            rs2 = registers[rest_parts[1]]
            rs2 = rs2 + "00000000000000"
        else:
            i = "1"
            if (int(rest_parts[1]) >= 0):
                rs2 = format(int(rest_parts[1]), "b")
                rs2 = m + appendf(rs2, 16)
            else:
                binary = format(-int(rest_parts[1]),"b")
                flip_str = two_complement(binary)
                rs2 = m + appendf2(flip_str, 16)
        inst = opcode + i + rd + rs1 + rs2
        print(appendf(format(int(inst, 2), "x"),8))
    elif(op == "mov" or op == "not"):   #checked
        rest_parts = rest.split(sep=",")
        rs1 = "0000"  # anything
        rd = registers[rest_parts[0]]
        if (rest_parts[1][0] == "r"):
            i = "0"
            rs2 = registers[rest_parts[1]]
            rs2 = rs2 + "00000000000000"
        else:
            i = "1"
            if (int(rest_parts[1]) >= 0):
                rs2 = format(int(rest_parts[1]), "b")
                rs2 = m + appendf(rs2, 16)
            else:
                binary = format(-int(rest_parts[1]), "b")
                flip_str = two_complement(binary)
                rs2 = m + appendf2(flip_str, 16)
        inst = opcode + i + rd + rs1 + rs2
        print(appendf(format(int(inst, 2), "x"),8))
    elif(op == "beq" or op == "bgt" or op == "b" or op == "call"): #checked
        g = find(rest)
        k = find(h[j])
        #print(g-k+1)
        #print(g-j+1)
        if((g-k+1)>=0):
            offset = str(format((g - k+1),"b"))
            offset = appendf(offset,27)
        else:
            binary = format(-int((g-k+1)), "b")
            flip_str = two_complement(binary)
            offset = appendf2(flip_str, 27)
        inst = opcode + offset
        print(appendf(format(int(inst,2),"x"),8))
    elif(op == "ld" or op == "st"): #checked
        i = "1"
        rest_parts = rest.split(sep=",")
        rd = registers[rest_parts[0]]
        rst = rest_parts[1].split(sep = "[")
        rst1 = rst[1].split(sep = "]")
        rs1 = registers[rst1[0]]
        if(int(rst[0])>=0):
            rs2 = format(int(rst[0]), "b")
            rs2 = m + appendf(rs2,16)
        else:
            rs2 = format(-int(rst[0]), "b")
            flip_str = two_complement(rs2)
            rs2 = m + appendf2(flip_str, 16)
        inst = opcode + i + rd + rs1 + rs2
        print(appendf(format(int(inst, 2), "x"),8))
    elif(op == "ret" or op == "nop"):   #checked
        inst = appendb(opcode,32)
        print(appendf(format(int(inst, 2), "x"),8))
    j= j+1
print(90000000)
