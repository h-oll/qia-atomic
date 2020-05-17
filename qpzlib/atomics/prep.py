class Prep:
    def __init__(self, _): 
        def pauli(bit, base):
            """bit in 0,1 -> base in 1=X,2=Z,3=Y -> qubit in basis = base with value = bit"""
            if base == 1: 
                if bit == 0 : q = _.H(_.PREP())
                elif bit == 1 : q = _.H(_.X(_.PREP()))
            elif base == 2: 
                if bit == 0 : q = _.PREP()
                elif bit == 1 : q = _.X(_.PREP())
            elif base == 3: 
                if bit == 0 : q = _.K(_.PREP())
                elif bit == 1 : q = _.K(_.X(_.PREP()))
            else: raise NameError(f"""Cannot prepare this state: basis must be 1=X, 2=Z or 3=Y. Currently:  {m}""")
            return q

        def ghz(nb_target_nodes):
            def add_one_qubit(q):
                __, r = _.CNOT(q, _.PREP())
                return r

            q = _.H(_.PREP())

            return [q] + [add_one_qubit(q) for _ in range(nb_target_nodes)]

        self.pauli = pauli
        self.ghz = ghz
