import typing as T

import yaml

from mn_prompts.layers.models import Layer
from mn_prompts.layers.rules.get_layer_names import get_layer_names
from mn_prompts.prompts.rules.get_prompts_dir import get_prompts_dir


def get_layer(layer_name: str, required_by: T.Optional[str] = None) -> Layer:
    layer_names = get_layer_names()
    if layer_name not in layer_names:
        required_by_text = f" (required by {required_by})" if required_by else ""
        raise UnknownLayerError(
            f"The layer {layer_name}{required_by_text} does not exist. The "
            "available layers are:\n" + "\n".join(f"  {name}" for name in layer_names)
        )

    snippet_file = get_prompts_dir() / "layers" / layer_name / "index-snippet.md"
    if not snippet_file.is_file():
        raise MissingIndexSnippetError(
            f"The layer {layer_name} has no index snippet ({snippet_file})."
        )

    frontmatter, snippet = _split_frontmatter(snippet_file.read_text())
    return Layer(
        name=layer_name,
        snippet=snippet.strip(),
        required_layer_names=frontmatter.get("requires") or [],
    )


def _split_frontmatter(text: str) -> T.Tuple[T.Dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    frontmatter, separator, body = text[len("---\n") :].partition("\n---\n")
    if not separator:
        return {}, text
    return yaml.safe_load(frontmatter) or {}, body


class UnknownLayerError(Exception):
    pass


class MissingIndexSnippetError(Exception):
    pass
