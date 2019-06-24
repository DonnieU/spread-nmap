import sys

arg = "192.168.0.0/10"
# arg = "192.168.0.0/1"

tmp = arg.split('/')
# print(tmp[0].split('.'))
ip = tmp[0].split('.')
sm = int(tmp[1])
for i in range(len(ip)):
  ip[i] = int(ip[i]) 
print('ip: {}'.format(ip))
print('subnet mask: {}'.format(sm))
print('octet b in 8-bit binary: {}'.format(bin(ip[1])))
print('type bin(ip[1]): {}'.format(type(bin(ip[1]))))

a, b, c, d = ip # destructure IP into octets
print('octet b of ip: {}'.format(b))
print()

"""
Algo:
1. Check subnet mask (sm): sm < 24 and sm >= 1 (1 to work with CIDR)

2. Check value of each ip octet: ip[0:] >= 0 and ip[0:] <= 255

3. Figure out which subnet octets to work with. We're doing it this way
   to know how many bits per octet we're working with:
   # if sm >= 1 and sm <= 8:
   if (24 - sm) >= 16:
     # we're dealing with 1st octet 
     sm_a = (24 - sm) - 16 
     sm_b = 0 
     sm_c = 0 
   elif ((24 - sm) > 8) and ((24 - sm) < 16):
     # we're dealing w/ 2nd and 3rd octet
     sm_a = 8 
     sm_b = (24 - sm) - 8
     sm_c = 0
   else:
     # we're only dealing w/ 3rd octet
     sm_a = 8 
     sm_b = 8
     sm_c = 24 - sm

4. IP ^ 255.255.255.255 # XOR to flip bits
5. IP_OCTET | SM_OCTET # OR to find upper limit of network range
6. Set starting value
7. Iterate and spin-up nmap instance
8. increment
9. repeat 7 and 8 until upper limit is reached
"""

def num_check():
  for num in ip:
    if num < 0 or num > 255:
      return False
  return True

# 1)
if (sm < 1) or (sm >=24):
  print('sm check')
  sys.exit(0)

# 2)
if not num_check():
  print("not num_check!")
  sys.exit(0)

# 3)
# num of bits ON per octet
# ignore last octet as we're working with subnet mask range of 1-23 (for CIDR)
# for 1st octet # of bits range: 
if (24 - sm) >= 16:
  sm_a = (24 - sm) - 16 
  sm_b = 0
  sm_c = 0
# for 2nd octet...
elif (24 - sm) > 8:
  sm_b = (24 - sm) - 8
  sm_c = 0
# for 3rd octet...
else:
  sm_b = 0 # why is this set to 0?!??!
  sm_c = 24 - sm

print('sm_b before conversion: {}'.format(sm_b))

# the number here represents the number of bits needed,
# NOT an int to be converted to binary
def int_to_bits(num):
  # bits = []
  # for i in range(num):
  #  bits.append(str(1))

  # bits = ''.join(bits).zfill(8)
  # bits = list(bits)
  # bits.append('0b')
  # bits = reversed(bits)
  # bits = ''.join(bits)

  bits = 0 
  for i in range(num,0,-1):
    bits += 1 << i
  bits =  format(bits, '0<08b')
  print('num= {}, number of bits: {}'.format(num, bits))
  return bits

sm_b = int_to_bits(sm_b)

print('subnet octet b (sm_b): {}'.format(sm_b))
print('bin(int(sm_b,2): {}'.format(bin(int(sm_b, 2))))
print('b | int(sm_b, 2): {}'.format(b | int(sm_b, 2)))
