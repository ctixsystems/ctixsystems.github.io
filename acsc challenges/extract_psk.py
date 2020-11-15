# A utility function to extract data from a keepass memory dump to assist with recovering 
# preotected stream keys and protected values from keepass data structures.

import binascii

# KeePass header structure
kp_header = binascii.a2b_hex(b'03D9A29A67FB')

file = '6792.dmp'   # file containing the dumped keypass process (from volatility for example)
locations = []      # store location of candidate headers
last_location = 0   # track the last location (file offset) for when headers are detected
candidate_psks = [] # store the candidare psk for use later

# Process the file
with open(file, 'rb') as f:
    kp_db = f.read()

while True:
    result = kp_db.find(kp_header, last_location + len(kp_header))
    if result == -1:
        break
    if result != last_location:
        locations.append(result)
        last_location = result
    else:
        break

# The protected stream key is a 32 byte value located 141 bytes from the KeePass header
# print all candidate values

for crib in locations:
    candidate = kp_db[crib+141:crib+173]
    candidate_psks.append(candidate)
    print("Candidate protected stream key values")
    print(binascii.b2a_hex(candidate)
