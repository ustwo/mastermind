from __future__ import (absolute_import, print_function, division)
from jsonschema import Draft4Validator, exceptions
import os
import datetime
import yaml

from .say import logger


def check(instance, schema):
    v = Draft4Validator(schema)
    timestamp = datetime.datetime.utcnow().isoformat()
    errors = [to_hashmap(x, timestamp) for x in sorted(v.iter_errors(instance),
                                                       key=exceptions.relevance)]

    if len(errors) > 0: logger.warning(errors)

    return errors

def is_valid(instance, schema):
    return len(check(instance, schema)) == 0


def to_hashmap(item, timestamp):
    return {"message": item.message,
            "context": item.context,
            "timestamp": timestamp,
            "cause": item.cause,
            "schema_path": list(item.schema_path),
            "path": list(item.absolute_path)}

rule_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "title": "Mastermind rule schema",
  "additionalProperties": False,
  "properties": {
    "name": {
      "id": "name",
      "type": "string",
      "title": "The name of the rule",
      "description": "This is only used by users to identify a rule.",
      "name": "name"
    },
    "url": {
      "id": "url",
      "type": "string",
      "title": "The URL or URL pattern to match against",
      "description": "The main identifier for a rule.  This value will be used in the request matching process",
      "name": "url"
    },
    "method": {
      "id": "method",
      "type": "string",
      "name": "method"
    },
    "schema": {
      "id": "schema",
      "type": "string",
      "name": "schema"
    },
    "request": {
      "id": "request",
      "type": "object",
      "name": "request",
      "additionalProperties": False,
      "properties": {
        "skip": {
          "id": "skip",
          "type": "boolean",
          "name": "skip"
        },
        "headers": {
            "id": "headers",
            "type": "object",
            "name": "headers",
            "properties": {
                "add": {
                    "id": "add",
                    "type": "object",
                    "name": "add"
                },
                "remove": {
                    "id": "remove",
                    "type": "array",
                    "name": "remove"
                }
            }
        }
      }
    },
    "response": {
      "id": "response",
      "type": "object",
      "name": "response",
      "additionalProperties": False,
      "properties": {
        "body": {
          "id": "body",
          "type": "string",
          "name": "body"
        },
        "code": {
          "id": "code",
          "type": "integer",
          "name": "code"
        },
        "delay": {
          "id": "delay",
          "type": "integer",
          "name": "delay"
        },
        "headers": {
            "id": "headers",
            "type": "object",
            "name": "headers",
            "properties": {
                "add": {
                    "id": "add",
                    "type": "object",
                    "name": "add"
                },
                "remove": {
                    "id": "remove",
                    "type": "array",
                    "name": "remove"
                }
            }
        }
      }
    }
  },
  "required": ["url"]
}

ruleset_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "/",
  "type": "array",
  "name": "/",
  "items":  rule_schema,
}
