from jsonschema import validate

buzz = {
  "method": "buzz",
  "parameters": {
    "uuid": {'type':'string'},
    "user": {'type':'string'}
  }
}
