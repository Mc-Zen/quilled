import unittest
from src.quilled import *
from src.quilled.source import piyfy
from qiskit.circuit import QuantumCircuit, ClassicalRegister, QuantumRegister


class TestData(unittest.TestCase):

    def test_source(self):
                
        qregs = [QuantumRegister(4, "q"), QuantumRegister(2, "p")]
        cregs = [ClassicalRegister(2, "a"), ClassicalRegister(3, "b")]
        qc = QuantumCircuit(*qregs, *cregs)

        qc.h([0,1])
        qc.cx(1, [0,3])
        qc.measure((1, 0, 2), cregs[1])
        qc.measure((3, 2), cregs[0])
        # qc.measure_all()
        qc.barrier(0, 1)
        qc.h(range(4))
        qc.rx(3.14159265358, 0)
        print(source(qc))
        # qprint(qc)
        # display(qc.draw("mpl"))
    
    def test_piyfy(self):
        pi = 3.14159265358979323
        self.assertEqual(piyfy(1), None)
        self.assertEqual(piyfy(pi*3/8), (3, 8))
        self.assertEqual(piyfy(pi*2), (2, 1))
        self.assertEqual(piyfy(pi*4), (4, 1))
        self.assertEqual(piyfy(pi*3), (3, 1))
        self.assertEqual(piyfy(pi*.5), (1, 2))
