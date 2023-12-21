# GirderPatchLoad

GirderPatchLoad is a Python library for patch load resistance prediction of unstiffened and stiffened plate girders.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install GirderPatchLoad
```

## Usage

```python
import GirderPatchLoad

from GirderPatchLoad import predict_load
load = predict_load(tw=5,a=1000,hw=700,fyw=392,tf=20,bf=225,fyf=355,Ss=200,bl=125,tst= 5,bst=60))
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author
Dai-Nhan Le. Email: ledainhan.huce@gmail.com


## License

[MIT](https://choosealicense.com/licenses/mit/)