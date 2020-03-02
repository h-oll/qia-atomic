import unittest
import random
import functools

from hypothesis import given, example, settings
from hypothesis.strategies import text
import hypothesis.strategies as st


from qpzlib import qpzlib

## tests using simulaqron backend on a single node
from cqc.pythonLib import CQCConnection
from mappings.simulaqron import mapping

if __name__ == "__main__": 

    with CQCConnection("Alice") as Alice:
        _ = qpzlib(mapping, Alice)

        @settings(deadline=None)
        @given(st.lists(st.tuples(
            st.integers(min_value=1, max_value=6),
            st.integers(min_value=0, max_value=3))
                        , min_size=1, max_size=10))
        def test_qotp(ck_b):
            def prep_classical(c):
                if c == 1: q = _.PREP()
                elif c == 2: q = _.X(_.PREP())
                elif c == 3: q = _.H(_.PREP())
                elif c == 4: q = _.Z(_.H(_.PREP()))
                elif c == 5: q = _.K(_.PREP())
                elif c == 6: q = _.Z(_.K(_.PREP()))
                else: raise NameError("Cannot prepare this state")
                return q

            def meas_classical(q, c):
                if c == 1: m = _.MEAS(q)
                elif c == 2: m = _.MEAS(_.X(q))
                elif c == 3: m = _.MEAS(_.H(q))
                elif c == 4: m = _.MEAS(_.H(_.Z(q)))
                elif c == 5: m = _.MEAS(_.K(q))
                elif c == 6: m = _.MEAS(_.K(_.Z(q)))
                else: raise NameError("Cannot measure in this basis")
                return m

            c_b, k_b = zip(*ck_b) # create a list for classical input values, and a list with the encoding key
            print("qotp_test - classical preparation / encryption key pairs: ", ck_b)
            q_b = [prep_classical(c) for c in c_b] # create a list of qubits according to the classical inputs
            qenc_b = _.qotp(q_b, k_b) # encode
            qdec_b = _.qotp(qenc_b, k_b) #decode
            meas_results = [meas_classical(q, c) for q, c in zip(qdec_b, c_b)] #measure the result given the classical input

            assert functools.reduce(lambda acc, cur: acc and (cur == 0), meas_results, True) # make sure the value is 0 on all measured qubits


        test_qotp()
