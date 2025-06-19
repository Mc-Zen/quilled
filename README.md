
# Quilled



[![PyPI Package](https://img.shields.io/pypi/v/quilled)](https://pypi.org/project/quilled/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/Mc-Zen/quilled/blob/main/LICENSE)
[![Tests](https://github.com/Mc-Zen/quilled/actions/workflows/run-tests.yml/badge.svg)](https://github.com/Mc-Zen/quilled/actions/workflows/run-tests.yml)
---


This package generates Quill quantum circuit diagrams from Qiskit circuits. You can install it via
```
pip install quilled
```

After the installation, you can use the package as follows:
```py
import quilled
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)

qc.h([0, 1])
qc.cz(0, 1)
qc.t([0, 1])

source_string = quilled.source(qc)
```

Or in order to directly draw and display in a Jupyter Notebook. 
```py
from quilled import qprint

qprint(qc)
qprint(qc, labels=False)  # Do not show qubit labels at the beginning of each wire. 
qprint(qc, bundle=False)  # Do not combine classical registers into one bundle. 
qprint(qc, scale=0.8)     # Scales the entire diagram. 
qprint(qc, qubits=[0, 1]) # Only display subset of qubits
```


## License

This library is distributed under the MIT License.

If you want to support work like this, you can consider a one-time or monthly [sponsorship](https://github.com/sponsors/Mc-Zen). 