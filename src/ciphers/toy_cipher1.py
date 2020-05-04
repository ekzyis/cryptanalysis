def s(n):
    """Implements the substitution box for the toy cipher 1 from C. Bender's about DCA."""
    _s = {
        0x0: 0b0110,
        0x1: 0b0100,
        0x2: 0b1100,
        0x3: 0b0101,
        0x4: 0b0000,
        0x5: 0b0111,
        0x6: 0b0010,
        0x7: 0b1110,
        0x8: 0b0001,
        0x9: 0b1111,
        0xA: 0b0011,
        0xB: 0b1101,
        0xC: 0b1000,
        0xD: 0b1010,
        0xE: 0b1001,
        0xF: 0b1011,
    }
    return _s[n]
