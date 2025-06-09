import os

size_15 = os.path.getsize("terraform/main15.tf.json")
size_150 = os.path.getsize("terraform/main150.tf.json")

print(f"Tamaño de 15 recursos: {size_15} bytes")
print(f"Tamaño de 150 recursos: {size_150} bytes")
