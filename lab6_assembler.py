# Import modules
import string

# Dictionary containing the list of instructions
opcodes = {"mv" : "000", "mvi" : "001", "add" : "010", "sub" : "011", "ld" : "100", "st" : "101", "mvnz" : "110"}
registers = {"R0" : "000", "R1" : "001", "R2" : "010", "R3" : "011", "R4" : "100", "R5" : "101", "R6" : "110", "R7" : "111"}

# Converts the registers to their respective binary code
def convert_bin(reg_x, reg_y, instr):
	print "RegX = %s; RegY = %s; Instr = %s" % (reg_x, reg_y, instr)
	return opcodes.get(instr) + registers.get(reg_x) + registers.get(reg_y)
	

# Open the files
assembly_file = open("hex_instr.txt", "r")
binary_file = open("mif_hex_instr.mif", "w")

i = 0

# Add the top description information to the mif file
binary_file.write("DEPTH = 128;\n")
binary_file.write("WIDTH = 32;\n")
binary_file.write("ADDRESS_RADIX = HEX;\n")
binary_file.write("DATA_RADIX = BIN;\n")
binary_file.write("\nCONTENT\n")
binary_file.write("BEGIN\n\n")

# Read the first line of assembly code
firstline = assembly_file.readline()
comment_code = firstline.split("%")
a_instr = comment_code[0]
 
#a_instr = a_instr[:len(a_instr)-1]

b_instr = ""

# As long as there is code, continue to translate
while a_instr:
	print a_instr
	list_codes = a_instr.split ("	")
	print list_codes
	
	hex_i = hex(i)
	binary_file.write(hex_i[2:] + " : ")
	#binary_file.write(format(str(i), 'x') + " : ")
	
	# Check if instruction is mvi
	if(list_codes[0] == "mvi"):
		b_instr = convert_bin(list_codes[1], "R0", list_codes[0])
	else:
		b_instr = convert_bin(list_codes[1], list_codes[2], list_codes[0])

	#Pad binary instruction to 32 bits
	while 32 - len(b_instr) != 0:
		b_instr += "0"

	binary_file.write(b_instr + ";	-- " + firstline[:len(firstline)-1] + "\n")
	
	# Add the extra line for the immediate value
	if(list_codes[0] == "mvi"):
		i += 1

		imma = bin(int(list_codes[2]))
		imma = imma[2:]
		zeros = ""
		
		while len(imma) + len(zeros) != 32:
			zeros += "0"
	
		imma = zeros + imma
		print imma
		
		hex_i = hex(i)
		binary_file.write(hex_i[2:] + " : " + imma + ";\n")
		
	# Increment to the next line and read it
	i+= 1
	firstline = assembly_file.readline()
	comment_code = firstline.split("%")
	a_instr = comment_code[0]

"""blank_instr = ""
z = 1
while z != 32:
	blank_instr += "0"
	z += 1
	
while i != 128:
	i += 1
	hex_i = hex(i)
	binary_file.write(hex_i[2:] + " : " + blank_instr + ";\n")"""
	
binary_file.write("\nEND;")

#Close the files
assembly_file.close()
binary_file.close()