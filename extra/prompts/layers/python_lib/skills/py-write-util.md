# Skill: py-write-util

Applies when writing a utility file: a generic helper function free from business logic.

Primary reference: `bookie/chapters/utils/strip_prefix.py`

---

## File location

```
<module>/utils/<util_name>.py
```

Typically each utility function lives in its own file. The exception is a group of many small, closely related functions (e.g. small math helpers) — these may share a single group file. When in doubt, ask whether a separate file or a group file is more appropriate.

## Rule vs. util

- **Rule** — the function encodes business logic or a domain opinion (e.g. `is_bad_word`). Lives in `<module>/rules/`.
- **Util** — the function is generic and free from domain opinion (e.g. `strip_prefix`). Lives in `<module>/utils/`.

## Checklist

- [ ] Function lives under `<module>/utils/`
- [ ] Function has no business logic or domain opinion — otherwise it belongs in `rules/`
- [ ] One function per file, unless functions are small and clearly grouped
