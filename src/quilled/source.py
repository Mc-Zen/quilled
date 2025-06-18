from qiskit.circuit import Bit, QuantumCircuit


def get_name(bit: Bit):
    name = bit._register.name
    if len(name) > 1:
        name = "\"" + name + "\""
    return name + "_" + str(bit._index)


def gate_to_quill(gate, qc: QuantumCircuit, bundle=False):
    nq = qc.num_qubits

    name = gate.name
    qubits = [qubit._index for qubit in gate.qubits]
    clbits = [clbit._index for clbit in gate.clbits]
    arg_str = ", ".join([str(qubit) for qubit in qubits])

    if name == "barrier":
        if qubits == [0, nq - 1]:
            arg_str = ""
        else:
            arg_str = f"start: {qubits[0]}, end: {qubits[1]}"
    if name == "measure":
        if bundle:
            creg = gate.clbits[0]._register
            arg_str += f", {qc.cregs.index(creg) + nq}, label: [{clbits[0]}]"
        else:
            arg_str += f", {clbits[0] + nq}"

    if name == "ecr":
        name = "mqgate"
        qubits = sorted(qubits)
        arg_str = f"{qubits[0]}, n: {qubits[1] - qubits[0] + 1}, [ECR]"
    if name in ("rx", "ry", "rz"):
        p = gate.operation.params[0]
        pifycation = piyfy(p)
        if pifycation is not None:
            enum, denom = pifycation
            if enum == 1: enum = ""
            else: enum = str(enum)

            if denom == 1: denom = ""
            p = enum + "π"
            if denom != "":
                p = f"({p})/{str(denom)}"
        arg_str = f"${p}$, " + arg_str
    return f"{name}({arg_str})"


def piyfy(x):
    pi = 3.14159265358979323
    frac = x / pi * 8
    if abs(frac - round(frac)) > 1e-9:
        return None
    frac = round(frac)
    denom = 8
    if frac % 2 == 0:
        denom = 4
        frac //= 2
    if frac % 2 == 0:
        denom = 2
        frac //= 2
    if frac % 2 == 0:
        denom = 1
        frac //= 2
    

    return (frac, denom)


def preamble():
    return """
    #set page(width: auto, height: auto, margin: 2pt)
    #import "@local/quill:0.7.1": *
    #import tequila: *
    """


def attach_bit_labels(qc: QuantumCircuit, bundle=False):
    result = ""
    for index, qubit in enumerate(qc.qubits):
        result += f"  lstick(${get_name(qubit)}$, x: 0, y: {index}),\n"
    if bundle:
        for index, creg in enumerate(qc.cregs):
            result += f"  lstick($\"{creg.name}\"$, x: 0, y: {index + len(qc.qubits)}),\n"
    else:
        for index, clbit in enumerate(qc.clbits):
            result += f"  lstick(${get_name(clbit)}$, x: 0, y: {index + len(qc.qubits)}),\n"
    return result


def attach_bundle_labels(qc: QuantumCircuit):
    result = ""
    for index, creg in enumerate(qc.cregs):
        result += f"  nwire([{creg.size}], x: 1, y: {index + len(qc.qubits)}),\n"
    return result


def source(qc: QuantumCircuit, labels=True, bundle=True) -> str:
    """Generate Typst source code to draw a Quill quantum circuit.

    Parameters
    ----------
    qc : QuantumCircuit
        The quantum circuit to draw. 
    labels : bool, optional
        Whether to display bit labels at the beginning of wires, by default True
    bundle : bool, optional
        Whether to bundle classical wires, by default True

    Returns
    -------
    str
        The generated Typst source code. 
    """
    nq = qc.num_qubits
    ncl = len(qc.cregs) if bundle else qc.num_clbits
    result = ""

    result += preamble()
    result += "#quantum-circuit(\n"
    result += f"  wires: (1,) * {nq} + (2,) * {ncl},\n"
    result += "  ..tequila.build(\n"

    for gate in qc:
        result += f"    {gate_to_quill(gate, qc, bundle=bundle)},\n"

    result += "  ),\n"

    if labels:
        result += attach_bit_labels(qc, bundle=bundle)
    if bundle:
        result += attach_bundle_labels(qc)
    result += ")\n"
    return result
