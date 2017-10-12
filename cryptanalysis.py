
import crymoire
import string
from core.utils import generate_random_key

f = open("secret.key", "r")
key = f.read()
#f = open("secret.key", "w")
#f.write(generate_random_key(size=1024, chars=string.ascii_letters))
f.close()



cipher = crymoire.Crymoire()
cipher.setKey(key)
#print(key)


message = "My secret message"

encs = [cipher.encrypt(message) for i in range(10)]
print(encs)

noise_clear = []
for i in range(len(encs[0])):
    cand = encs[0][i]
    noise_clear.append(cand)
    for j in range(1, len(encs)):
        if encs[j][i] != cand:
            noise_clear.pop(-1)
            break
print(noise_clear)

print("%r"%("".join(noise_clear)))
