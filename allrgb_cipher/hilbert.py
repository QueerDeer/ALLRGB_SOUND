class Hilbert:
    """Multi-dimensional Hilbert space-filling curve.
    """
    
    def __init__(self, n):
        """Create an n-dimensional Hilbert space-filling curve.
        """
        self.n = n
        self.mask = (1 << n) - 1

    def encode(self, index):
        """Convert index to coordinates of a point on the Hilbert curve.
        """
        
        # Compute base-n digits of index.
        digits = []
        while True:
            index, digit = divmod(index, self.mask + 1)
            digits.append(digit)
            if index == 0:
                break

        # Start with largest hypercube orientation that preserves
        # orientation of smaller order curves.
        vertex, edge = (0, -len(digits) % self.n)

        # Visit each base-n digit of index, most significant first.
        coords = [0] * self.n
        for digit in reversed(digits):

            # Compute position in current hypercube, distributing the n
            # bits across n coordinates.
            bits = self.subcube_encode(digit, vertex, edge)
            for bit in range(self.n):
                coords[bit] = (coords[bit] << 1) | (bits & 1)
                bits = bits >> 1

            # Compute orientation of next sub-cube.
            vertex, edge = self.rotate(digit, vertex, edge)
        return tuple(coords)

    def subcube_encode(self, index, vertex, edge):
        h = self.gray_encode(index)
        h = (h << (edge + 1)) | (h >> (self.n - edge - 1))
        return (h & self.mask) ^ vertex

    def rotate(self, index, vertex, edge):
        v = self.subcube_encode(max((index - 1) & ~1, 0), vertex, edge)
        w = self.subcube_encode(min((index + 1) | 1, self.mask), vertex, edge)
        return (v, self.log2(v ^ w))

    def gray_encode(self, index):
        return index ^ (index >> 1)

    def log2(self, x):
        y = 0
        while x > 1:
            x = x >> 1
            y = y + 1
        return y
