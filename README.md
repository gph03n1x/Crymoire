## Crymoire

This is merely a toy ! Do not use in commercial products .
It offers no kind of production encryption whatsoever

Crymoire is a cipher based on the vigenere encryption
in a more hardened version against statistical attacks.
Introduces noise and false characters in encrypted output
so that every letter will have the same chance of occuring
in the encrypted output and it wont be easy to find which letter
is substituting which because every letter will have the same
chance of occuring .


### Requirements

* Bokeh ( Used in letter visualization. Not essential though.)

### Examples

```python
from crymoire import Crymoire
from core.utils import generate_random_key

crymoire = Crymoire()
crymoire.setKey(generate_random_key())

message = "my message"
encrypted_message = crymoire.encrypt(message)
decrypted_message = crymoire.decrypt(encrypted_message)
```

### Downgrade to vigenere.

In order to downgrade this back to normal vigenere one way is to encrypt many times
the same message. For example lets say our secret message is "My secret message".
Each time you encrypt it the cipher will produce a different encrypted message:

```
N*!x2$\n2$"b*\nj\n*!"j0NNb2!b\n*"!$00x$Nj2jxb0"x
N\n$x2$N\n!"!**x\njj"\n0b0j2!b0x"N$x2*$b!*j2b0"N
N0xx2$0$2"0*\n\n\n\n!"j0*2b2!*b*"x$b!!$xjNjNbN"j
```

Looking carefully you can find the vigenere encrypted message and remove the noise
by finding the positions with the same letters. Example in position 0 each string has 'N'
so 'N' is part of the encrypted message, while in position 1 the letters are different in each string
and thus we can deduce that the character in position 1 is part of the noise.

```
Nx2$"*\n"02!"$$jb"
```

Now you can simply decrypt it like a normal vigenere encrypted message.

