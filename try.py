import json

data = {
    "name": "Alice",
    "age": 25
}

json_string = json.dumps(data)
#print(json_string)

python_obj = json.loads(json_string)
print(python_obj) 