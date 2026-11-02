# Instructions

This directory contains the instructions for a spec-driven software development process, where specifications are
written first, then mapped to implementation. It combines the layers below: each layer holds the instructions for
one technology.

If [project.md](./project.md) exists, then read it first: it describes the project, and says which layers apply to
which part of it.

## Overview

Before you write code (or a plan for it), read the index files of the layers below that apply to your work, to
identify the skills that apply to the code units, and follow them closely.

## The layers

{{layers}}

## Paths

- The `<layer_name>_layer` entries in this directory are symlinks to the layers, and `examples` is a symlink to the
  reference apps.
- A path in a skill file that starts with `examples/` or `<layer_name>_layer/` is relative to this directory.
- A skill may refer to a skill of a layer that is not in this directory. Ignore such a reference.
