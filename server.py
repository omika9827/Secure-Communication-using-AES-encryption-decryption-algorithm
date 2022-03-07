import socket
"""Server Socket Created"""
s = socket.socket()
print("Socket Created")

s.bind(('localhost', 9999))

s.listen(3)
print('Waiting for connections')

while True:
    c, addr = s.accept()
    ciphertext = c.recv(4096).decode('utf-8')
    key = c.recv(4096).decode('utf-8')

    print("Connected with Omika Gari : Mtech CSE (20MCS022) ", addr)

    "S-Box"
    SBox = [0x9, 0x4, 0xa, 0xb, 0xd, 0x1, 0x8, 0x5, 0x6, 0x2, 0x0, 0x3, 0xc, 0xe, 0xf, 0x7]

    "Inverse S-Box"
    ISBox = [0xa, 0x5, 0x9, 0xb, 0x1, 0x7, 0x8, 0xf, 0x6, 0x0, 0x2, 0x3, 0xc, 0x4, 0xd, 0xe]

    w = [None] * 6
    "Used for key generation or expansion"


    def keyExp(key):

        "This function will swap each nibble and substitute it using SBox (More explanation is given in Readme file"

        def SubNib(b):
            return SBox[b >> 4] + (SBox[b & 0x0f] << 4)

        Round1, Round2 = 0b10000000, 0b00110000

        w[0] = (key & 0xff00) >> 8  # Result into first 8 bit of the key
        w[1] = key & 0x00ff  # Result into last 8 bit of the key
        w[2] = w[0] ^ Round1 ^ SubNib(w[1])
        w[3] = w[2] ^ w[1]
        w[4] = w[2] ^ Round2 ^ SubNib(w[3])
        w[5] = w[4] ^ w[3]
        print("Round Key K0:", bin(w[0] + w[1]))
        print("Round Key K1:", bin(w[2] + w[3]))
        print("Round Key K2:", bin(w[4] + w[5]))


    def int_to_state(n):
        "This function converts a 16 bits value into a 4-states"
        return [n >> 12, (n >> 4) & 0xf, (n >> 8) & 0xf, n & 0xf]


    def state_to_int(m):
        "This function converts a 16 bits value into a 4-states"
        return (m[0] << 12) + (m[2] << 8) + (m[1] << 4) + m[3]


    def SubsNibble(SBox, s):
        """Nibble substitution function"""
        return [SBox[e] for e in s]


    def ShiftRows(s):
        "Swap 2nd and 4th nibble"
        return [s[0], s[1], s[3], s[2]]


    def gfmult(p1, p2):
        "This function performs Galois multiplication"
        p = 0
        while p2:
            if p2 & 0b1:
                p ^= p1
            p1 <<= 1
            if p1 & 0b10000:
                p1 ^= 0b11
            p2 >>= 1
        return p & 0b1111


    def addKey(s1, s2):
        "Add key"
        return [i ^ j for i, j in zip(s1, s2)]


    def convert(lst):
        """Converts content of list into binary form"""
        new_lst = []
        for i in lst:
            new_lst.append(bin(i))
        return new_lst


    def decrypt(ctext):
        "Decrypt ciphertext block"

        def IMixCol(s):
            return [gfmult(9, s[0]) ^ gfmult(2, s[2]), gfmult(9, s[1]) ^ gfmult(2, s[3]),
                    gfmult(9, s[2]) ^ gfmult(2, s[0]), gfmult(9, s[3]) ^ gfmult(2, s[1])]

        s1 = int_to_state(((w[4] << 8) + w[5]) ^ ctext)
        print("After Pre-round transformation: ", convert(s1))
        s2 = ShiftRows(s1)
        print("After Round 1 InvShift rows: ", convert(s2))
        s3 = SubsNibble(ISBox, s2)
        print("After Round 1 InvSubstitute nibbles: ", convert(s3))
        s4 = addKey(int_to_state((w[2] << 8) + w[3]), s3)
        print("After Round 1 InvAdd round key: ", convert(s4))
        s5 = IMixCol(s4)
        print("After Round 1 InvMix columns: ", convert(s5))
        s6 = ShiftRows(s5)
        print("After Round 2 InvShift rows: ", convert(s6))
        s7 = SubsNibble(ISBox, s6)
        print("After Round 2 InvSubstitute nibbles: ", convert(s7))
        s8 = addKey(int_to_state((w[0] << 8) + w[1]), s7)
        print("After Round 2 Add round key: ", convert(s8))
        return state_to_int(s8)


    k = int(key,2)
    ct = int(ciphertext, 2)
    print("Cipher text: ", bin(ct))
    print("Cipher key:", bin(k))
    keyExp(k)
    plaintext = decrypt(ct)
    print("Plaintext:", bin(plaintext))
    #c.send(bytes('Welcome..', 'utf-8'))
    c.close()
