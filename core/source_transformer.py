import command_line
import ast
import os
import traceback
from operator import attrgetter

import settings
from execution_tree_builder import build_execution_tree

# TODO move classes to separate files


class DataCollectorCall(object):
    def __init__(self, var_name="", indentation=0, line_position=0, need_stacktrace=False, is_return_operator=False):
        self.collected_variable = var_name
        self.indentation = indentation
        self.line_position = line_position
        self.need_stacktrace = need_stacktrace
        self.is_return_operator = is_return_operator


class SourceCodeInfo(object):
    def __init__(self, function_calls=[], function_declarations=[], statements=[], source_code_string="", return_calls=[]):
        self.function_calls = function_calls
        self.function_declarations = function_declarations
        self.statements = statements
        self.source_code_string = source_code_string
        self.return_calls = return_calls


class FunctionCall(object):
    def __init__(self, func_name="", arguments=[], line_position=0, indentation=0, parent_function=""):
        self.func_name = func_name
        self.arguments = arguments
        self.line_position = line_position
        self.indentation = indentation
        self.parent_function = parent_function

    def __str__(self):
        return self.func_name + " " + str(self.line_position)


class FunctionDeclaration(object):
    def __init__(self, func_name="", arguments=[], start_position=0, end_position=0):
        self.name = func_name
        self.arguments = arguments
        self.start_position = start_position
        self.end_position = end_position

    def __str__(self):
        return self.name + " " + str(self.arguments) + " " + str(self.start_position) + " " + str(self.end_position)


class ReturnCall(object):
    def __init__(self, line_position = 0, indentation = 0):
        self.line_position = line_position
        self.indentation = indentation


class Statement(object):
    def __init__(self, destination_var_name="", subscript_key="", line_position=0, indentation=0):
        self.destination_var_name = destination_var_name
        self.subscript_key = subscript_key
        self.line_position = line_position
        self.indentation = indentation

    def __str__(self):
        return self.destination_var_name + " " + str(self.line_position)


class VariableAsFunction(object):
    def __init__(self):
        self.var_name = ""
        self.type = "" # ???
        self.dependencies = ()

### Sample of the modification of existing source code
### http://stackoverflow.com/questions/768634/parse-a-py-file-read-the-ast-modify-it-then-write-back-the-modified-source-c

# TODO move process functions to separate file


def process_assign_node(node):
    statement = Statement()

    if isinstance(node, ast.AugAssign):
        statement.destination_var_name = node.target.id
        statement.line_position = node.target.lineno
        statement.indentation = node.target.col_offset
    else:
        for target in node.targets:
            if isinstance(target, ast.Name):
                statement.destination_var_name = target.id
                statement.line_position = target.lineno
                statement.indentation = target.col_offset
            elif isinstance(target, ast.Subscript):
                statement.destination_var_name = target.value.id
                statement.subscript_key = target.slice.value.id
                statement.line_position = target.lineno
                statement.indentation = target.col_offset

    if isinstance(node.value, ast.List):
        for list_item in node.value.elts:
            if is_value_type(list_item):
                print "Value type"
            else:
                print "Other type"
    elif isinstance(node.value, ast.BinOp):
        print "Binary operation"
        process_operand(node.value.left)
        process_operand(node.value.right)
    elif isinstance(node.value, ast.Subscript):
        print "Subscript assign "
    elif is_value_type(node.value):
        print ""
    else:
        print "Unhandled assign type"

    return statement


def process_operand(operand):
    if isinstance(operand, ast.Num):
        print "Operand is a number."
    elif isinstance(operand, ast.Call):
        print "Operand is function call."
    else:
        print "Unhandled operand's processing."


def is_value_type(item):
    # TODO: extend with
    return isinstance(item, ast.Num)

def process_return_call_node(node):
    return_call = ReturnCall(line_position=node.lineno, indentation=node.col_offset)
    return return_call


def process_func_call_node(node):
    function_call = FunctionCall()

    items = []
    for arg in node.args:
        # ast.Name
        if isinstance(arg, ast.Name):
            items.append(arg.id)

    function_call.func_name = node.func.id
    function_call.arguments = items
    function_call.line_position = node.lineno
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
    declaration.start_position = node.lineno
    for element in node.body:
        if element.lineno > declaration.end_position:
            declaration.end_position = element.lineno

    return declaration


def put_data_collector(variable, line_position):
    print variable + " " + str(line_position)


def generate_indentation(size):
    return " " * size


def build_data_collectors(source_code_info):
    """
    Build structures with arguments for generating file write capturing calls
    """

    file_write_calls = []
    for statement in source_code_info.statements:
        line_position = statement.line_position + 1
        data_collector = DataCollectorCall(statement.destination_var_name, statement.indentation, line_position)
        file_write_calls.append(data_collector)

    for function_declaration in source_code_info.function_declarations:
        for argument in function_declaration.args:
            line_position = function_declaration.start_position + 1
            data_collector = DataCollectorCall(argument, settings.DEFAULT_INDENT_SIZE, line_position, True)
            file_write_calls.append(data_collector)

    for return_call in source_code_info.return_calls:
        data_collector = DataCollectorCall(indentation=return_call.indentation,
                                           line_position=return_call.line_position - 1,
                                           is_return_operator=True,
                                           need_stacktrace=True)
        file_write_calls.append(data_collector)

    file_write_calls.sort(key=attrgetter('line_position'))
    return file_write_calls


def generate_data_collector_call(data_collector_call, descriptor_name):
    result_write_call = ""

    indentation = generate_indentation(data_collector_call.indentation)

    if data_collector_call.need_stacktrace:
        stacktrace_type = settings.META_MARK_FUNC_CALL_STACKTRACE
        if data_collector_call.is_return_operator == True:
            stacktrace_type = settings.META_MARK_RETURN_STACKTRACE

        file_write_call_string = "{}.write(\"{}\" + str(traceback.extract_stack()) + \"\\n\")\n".format(descriptor_name,
                                                                                                        stacktrace_type)
        stacktrace_snapshot_call = indentation + file_write_call_string
        result_write_call += stacktrace_snapshot_call

    if data_collector_call.is_return_operator == False:
        var_name = data_collector_call.collected_variable
        file_write_call_string = "{}.write(\"{} \" + \"{} = \" + str({}) + \"\\n\")\n".format(descriptor_name,
                                                                                              settings.META_MARK_VARCHANGE,
                                                                                              var_name, var_name)
        var_change_write_call = indentation + file_write_call_string

        result_write_call += var_change_write_call

    return result_write_call


def apply_data_collectors(source_code_info):
    data_collectors_info = build_data_collectors(source_code_info)

    result_code = settings.FILE_DESCRIPTOR_NAME + " = open(\"" + settings.COLLECTED_DATA_FILE + "\", \"w\")\n"
    line_counter = 1
    code_lines = source_code_info.source_code_string.split("\n")

    if len(data_collectors_info) > 0:
        current_data_collector = data_collectors_info[0]
        data_collectors_info.remove(current_data_collector)

        for code_line in code_lines:
            while current_data_collector is not None and current_data_collector.line_position == line_counter:
                result_code += "\n" + generate_data_collector_call(current_data_collector, settings.FILE_DESCRIPTOR_NAME)
                current_data_collector = None
                if len(data_collectors_info) > 0:
                    current_data_collector = data_collectors_info[0]
                    data_collectors_info.remove(current_data_collector)

            result_code = result_code + "\n" + code_line
            line_counter += 1

    result_code = "{}\n{}{}".format(result_code, settings.FILE_DESCRIPTOR_NAME, ".close()")

    return result_code