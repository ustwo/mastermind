from jsonschema import Draft4Validator, exceptions

def check(instance, schema):
    v = Draft4Validator(schema)
    timestamp = datetime.datetime.utcnow().isoformat()

    return [to_hashmap(x, timestamp) for x in sorted(v.iter_errors(yaml.safe_load(instance)),
                                                     key=exceptions.relevance)]

def to_hashmap(item, timestamp):
    return {"message": item.message,
            "context": item.context,
            "timestamp": timestamp,
            "cause": item.cause,
            "schema_path": list(item.schema_path),
            "path": list(item.absolute_path)}
