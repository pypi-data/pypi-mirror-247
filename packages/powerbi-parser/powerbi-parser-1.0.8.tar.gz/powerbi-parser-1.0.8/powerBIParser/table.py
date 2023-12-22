import json

class Table:
    def __init__(self, name, lineageTag, annotations, tableItem):
        self.raw = tableItem
        self.name = name
        self.lineageTag = lineageTag
        self.annotations = annotations
        self.fields = []
        self.sources = []

    def toJSON(self):
        tmpRaw = None
        if hasattr(self, "raw"):
            tmpRaw = self.raw
            del self.raw
        output = json.dumps(self, default=lambda o: 
                          o.__dict__ if Table == type(o) or not hasattr(o, "toJSON")else o.toJSON(), indent=4)
        self.raw = tmpRaw
        return json.loads(output)
    def __repr__(self):
        return type(self).__name__+" = "+self.name
    def __str__(self):
        return self.name