#Author: Ian Snyder

import re

#array to hold lines for processing
unprocessed_array = []

#creates the hack file
create_hack_file = open('RectL.hack', 'w')

#opens and reads the Add.asm
add_file = open('rect/RectL.asm', 'r')
#puts each line as a single element into an array
#skips empty lines 
for x in add_file:
    if x == "\n":
        continue
    unprocessed_array.append(x.strip())

#sanity check
print("-----UNPROCESSED ARRAY------")
print(unprocessed_array)

#pass 1 removes comments
processed_array = []
for x in unprocessed_array:
    if re.findall("^/", x) == []:
        processed_array.append(x)
   
#sanity check

print("-----PROCESSED ARRAY------")
print(processed_array)
for x in processed_array:
    print(x)   

#pass 2
tranlated_array = []
#process A-Instructions
def a_trans(trans_code):
    new_string = int(trans_code[1:])
    final_string = format(new_string, '016b')
    return final_string 
#process C-Instructions
#C-Instruction dictionaris
comp_instructions = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "M":   "1110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "!M":  "1110001",
    "-D":  "0001111",
    "-A":  "0110011", 
    "-M":  "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101"
}

dest_instructions = {
    "null": "000", 
    "M":    "001",   
    "D":    "010",   
    "MD":   "011",   
    "A":    "100",  
    "AM":   "101",  
    "AD":   "110",  
    "AMD":  "111"
}

jump_instructions = {
    "null": "000",
    "JGT":  "001",
    "JEQ":  "010",
    "JGE":  "011",
    "JLT":  "100",
    "JNE":  "101",
    "JLE":  "110",
    "JMP":  "111"
}

def c_trans(trans_code):
    op_code = "111"
    dest_code = "null"
    jump_code = "null"
    
    #split trans_code at = and ;
    code_list = re.split('(=|;)', trans_code)
    eq_idx = 0
    semi_idx = len(code_list)
    print("<<<LISTS>>>")
    print("CODE:", code_list)
    # dest logic
    if "=" in code_list:
        eq_idx = code_list.index("=")
        dest_list = code_list[:eq_idx]
        dest_code = dest_list[0]
        print("DEST:", dest_code)
    else:
        #cheaply resets index if no = found 
        eq_idx = -1
    # jump logic
    if ";" in code_list:
        semi_idx = code_list.index(";")
        jump_list = code_list[semi_idx+1:]
        jump_code = jump_list[0]
        print("JUMP:", jump_code)
    
    #comp logic
    comp_list = code_list[eq_idx+1:semi_idx]
    comp_code = comp_list[0]
    print("CMP:", comp_code)

    binary_code = op_code
    binary_code += comp_instructions[comp_code]
    binary_code += dest_instructions[dest_code]
    binary_code += jump_instructions[jump_code]

    print("BINARY:", binary_code)


    return binary_code
#loop through and translate
for x in processed_array:
    if re.findall("^@", x) != []:
        tranlated_array.append(a_trans(x))
    else:
        tranlated_array.append(c_trans(x))

#print translated array
print("-----TRANSLATED ARRAY------")
print(tranlated_array)
for x in tranlated_array:
    print(x)
    create_hack_file.write(x+"\n")

#write translated array to add.hack

#closes files
add_file.close()
create_hack_file.close()
