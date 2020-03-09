import unittest
import random
import functools
import time

from hypothesis import given, example, settings
from hypothesis.strategies import text
import hypothesis.strategies as st

from qpzlib import qpzlib

## tests using simulaqron backend on a single node
from cqc.pythonLib import CQCConnection
from mappings.simulaqron import mapping

def pres_qotp_t(ck_b):
    print('.', end='', flush=True) 
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
    q_b = [prep_classical(c) for c in c_b] # create a list of qubits according to the classical inputs
    qenc_b = _.pres_qotp(q_b, k_b) # encode
    qdec_b = _.pres_qotp(qenc_b, k_b) #decode
    meas_results = [meas_classical(q, c) for q, c in zip(qdec_b, c_b)] #measure the result given the classical input

    assert functools.reduce(lambda acc, cur: acc and (cur == 0), meas_results, True) # make sure the value is 0 on all measured qubits


def prep_pauli_t(bit, base):
    print('.', end='', flush=True) 
    q = _.prep_pauli(bit, base)
    if base == 1: m = _.MEAS(_.H(q))
    elif base == 2: m = _.MEAS(q)
    elif base == 3: m = _.MEAS(_.K(q))

    assert (m == bit)

def prep_ghz_t(nb_target_nodes, basis):
    print('.', end= '', flush=True)
    def meas(q, basis):
        if basis == 1: #X measurement
            return _.MEAS(_.H(q))
        elif basis == 2: #Z measurement
            return _.MEAS(q)

    ghz_state = _.prep_ghz(nb_target_nodes)
    meas_results = [meas(q, basis) for q in ghz_state]
    nb_parties = 1 + nb_target_nodes

    assert functools.reduce(lambda acc, cur: acc + cur, meas_results, 0) % (2 if basis == 1 else nb_parties) == 0
        
        
if __name__ == "__main__": 

    with CQCConnection("Alice") as Alice:
        _ = qpzlib(mapping, Alice)

        @settings(deadline=None)
        @given(st.lists(st.tuples(st.integers(min_value=1, max_value=6), st.integers(min_value=0, max_value=3)), min_size=1, max_size=10))
        def test_pres_qotp(ck_b): pres_qotp_t(ck_b)

        @given(st.integers(min_value=0, max_value=1), st.integers(min_value=1, max_value=3))
        @settings(deadline=None)
        def test_prep_pauli(bit, base): prep_pauli_t(bit, base)

        @given(st.integers(min_value=1, max_value=3), st.integers(min_value=1, max_value=2))
        @settings(deadline=None)
        def test_prep_ghz(nb_target_nodes, basis): prep_ghz_t(nb_target_nodes, basis)

        print("Pauli Preparation Tests")
        test_prep_pauli()
        print("OK")
        
        print("Quantum OTP Tests")
        test_pres_qotp()
        print("OK")
        
        print("Local GHZ preparation")
        test_prep_ghz()
        print("OK")
