import typing as T

from mn_prompts.layers.models import Layer
from mn_prompts.layers.rules.get_layer import get_layer


def get_selected_layers(layer_names: T.List[str]) -> T.List[Layer]:
    # Add the layers that the selected layers require
    layer_by_name: T.Dict[str, Layer] = {}
    for layer_name in layer_names:
        _add_with_required_layers(get_layer(layer_name), layer_by_name)

    # Each layer comes after the layers that it requires, and ties are broken by name
    ordered_layers: T.Dict[str, Layer] = {}
    for layer_name in sorted(layer_by_name):
        _add_in_order(layer_by_name[layer_name], layer_by_name, ordered_layers, [])
    return list(ordered_layers.values())


def _add_with_required_layers(layer: Layer, layer_by_name: T.Dict[str, Layer]):
    if layer.name in layer_by_name:
        return
    layer_by_name[layer.name] = layer
    for required_layer_name in layer.required_layer_names:
        _add_with_required_layers(
            get_layer(required_layer_name, required_by=layer.name), layer_by_name
        )


def _add_in_order(
    layer: Layer,
    layer_by_name: T.Dict[str, Layer],
    ordered_layers: T.Dict[str, Layer],
    visiting: T.List[str],
):
    if layer.name in ordered_layers:
        return
    if layer.name in visiting:
        cycle = visiting[visiting.index(layer.name) :] + [layer.name]
        raise LayerDependencyCycleError(
            "The layers require each other: " + " -> ".join(cycle)
        )

    for required_layer_name in sorted(layer.required_layer_names):
        _add_in_order(
            layer_by_name[required_layer_name],
            layer_by_name,
            ordered_layers,
            visiting + [layer.name],
        )
    ordered_layers[layer.name] = layer


class LayerDependencyCycleError(Exception):
    pass
