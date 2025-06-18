import unittest
from src.quilled import *
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
        print(source(qc))
        # qprint(qc)
        # display(qc.draw("mpl"))
        