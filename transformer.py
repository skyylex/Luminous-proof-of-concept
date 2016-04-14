import ast
import os
from operator import attrgetter

# TODO move classes to separate files


class DataCollectorCall:
    collected_variable = ""
    indentation = 0
    line_position = 0
    stacktrace_observable = False


class SourceCodeInfo:
    function_calls = []
    function_declarations = []
    statements = []
    codeString = ""


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

DESTINATION_SOURCE_FILE = "data_collection.txt"
SOURCE_FILE_NAME = "source.py"
IDENTIFIER_KEY = "id"
LINE_NUMBER_KEY = "lineno"
DEFAULT_INDENT_SIZE = 4

### Sample of the modification of existing source code
### http://stackoverflow.com/questions/768634/parse-a-py-file-read-the-ast-modify-it-then-write-back-the-modified-source-c

# TODO move process functions to separate file

def process_assign_node(node):
    statement = Statement()
    for target in node.targets:
        print("\ttarget.class: " + target.__class__.__name__)

        if target.__class__.__name__ == ast.Name.__name__:
            statement.destinationName = target.id
            statement.linePosition = target.lineno
            statement.indentation = target.col_offset
        else:
            if target.__class__.__name__ == ast.Subscript.__name__:
                statement.destinationName = target.value.id
                statement.subscriptIndexName = target.slice.value.id
                statement.linePosition = target.lineno
                statement.indentation = target.col_offset
    return statement


def process_func_call_node(node):
    function_call = FunctionCall()

    items = []
    for arg in node.args:
        # ast.Name
        items.append(arg.id)

    function_call.callFuncName = node.func.id
    function_call.arguments = items
    function_call.linePosition = node.lineno
    function_call.indentation = node.col_offset
    return function_call


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


def put_data_collector(variable, line_position):
    print variable + " " + str(line_position)


def generate_indentation(size):
    return " " * size


def build_data_collectors(source_code_info):
    data_collectors_info = []
    for statement in source_code.statements:
        data_collector = DataCollectorCall()
        data_collector.collected_variable = statement.destinationName
        data_collector.line_position = statement.linePosition + 1
        data_collector.indentation = statement.indentation
        data_collectors_info.append(data_collector)

    for function_declaration in function_declarations:
        for argument in function_declaration.args:
            data_collector = DataCollectorCall()
            data_collector.collected_variable = argument
            data_collector.line_position = function_declaration.startPosition + 1
            data_collector.indentation = DEFAULT_INDENT_SIZE
            data_collector.stacktrace_observable = True
            data_collectors_info.append(data_collector)
    data_collectors_info.sort(key=attrgetter('line_position'))
    return data_collectors_info


def generate_data_collector_call(data_collector_call, descriptor_name):
    indentation = generate_indentation(data_collector_call.indentation)
    var_name = data_collector_call.collected_variable
    file_write_call = descriptor_name + ".write(\"" + var_name + "\" + \" = \" + str(" + var_name + ") + \"\\n\")\n"
    return indentation + file_write_call


def apply_data_collectors(source_code_info):
    data_collectors_info = build_data_collectors(source_code_info)

    descriptor_name = "file_descriptor"
    result_code = descriptor_name + " = open(\"" + DESTINATION_SOURCE_FILE + "\", \"w\")\n"
    line_counter = 1
    code_lines = source_code.codeString.split("\n")

    if len(data_collectors_info) > 0:
        current_data_collector = data_collectors_info[0]
        data_collectors_info.remove(current_data_collector)

        for code_line in code_lines:
            while current_data_collector is not None and current_data_collector.line_position == line_counter:
                data_collector_call_string = generate_data_collector_call(current_data_collector, descriptor_name)
                result_code += "\n" + data_collector_call_string
                current_data_collector = None

                if len(data_collectors_info) > 0:
                    current_data_collector = data_collectors_info[0]
                    data_collectors_info.remove(current_data_collector)

            result_code = result_code + "\n" + code_line
            line_counter += 1

    result_code = result_code + "\n\n" + descriptor_name + ".close()"

    return result_code


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
            statement = process_assign_node(node)
            statements.append(statement)
        elif node.__class__.__name__ == ast.FunctionDef.__name__:
            function = process_func_declaration_node(node)
            function_declarations.append(function)
        elif node.__class__.__name__ == ast.Call.__name__:
            functionCall = process_func_call_node(node)
            function_calls.append(functionCall)

    source_code = SourceCodeInfo()
    source_code.function_calls = function_calls
    source_code.function_declarations = function_declarations
    source_code.statements = statements
    source_code.codeString = source_file_content

    result_source_code_file = "transformed_source_code.txt"
    transformed_source_code = apply_data_collectors(source_code)
    descriptor = open(result_source_code_file , "w")
    descriptor.write(transformed_source_code)
    descriptor.close()

    os.remove(DESTINATION_SOURCE_FILE) if os.path.exists(DESTINATION_SOURCE_FILE) else None

    execfile(result_source_code_file)

    print transformed_source_code

    print "\nFunction name used in calls"
    for call in function_calls:
        print call
    print "\nFunction declaration"
    for declaration in function_declarations:
        print declaration
    print "\n Collected statements"
    for statement in statements:
        print statement