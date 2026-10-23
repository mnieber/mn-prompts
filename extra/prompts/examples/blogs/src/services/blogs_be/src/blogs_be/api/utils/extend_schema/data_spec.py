from blogs_be.common.utils.inspect import get_argument_names


def resolve_data_spec(data_spec, initial_resolved_data):
    resolved_data = initial_resolved_data.copy()
    unresolved_entries = data_spec.copy()

    def resolve_entry(key, resolve_fn):
        var_names = get_argument_names(resolve_fn)
        args = {
            arg_name: resolved_data[arg_name]
            for arg_name in var_names
            if arg_name in resolved_data
        }
        has_result = len(args) == len(var_names)
        result = resolve_fn(**args) if has_result else None
        return result, has_result

    while unresolved_entries:
        resolved_any = False
        for key, resolve_fn in list(unresolved_entries.items()):
            result, has_result = resolve_entry(key, resolve_fn)
            if has_result:
                resolved_any = True
                resolved_data[key] = result
                del unresolved_entries[key]

        if not resolved_any:
            raise ValueError(
                "Cannot resolve dependencies among data entries. "
                + f"Unresolved entries: {unresolved_entries}"
            )

    return resolved_data


def get_data_kwargs(
    kwarg_names,
    request_data,
    resolved_data,
    data_args_never_passed,
):
    data_kwargs = {
        arg_name: resolved_data[arg_name]
        for arg_name in kwarg_names
        if arg_name in resolved_data and arg_name not in data_args_never_passed
    }
    if "request_data" in kwarg_names:
        data_kwargs["request_data"] = request_data
    return data_kwargs
