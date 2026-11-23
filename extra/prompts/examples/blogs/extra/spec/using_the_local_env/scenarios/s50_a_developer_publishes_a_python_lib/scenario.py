import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s50_a_developer_publishes_a_python_lib")


def run_scenario():
    r.developer = c.External.Actors.Developer
    r.uv = c.External.Actors.Uv
    r.pypi = c.External.Actors.PyPI
    r.publish_target = c.Python.Targets.Publish

    with goal().publish_a(r.library).to(r.pypi):
        the(r.developer).bumps_the(r.version).of_the(r.library)
        with the(r.developer).runs(r.publish_target).with_the(r.package_dir):
            it().asks(r.uv).to_build_the(r.library).into_a(r.temp_dir)
            it().shows_the(r.built_files)
            it().asks_the(r.developer).for_the(r.password)
            with it().asks(r.uv).to_upload_the(r.built_files).to(r.pypi):
                it().uses_the(r.username).and_the(r.publish_url).from_the(r.config)
                it().passes_the(r.password).in_the(r.environment)
            it().removes_the(r.temp_dir)

    with goal().publish_a(r.library).to_another(r.index):
        the(r.developer).sets_the(r.publish_url).in_their(r.local_config)
        the(r.developer).runs(r.publish_target).with_the(r.package_dir)


markdown_node = sunya.add_markdown_node(
    scenario, "A developer publishes a Python library"
)

markdown_node.markdown = """
The developer publishes one of their Python libraries to PyPI. The settings of the upload (the user name and the url
of the index) are in the `/python/pypi` section of the config, so the developer only types their password, at the
moment of the upload.

## Diagram

```mermaid
flowchart TD
    bump(["The developer bumps the version of the library [1]"]) --> publish

    subgraph to_pypi ["Publish a library to PyPI"]
        publish["The developer runs jaz python.publish with the package dir [2]"] --> build["Build the library into a temp dir [3]"]
        build --> show["Show the built files"]
        show --> password["Ask for the password [4]"]
        password --> empty{{"Is the password empty?"}}:::choice
        empty -- yes --> abort["Abort the upload"]
        empty -- no --> upload["Upload the built files [5]"]
        upload --> remove["Remove the temp dir"]
        abort --> remove
    end

    other_index(["The developer wants to publish to another index"]) --> publish_url

    subgraph to_other_index ["Publish a library to another index"]
        publish_url["Override the publish url in local.yaml [6]"]
    end

    publish_url --> publish

    classDef choice color:#c9a227
```

### Footnotes

#### [1] - PyPI never accepts the same version twice

The developer bumps the `version` in the `pyproject.toml` of the library.</br>

#### [2] - A relative package dir is relative to the root dir of the project

The developer runs e.g. `jaz python.publish package-dir=src/libs/python_toolkit`.</br>
`python.publish` delegates to `python_tools.py`, which runs on the host.</br>

#### [3] - Only the files of this build are uploaded

`uv build` builds the sdist and the wheel into a temp dir. The target shows the built files, so that the developer
sees the package name and version before the upload.</br>

#### [4] - The password is never stored

The target asks for the password without echoing it. For PyPI, the user name is `__token__`, and the password is an
API token of the developer.</br>

#### [5] - The password never shows up in the args of a process

`uv publish` uploads the built files to `/python/pypi/publish_url` as `/python/pypi/username`. The password reaches
`uv` in `UV_PUBLISH_PASSWORD`.</br>

#### [6] - The developer overrides the url of the index in their own config

To upload to another index (e.g. TestPyPI), the developer overrides `/python/pypi/publish_url` in their own
`local.yaml`, and runs `python.publish` as before.</br>
"""
