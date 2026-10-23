# Skill: py-write-schema

Applies when writing a schema file: pydantic classes that describe the internal structure of a JSON blob.

---

## What is a schema?

A schema file contains pydantic classes that validate and describe the structure of a JSON blob — for example, an API response or a configuration file. Schemas are distinct from models (which are plain dataclassy dataclasses representing domain entities).

## File location

Place schema files where they are closest to the code that uses them (typically alongside the module that reads or writes the JSON).

## Checklist

- [ ] Schema classes are pydantic models
- [ ] Schema is used for JSON validation, not as a domain model
