from qiskit.circuit import QuantumCircuit, QuantumRegister


def extract_subcircuit(
    qc: QuantumCircuit,
    qubits=[],
    strict=True
) -> QuantumCircuit:
    """Prunes a quantum circuit by extracting out a subcircuit on the specified qubits. 

    Parameters
    ----------
    qc : QuantumCircuit
        The original quantum circuit
    qubits : list, optional
        A list of qubits to keep from the original circuit, by default []
    strict : bool, optional
        Whether to fail when the subcircuit is connected to other qubits via
        multi-qubit operations, by default True

    Returns
    -------
    QuantumCircuit
        The subcircuit

    Raises
    ------
    ValueError
        When the subcircuit cannot be extracted due to gates that connect to non-
        selected qubits. 
    """
    qc_pruned = QuantumCircuit(QuantumRegister(len(qubits), "q"), *qc.cregs)
    qmap = {qubit: new_index for new_index, qubit in enumerate(qubits)}
    for gate in qc:
        qs = [qubit._index for qubit in gate.qubits]
        if all(map(lambda x: x in qubits, qs)):
            qc_pruned.append(gate.replace(qubits=[qmap[qubit] for qubit in qs]))
        elif strict and any(map(lambda x: x in qubits, qs)):
            raise ValueError("Cannot prune circuit because of some gates")
    return qc_pruned
