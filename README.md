## Linux `cp` command using `python`

### Installation

```python
pip install -e . -U
```

### Exclusivities

* **Copy single file**
* **Copy directories**
* **Verbose support**
* **Mullti file support**
* **multi directory support**

### Usage:

```bash
cpy <fiel1> <fiel2>  ... [-v | --vervose]

cpy -r <directory1> <directory2>  ... [-v | --vervose]

cpy -r <directory1> <directory2> <file1> <file2>  ... [-v | --vervose]
```


### cpy -h

```bash
usage: cp [-h] [-r] [-v] [N [N ...]]

positional arguments:
  N    source path

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  copy directories recursively
  -v, --verbose    explain what is being done
```

