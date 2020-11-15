import base64
from Crypto.Cipher import AES, Salsa20
import hashlib
import binascii

# known protected, clear value pair
# ProtectedValue="UhzPpRhmnGMtvRFOUrFYlRHfz7E="
# Unprotected value = "FfGEr3EZCGN7TOvBQKGw" 

KDB4_SALSA20_IV = bytes(bytearray.fromhex('e830094b97205d2a'))
# PSK = binascii.a2b_hex(b'959e8830f06ccac1c192772907fed66534a4709fc38f45b334b572297340bcca')

# The protected stream key can be extracted from the header of the KeePass process in memory
# The start of the KeePass process is identified by the hex string: 03D9A29A67FB
# The PSK is a 32 byte vale offset from the header by 141 (decimal)

PSK = binascii.a2b_hex(b'5BD2383F7C370A82C6E010A08179C6299FC12CED6489971C87FD1C2475039D8F')

protected_value = 'ufeb8Ki+SG2cXLZgOPpA0t0DD/Q='

def sha256(s):
    """Return SHA256 digest of the string `s`."""
    return bytes(hashlib.sha256(s).digest())

def xor(aa, bb):
    """Return a bytearray of a bytewise XOR of `aa` and `bb`."""
    return bytearray([a ^ b for a, b in zip(bytearray(aa), bytearray(bb))])

salsa_buffer = bytearray()
salsa = Salsa20.new(sha256(PSK), KDB4_SALSA20_IV)

tmp1 = base64.b64decode(protected_value)

new_salsa = salsa.encrypt(bytearray(64))
salsa_buffer.extend(new_salsa)

ptxt1_bytes = xor(tmp1,salsa_buffer[:len(tmp1)])

print(ptxt1_bytes.decode('utf-8'))
