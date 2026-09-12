# P3 OpenFHE try (farm-a)

Host: `root@207.246.94.252` VPC `10.20.0.4` container `umbra-p3` (Python 3.11.16). Live `umbra-choreo` / `10.20.0.5` not touched. No `docker rm`.

`import openfhe` failed. Compile never started.

```
cmd: docker exec umbra-p3 python3 -c "import openfhe"
stderr:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/usr/local/lib/python3.11/site-packages/openfhe/__init__.py", line 1, in <module>
    from .openfhe import *
ModuleNotFoundError: No module named 'openfhe.openfhe'
```

```
cmd: docker exec umbra-p3 python3 -c "import openfhe; openfhe.CCParamsCKKSRNS(); openfhe.GenCryptoContext(...)"
stderr:
Traceback (most recent call last):
  File "<string>", line 5, in <module>
  File "/usr/local/lib/python3.11/site-packages/openfhe/__init__.py", line 1, in <module>
    from .openfhe import *
ModuleNotFoundError: No module named 'openfhe.openfhe'
import openfhe failed
cannot compile OpenFHE circuit
```

```
cmd: docker exec umbra-p3 pip install --no-cache-dir openfhe==1.5.1.0.22.4
stdout/stderr:
Requirement already satisfied: openfhe==1.5.1.0.22.4 in /usr/local/lib/python3.11/site-packages (1.5.1.0.22.4)
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
[notice] A new release of pip is available: 24.0 -> 26.2.1
[notice] To update, run: pip install --upgrade pip
```

Wheel layout: `openfhe.cpython-310-x86_64-linux-gnu.so` under site-packages (CPython 3.10 ABI) on a 3.11 interpreter. `pip show openfhe` Version `1.5.1.0.22.4`. Re-import after pip still fails with the same `openfhe.openfhe` error. No OpenFHE circuit on farm-a.
