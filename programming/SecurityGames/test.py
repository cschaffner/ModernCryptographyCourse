import nacl.secret
import nacl.utils

# This must be kept secret, this is the combination to your safe
key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)

# This is your safe, you can use it to encrypt or decrypt messages
box = nacl.secret.SecretBox(key)

# This is our message to send, it must be a bytestring as SecretBox will
#   treat it as just a binary blob of data.
message = b"The president will be exiting through the lower levels"

# Encrypt our message, it will be exactly 40 bytes longer than the
#   original message as it stores authentication information and the
#   nonce alongside it.
encrypted = box.encrypt(message)

assert len(encrypted) == len(message) + box.NONCE_SIZE + box.MACBYTES

nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

encrypted = box.encrypt(message, nonce)

# since we are transmitting the nonce by some other means,
# we just need to get the ciphertext and authentication data

ctext = encrypted.ciphertext

# ctext is just nacl.secret.SecretBox.MACBYTES longer
# than the original message

assert len(ctext) == len(message) + box.MACBYTES

# Decrypt our message, an exception will be raised if the encryption was
#   tampered with or there was otherwise an error.
plaintext = box.decrypt(encrypted)
print(plaintext.decode('utf-8'))