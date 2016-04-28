## Crymoire

Crymoire is a cipher based on the vigenere encryption
in a more hardened version against statistical attacks.
Introduces noise and false characters in encrypted output
so that every letter will have the same chance of occuring
in the encrypted output and it wont be easy to find which letter
is substituting which because every letter will have the same
chance of occuring .

This is merely a toy ! Do not use in commercial products .

### Requirements

* Bokeh ( Used in letter visualization. Not essential though.)

### Examples

```python
from crymoire import Crymoire
from core.utils import generate_random_key

crymoire = Crymoire()
crymoire.setKey(generate_random_key())
message = "my message"
enc_ = crymoire.encrypt(message)
dec_ = crymoire.decrypt(enc_)
```

### Broke it ?

Please show me how you achieved it. [Mail me](mailto:giannispapcod7@gmail.com)
