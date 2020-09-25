from django.core import signing
value = signing.dumps({"foo":"bar"})
src = signing.loads(value)
print(value)
print(src)