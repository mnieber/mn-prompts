# General code generation instructions

`RULE`: do not insert references to the spec files when writing code. Small inline comments to guide the flow are good, but don't explain the bigger ideas in the code. Assume that the user learns about these ideas by refering to the spec files on their own.

## Please follow the rules very closely

In the instructions in the reference data, I will indicate the rules using a `RULE:` prefix.
It's extremely important to follow the rules as closely as possible. If the rules are not followed closely then I will have to manually edit the generated source files, which will result in a very tedious process. This should be avoided at all cost.

## Use of specific code generation instructions relevant to the code unit

When you need to write the source code for a code unit (such as an api view), then a specific set of instructions for writing such a code unit will be available in the project instructions. If you cannot find the specific instructions, please let me know.

## Use of example code

The project instructions will always contain references to example code. It's important that this example code is followed closely when generating the requested code. If you cannot find the referenced example code, please let me know.

Each example has an extra/spec_src directory with scenario specs, as well as a src directory with source code that is based on these scenario specs. By studying the example src code and the example spec files, you will be able to see how the information in the spec files is used for generating a specific source file.
