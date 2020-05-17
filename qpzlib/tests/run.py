import unittest
import random

from hypothesis import given, example, settings
from hypothesis.strategies import text
import hypothesis.strategies as st

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from qpzlib import qpzlib 

import prep, meas, pres

## tests using simulaqron backend on a single node
from cqc.pythonLib import CQCConnection
from mappings.simulaqron import mapping

if __name__ == "__main__": 

    with CQCConnection("Alice") as Alice:
        _ = qpzlib(mapping, Alice)

        @settings(deadline=None)
        @given(st.lists(st.tuples(st.integers(min_value=1, max_value=6), st.integers(min_value=0, max_value=3)), min_size=1, max_size=10))
        def test_pres_qotp(ck_b): pres.qotp(_, ck_b)

        @given(st.integers(min_value=0, max_value=1), st.integers(min_value=1, max_value=3))
        @settings(deadline=None)
        def test_prep_pauli(bit, base): prep.pauli(_, bit, base)

        @given(st.integers(min_value=0, max_value=1), st.integers(min_value=1, max_value=3))
        @settings(deadline=None)
        def test_meas_pauli(bit, base): meas.pauli(_, bit, base)
        
        @given(st.integers(min_value=1, max_value=3), st.integers(min_value=1, max_value=2))
        @settings(deadline=None)
        def test_prep_ghz(nb_target_nodes, basis): prep.ghz(_, nb_target_nodes, basis)

        print("Pauli Preparation Tests")
        test_prep_pauli()
        print("OK")

        print("Pauli Measurement Tests")
        test_meas_pauli()
        print("OK")
        
        print("Quantum OTP Tests")
        test_pres_qotp()
        print("OK")
        
        print("Local GHZ preparation")
        test_prep_ghz()
        print("OK")
