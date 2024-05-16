#!/usr/bin/env python3
import pyotp
import qrcode
"""
# key = pyotp.random_base32()
key = "NomioSuga6767"  # Key should be base32

totp = pyotp.TOTP(key)
print(totp.now())		# every 30 sec
input_code = input("Enter 2FA code:")	# totp - timed one time password
# code = totp.now()
# print(code == input_code)
print(totp.verify(input_code))
"""
key = "OochkoSuga3456"

uri = pyotp.totp.TOTP(key).provisioning_uri(name="username", issuer_name="Hicheejiinoo Web")
print(uri)
qrcode.make(uri).save("2fa.png")

totp = pyotp.TOTP(key)
print(totp.verify(input("Enter 2fa code: ")))
