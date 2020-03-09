class Mixin:
    def test_swap(self, conn, q1, q2):

        """
        launch the swap test
        params:
            conn: string, node to do the swap
            q1, q2: iterable of qubits

        """

        q=zip(q1,q2)
        q0 = self.PREP()
        self.H(q0)

        for q1,q2 in q:
            self.gate_CSWAP(q0, q1, q2)
            print(self.MEAS(q1), self.MEAS(q2))

        self.H(q0)
        m = self.MEAS(q0)

        print ('q0 measure is ', m)
        
        return m
