class Mixin:
    
    def prep_pauli(self, bit, base):
        if base == 1: 
            if bit == 0 : q = self.H(self.PREP())
            elif bit == 1 : q = self.H(self.X(self.PREP()))
        elif base == 2: 
            if bit == 0 : q = self.PREP()
            elif bit == 1 : q = self.X(self.PREP())
        elif base == 3: 
            if bit == 0 : q = self.K(self.PREP())
            elif bit == 1 : q = self.K(self.X(self.PREP()))
        else: raise NameError("Cannot prepare this state")
        return q

    def prep_ghz(self, nb_target_nodes):
        def add_one_qubit(q):
            _, r = self.CNOT(q, self.PREP())
            return r

        q = self.H(self.PREP())

        return [q] + [add_one_qubit(q) for _ in range(nb_target_nodes)]
