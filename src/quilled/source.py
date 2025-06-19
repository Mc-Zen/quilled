from qiskit.circuit import Bit, QuantumCircuit, QuantumRegister
from .extract_subcircuit import extract_subcircuit
from .piyfy import piyfy

def get_name(bit: Bit, map=None):
    name = bit._register.name
    if len(name) > 1:
        name = "\"" + name + "\""
    index = bit._index
    if map is not None:
        index = map[bit._index]
    return name + "_" + str(index)


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
            qubits = sorted(qubits)
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
            if enum == 1:
                enum = ""
            else:
                enum = str(enum)

            if denom == 1:
                denom = ""
            p = enum + "π"
            if denom != "":
                p = f"({p})/{str(denom)}"
        arg_str = f"${p}$, " + arg_str
    return f"{name}({arg_str})"


def preamble():
    return """
    #set page(width: auto, height: auto, margin: 2pt)
    #import "@local/quill:0.7.1": *
    #import tequila: *
    """


def attach_bit_labels(qc: QuantumCircuit, bundle=False, qubits=None):
    if qubits is None:
        qubits = range(qc.qubits)
    result = ""
    for index, qubit in enumerate(qc.qubits):
        result += f"  lstick(${get_name(qubit, map=qubits)}$, x: 0, y: {index}),\n"
    if bundle:
        for index, creg in enumerate(qc.cregs):
            result += f"  lstick($\"{creg.name}\"$, x: 0, y: {index + len(qc.qubits)}),\n"
    else:
        for index, clbit in enumerate(qc.clbits):
            result += f"  lstick(${get_name(clbit, map=qubits)}$, x: 0, y: {index + len(qc.qubits)}),\n"
    return result


def attach_bundle_labels(qc: QuantumCircuit):
    result = ""
    for index, creg in enumerate(qc.cregs):
        result += f"  nwire([{creg.size}], x: 1, y: {index + len(qc.qubits)}),\n"
    return result


def source(
    qc: QuantumCircuit,
    labels=True,
    bundle=True,
    scale=1.,
    qubits=None,
    highlight=[]
) -> str:
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
    if qubits is not None:
        qc = extract_subcircuit(qc, qubits=qubits, strict=True)
    else:
        qubits = range(qc.qubits)

    nq = qc.num_qubits
    ncl = len(qc.cregs) if bundle else qc.num_clbits

    result = ""
    result += preamble()
    result += f"#scale({scale*100}%, reflow: true, quantum-circuit(\n"
    result += f"  wires: (1,) * {nq} + (2,) * {ncl},\n"
    result += "  ..tequila.build(\n"

    for gate in qc:
        result += f"    {gate_to_quill(gate, qc, bundle=bundle)},\n"

    result += "  ),\n"  # end tequila.build

    for highlighted_qubits, color in highlight:
        for qubit in highlighted_qubits:
            result += f"  gategroup(x: {0}, y: {qubit}, 1, 100, fill: {color}, stroke: none),\n"

    if labels:
        result += attach_bit_labels(qc, bundle=bundle, qubits=qubits)
    if bundle:
        result += attach_bundle_labels(qc)
    result += "))\n"
    return result
