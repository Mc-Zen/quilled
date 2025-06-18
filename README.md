
# Quilled



[![PyPI Package](https://img.shields.io/pypi/v/quilled)](https://pypi.org/project/quilled/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/Mc-Zen/quilled/blob/main/LICENSE)
[![Tests](https://github.com/Mc-Zen/quilled/actions/workflows/run-tests.yml/badge.svg)](https://github.com/Mc-Zen/quilled/actions/workflows/run-tests.yml)
---


Generate Quill quantum circuit diagrams from Qiskit circuits

## Python package

The python package features???. You can install it via
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
```


## License

This library is distributed under the MIT License.

If you want to support work like this, you can consider a one-time or monthly [sponsorship](https://github.com/sponsors/Mc-Zen). 