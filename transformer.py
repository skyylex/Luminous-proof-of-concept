import ast

class FunctionCall:
    # Semantic
    callFuncName = ""
    arguments = ()

    # Location
    linePosition = 0
    indentation = 0
    containerFunction = ""

    def __str__(self):
        return self.callFuncName + " " + str(self.linePosition)


class FunctionDeclaration:
    name = ""
    arguments = ()
    startPosition = 0
    endPosition = 0

    def __str__(self):
        return self.name + " " + str(self.arguments) + " " + str(self.startPosition) + " " + str(self.endPosition)


class Statement:
    destinationName = ""
    subscriptIndexName = ""
    linePosition = 0
    indentation = 0

    def __str__(self):
        return self.destinationName + " " + str(self.linePosition)


class VariableAsFunction:
    varName = ""
    type = "" # ???
    dependencies = ()

SOURCE_FILE_NAME = "source.py"
IDENTIFIER_KEY = "id"
LINE_NUMBER_KEY = "lineno"

### Sample of the modification of existing source code
### http://stackoverflow.com/questions/768634/parse-a-py-file-read-the-ast-modify-it-then-write-back-the-modified-source-c


def process_assign_node(node):
    return


def process_func_call_node(node):
    functionCall = FunctionCall()

    items = []
    for arg in node.args:
        # ast.Name
        items.append(arg.id)

    functionCall.callFuncName = node.func.id
    functionCall.arguments = items
    functionCall.linePosition = node.lineno
    functionCall.indentation = node.col_offset
    return functionCall


def process_func_declaration_node(node):
    declaration = FunctionDeclaration()

    function_args = []
    for arg in node.args.args:
        # ast.Name
        function_args.append(arg.id)

    declaration.name = node.name
    declaration.args = function_args
    declaration.startPosition = node.lineno
    for element in node.body:
        if element.lineno > declaration.endPosition:
            declaration.endPosition = element.lineno

    return declaration


if __name__=="__main__":
    source_file = open(SOURCE_FILE_NAME)
    source_file_content = source_file.read()
    syntax_tree = ast.parse(source_file_content)

    collected_variable_names = []
    var_used_line_numbers = []
    function_declarations = []
    function_calls = []
    statements = []
    for node in ast.walk(syntax_tree):
        print("node.class: " + node.__class__.__name__)
        if node.__class__.__name__ == ast.Assign.__name__:
            statement = Statement()
            for target in node.targets:
                print("\ttarget.class: " + target.__class__.__name__)

                if target.__class__.__name__ == ast.Name.__name__:
                    statement.destinationName = target.id
                    statement.linePosition = target.lineno
                    statement.indentation = target.col_offset
                    statements.append(statement)
                else:
                    if target.__class__.__name__ == ast.Subscript.__name__:
                        statement.destinationName = target.value.id
                        statement.subscriptIndexName = target.slice.value.id
                        statement.linePosition = target.lineno
                        statement.indentation = target.col_offset
                        statements.append(statement)
        elif node.__class__.__name__ == ast.FunctionDef.__name__:
            function = process_func_declaration_node(node)
            function_declarations.append(function)
        elif node.__class__.__name__ == ast.Call.__name__:
            functionCall = process_func_call_node(node)
            function_calls.append(functionCall)

    print "\nFunction name used in calls"
    for call in function_calls:
        print call
    print "\nFunction declaration"
    for declaration in function_declarations:
        print declaration
    print "\n Collected statements"
    for statement in statements:
        print statement