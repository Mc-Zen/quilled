from .source import source

import typst
from qiskit.circuit import QuantumCircuit


def qprint(qc: QuantumCircuit, labels=True, bundle=True, **kwargs):
    """Displays a quantum circuit with IPython

    Parameters
    ----------
    qc : QuantumCircuit
        The quantum circuit to draw. 
    labels : bool, optional
        Whether to display bit labels at the beginning of wires, by default True
    bundle : bool, optional
        Whether to bundle classical wires, by default True
    """
    from IPython.display import SVG, display

    quill_source = source(qc, labels=labels, bundle=bundle, **kwargs)
    
    svg_bytes = typst.compile(
        quill_source.encode(encoding="utf-8"),
        format="svg",
        root="."
    )
    display(SVG(svg_bytes))
