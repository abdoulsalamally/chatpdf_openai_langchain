from rave_python import Rave, RaveExceptions, Misc
rave = Rave("FLWPUBK_TEST-645532d24e73e56cdf04a8292d7d15d4-X", "FLWSECK_TEST-1f3416a7a9063c640a15efac209f3a84-X", usingEnv = False)

# mobile payload
payload = {
  "amount": "500",
  "email": "lokukuminga@gmail.com",
  "phonenumber": "0766415764",
  "redirect_url": "http://127.0.0.1:8000/receivepayment",
  "IP":""
}

try:
  res = rave.UGMobile.charge(payload)
  print(res)
  res = rave.UGMobile.verify(res)
  print(res)

except RaveExceptions.TransactionChargeError as e:
  print(e.err)
  print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
  print(e.err["errMsg"])
  print(e.err["txRef"])