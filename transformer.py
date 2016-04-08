import ast

SOURCE_FILE_NAME = "source.py"
IDENTIFIER_KEY = "id"
LINE_NUMBER_KEY = "lineno"

### Sample of the modification of existing source code
### http://stackoverflow.com/questions/768634/parse-a-py-file-read-the-ast-modify-it-then-write-back-the-modified-source-c

if __name__=="__main__":
    source_file = open(SOURCE_FILE_NAME)
    source_file_content = source_file.read()
    syntax_tree = ast.parse(source_file_content)

    collected_ids = []
    line_numbers = []
    function_definitions = {}
    function_calls = []

    for node in ast.walk(syntax_tree):
        print("node.class: " + node.__class__.__name__)
        if node.__class__.__name__ == ast.Assign.__name__:
            for target in node.targets:
                print("target.class: " + target.__class__.__name__)
                if target.__class__.__name__ == ast.Name.__name__:
                    for field in target._fields:
                        collected_ids.append(getattr(target, IDENTIFIER_KEY, None))
                        line_numbers.append(getattr(target, LINE_NUMBER_KEY, None))
                else:
                    if target.__class__.__name__ == ast.Subscript.__name__:
                        value = getattr(target, "value")
                        if getattr(target, "value").__class__.__name__ == ast.Name.__name__:
                            collected_ids.append(getattr(value, IDENTIFIER_KEY, None))
                            line_numbers.append(getattr(target, LINE_NUMBER_KEY, None))
        elif (node.__class__.__name__ == ast.FunctionDef.__name__):
            function_def_args = []
            for arg in node.args.args:
                # ast.Name
                function_def_args.append(arg.id)

            function_definitions[node.name] = function_def_args
        elif (node.__class__.__name__ == ast.Call.__name__):
            items = []
            for arg in node.args:
                # ast.Name
                items.append(arg.id)

            function_calls.append({node.func.id : items})

    print function_calls
    print function_definitions
    print collected_ids
    print line_numbers



# exclude = [
#     # "function",
#     # "type",
#     # "list",
#     # "dict",
#     # "tuple",
#     "wrapper_descriptor",
#     "module",
#     "method_descriptor",
#     "member_descriptor",
#     "instancemethod",
#     "builtin_function_or_method",
#     "frame",
#     "classmethod",
#     "classmethod_descriptor",
#     "_Environ",
#     "MemoryError",
#     "_Printer",
#     "_Helper",
#     "getset_descriptor",
#     "weakref",
#     "property",
#     "cell",
#     "staticmethod"
#     ]
#
# def dumpObjects():
#     gc.collect()
#     oo = globals()
#     for o in oo:
#         # print o.type()
#         # print type(o)
#
#         if getattr(o, "__class__", None):
#             name = o.__class__.__name__
#             if name == "list":
#                 print o