class Prep:
    def __init__(self, _): 
        def pauli(bit, base):
            if base == 1: 
                if bit == 0 : q = _.H(_.PREP())
                elif bit == 1 : q = _.H(_.X(_.PREP()))
            elif base == 2: 
                if bit == 0 : q = _.PREP()
                elif bit == 1 : q = _.X(_.PREP())
            elif base == 3: 
                if bit == 0 : q = _.K(_.PREP())
                elif bit == 1 : q = _.K(_.X(_.PREP()))
            else: raise NameError("Cannot prepare this state")
            return q

        def ghz(nb_target_nodes):
            def add_one_qubit(q):
                __, r = _.CNOT(q, _.PREP())
                return r

            q = _.H(_.PREP())

            return [q] + [add_one_qubit(q) for _ in range(nb_target_nodes)]

        self.pauli = pauli
        self.ghz = ghz
