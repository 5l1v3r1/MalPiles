import csv
import math
import pefile
import sys
import os

"""data here is list of lists"""

def csv_writer(path, data, family_name):
    with open(path, "ab+") as csv_file:
        writer = csv.writer(csv_file, delimiter = ',')
        for line in data:
        	line.append(family_name)
        	writer.writerow(line)

def get_entry_point_section(pe, eop_rva):
    for section in pe.sections:
        if section.contains_rva(eop_rva):
            return section

def get_all_sections_virtual_size(pe):
	total_virtual_size = 0
	for section in pe.sections:
		total_virtual_size += section.Misc_VirtualSize
	return total_virtual_size

def get_exports_count(pe):
	exports_count = 1
	if hasattr(pe, "DIRECTORY_ENTRY_EXPORT"):
		for export in pe.DIRECTORY_ENTRY_EXPORT.symbols:
		    exports_count += 1
	return exports_count

def is_ascii(value):
	if value >= 32 and value <= 126:
		return True
	else:
		return False

def get_longest_ascii_string(data):
	longest_ascii_string_len = 0
	longest_ascii_string_offset = None
	current_ascii_string_len = 0
	current_ascii_string_offset = None
	for value in enumerate(data):
		if is_ascii(value[1]) == True:
			current_ascii_string_len += 1
			if current_ascii_string_offset == None:
				current_ascii_string_offset = value[0]
			if current_ascii_string_len > longest_ascii_string_len:
				longest_ascii_string_len = current_ascii_string_len
				longest_ascii_string_offset = current_ascii_string_offset
		else:
			current_ascii_string_len = 0
			current_ascii_string_offset = None

	return data[longest_ascii_string_offset:longest_ascii_string_offset + longest_ascii_string_len]

def calculate_entropy(data):
	if not data:
		return 0
	entropy = 0
	data_len = len(data)
	for x in range(256):
		p_x = float(data.count(chr(x))) / data_len
		if p_x > 0:
			entropy += - p_x * math.log(p_x, 2)
	return entropy

def calculate_ascii_entropy(data):
	if not data:
		return 0
	entropy = 0
	data_len = len(data)

	for x in range(127):
		if chr(x) != ' ':
			p_x = float(data.count(chr(x))) / data_len
			if p_x > 0:
				entropy += - p_x * math.log(p_x, 2)
	return entropy

def parse_file(pe, filepath):
	entry_point = pe.OPTIONAL_HEADER.AddressOfEntryPoint

	code_section = get_entry_point_section(pe, entry_point)
	if not code_section:
		print "Invalid PE file, exiting"
		exit()

	"""	all_sections_virtual_size = get_all_sections_virtual_size(pe)
		code_section_percent = 1
		if all_sections_virtual_size > 0:
			code_section_percent = (float(code_section.Misc_VirtualSize) / float(all_sections_virtual_size)) * 100
		print "Code section percent of all sections virtual size %.2f" % code_section_percent
	"""
	"""	code_at_entry_point = bytearray(code_section.get_data(entry_point, 200))
		code_at_entry_point_entropy = calculate_entropy(code_at_entry_point)
		print "Code at entry point entropy %.2f" % code_at_entry_point_entropy
	"""
	code_section_data = bytearray(code_section.get_data())
	code_section_data_entropy = calculate_entropy(code_section_data)
	print "Code section entropy %.2f" % code_section_data_entropy

	with open(filepath, mode='rb') as file:
	    entire_pe_data = bytearray(file.read())

	entire_pe_data_entropy = calculate_entropy(entire_pe_data)
	print "Entire PE data entropy %.2f" % entire_pe_data_entropy

	overlay_data_entropy = 1

	overlay_offset = pe.get_overlay_data_start_offset()
	if overlay_offset != None:
		overlay_size = len(entire_pe_data[overlay_offset:])
		overlay_data_entropy = calculate_entropy(entire_pe_data[overlay_offset:])
	print "Overlay data entropy %.2f" % overlay_data_entropy

	longest_ascii_string = get_longest_ascii_string(entire_pe_data)
	longest_ascii_string_entropy = calculate_ascii_entropy(longest_ascii_string)
	print "Longest string entropy %.2f" % longest_ascii_string_entropy
	
	return [str(round(code_section_data_entropy, 2)), str(round(code_section_data_entropy, 2)),
			str(round(entire_pe_data_entropy, 2)), str(round(entire_pe_data_entropy, 2)),
			str(round(overlay_data_entropy, 2)), str(float(len(longest_ascii_string))),
			str(round(longest_ascii_string_entropy, 2))]


if len(sys.argv) < 3:
	print "python generate_dataset.py C:\\Samples dataset.csv"
	exit()

if os.path.isdir(sys.argv[1]) == False:
	print "%s is not directory." % sys.argv[1]
	exit()

all_families_data = {}

for filename in os.listdir(sys.argv[1]):
	try:
		filepath = sys.argv[1] + "\\" + filename
		pe = pefile.PE(filepath)
	except Exception as e:
		print "%s is not valid PE file" % filename
	else:
		family_data = parse_file(pe, filepath)
		family_name = filename.split(" ")[0]
		if all_families_data.has_key(family_name) == False:
			all_families_data[family_name] = []
		all_families_data[family_name].append(family_data)

try:
	os.remove(sys.argv[2])
except Exception:
	pass

for family_name in all_families_data:
	csv_writer(sys.argv[2], all_families_data[family_name], family_name)
