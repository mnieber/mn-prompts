# Skill: py-write-rule

Applies when writing a rule file: a function that retrieves or computes information subject to business logic, without modifying application state.

Primary reference: `bookie/chapters/rules/is_bad_word.py`

---

## File location

```
<module>/rules/<rule_name>.py
```

## What is a rule?

A rule is a function that retrieves information (from the application state, or otherwise) subject to business logic. Rules do not change state — that is the responsibility of actions.

**Rule vs. util:** functions that involve business logic are rules; functions that are free from business logic (generic helpers) are utils. For example, `is_bad_word` is a rule because it encodes a domain-specific definition of "bad word". `strip_prefix` is a util because it is a generic string operation with no opinion about the domain.

## Checklist

- [ ] Function lives under `<module>/rules/`
- [ ] Function does not modify application state
- [ ] Logic is domain-specific (opinionated) — otherwise it belongs in `utils/`
