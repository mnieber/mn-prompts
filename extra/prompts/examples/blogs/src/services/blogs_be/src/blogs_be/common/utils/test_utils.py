import re


def rhs_is_not_none(lhs, rhs):
    return rhs is not None


def deepdiff_regex_path(*indices):
    path = "root"
    for index in indices:
        if index is int:
            path += r"\[\d+\]"
        else:
            path += rf"\['{index}'\]"
    return path


class DeepDiffOperator:
    def __init__(self, cmp, *indices):
        self.regex = re.compile(deepdiff_regex_path(*indices))
        self.cmp = cmp

    def match(self, level) -> bool:
        return bool(self.regex.match(level.path()))

    def give_up_diffing(self, level, diff_instance) -> bool:
        return self.cmp(level.t1, level.t2)


def has_error_code(response, error_code):
    for error in response.data["errors"]:
        if error["code"] == error_code:
            return True
    return False
