import os
lst = []
for x in os.listdir(__file__[:-12]) and x != '__pycache__':
  if os.path.isdir(__file__[:-12]+"/"+x):
    lst.append(x)

print(f"""
This is a container for modules to make importing my own projects easier and more universal.
Access a module of mine via "from ultralink import module_name_here".

Found modules:
{lst}
""")