import jwt

encoded = jwt.encode({'foo': 'bar'}, 'secret', algorithm='HS256')
print(encoded)
x = jwt.decode(encoded, 'secret', algorithms=['HS256'])
print(x)

