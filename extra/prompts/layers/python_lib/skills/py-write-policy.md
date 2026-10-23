# Skill: py-write-policy

Applies when writing a policy: a class that hides an interaction with the outside world (e.g. an external service,
or a third-party tool), so that it can be replaced, e.g. by a fake in the tests.

---

## File location

```
<module>/policies/<name>_policy.py           ← the abstract base class
<module>/policies/<impl>_<name>_policy.py    ← each implementation
<module>/rules/create_<name>_policy.py       ← the rule that creates the policy
```

## Structure

The base class is an `ABC` with an abstract method per interaction. An implementation subclasses it.

```python
from abc import ABC, abstractmethod


class RfaPolicy(ABC):
    @abstractmethod
    def run(self, rfa: Rfa) -> None:
        pass
```

The config names the policy that is used, by the import path (`<module>:<name>`) of a callable that returns it
(e.g. the class). The default value is the real implementation. The create rule imports the callable and calls it:

```python
def create_rfa_policy(config: Config) -> RfaPolicy:
    return import_object(config.rfa_policy)()
```

The tests point the config at a callable that returns a fake (e.g. a singleton that replays scripted answers, and
records the requests that it receives).

## Checklist

- [ ] The base class and each implementation are in their own file under `<module>/policies/`
- [ ] The code only depends on the base class, and gets the policy from the create rule
- [ ] The config names the policy by its import path, with the real implementation as the default
