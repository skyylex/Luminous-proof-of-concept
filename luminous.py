#!/usr/bin/python

from core import command_line
from core import settings
from core import source_transformer

from core.source_transformer import process_assign_node
from core.source_transformer import process_func_call_node
from core.source_transformer import process_func_declaration_node
from core.source_transformer import process_return_call_node
from core.source_transformer import SourceCodeInfo
from core.source_transformer import build_execution_tree
from core.source_transformer import apply_data_collectors

import ast
import os
import traceback
from operator import attrgetter

# TODO: investigate move to def main(). The problem is that "file_descriptor" in the transformed code becomes invisible in some places.
if __name__ == "__main__":
    user_configuration = command_line.process_command_line_arguments()

    if user_configuration.argument_error is not None:
        print "Error occured during command-line argument processing: " + str(user_configuration.argument_error)
    else:
        with open(user_configuration.source_file) as source_file:
            source_file_content = source_file.read()

        syntax_tree = ast.parse(source_file_content)

        function_declarations = []
        function_calls = []
        statements = []
        return_calls = []

        collected_nodes_names = []

        for node in ast.walk(syntax_tree):
            collected_nodes_names.append(node.__class__.__name__)

            # TODO: investigate replacement manual checking node.__attributes to usage of ast.NodeVisitor

            if isinstance(node, ast.Assign) or isinstance(node, ast.AugAssign):
                statement = process_assign_node(node)
                statements.append(statement)
            elif isinstance(node, ast.FunctionDef):
                function = process_func_declaration_node(node)
                function_declarations.append(function)
            elif isinstance(node, ast.Call):
                function_call = process_func_call_node(node)
                function_calls.append(function_call)
            elif isinstance(node, ast.Return):
                return_call = process_return_call_node(node)
                return_calls.append(return_call)

        with open(settings.TRANSFORMED_SOURCE_FILE, "w") as transformed_source_file:
            source_code = SourceCodeInfo(function_calls, function_declarations, statements, source_file_content, return_calls)
            transformed_source_code = apply_data_collectors(source_code)
            transformed_source_file.write(transformed_source_code)

        if os.path.exists(settings.COLLECTED_DATA_FILE):
            os.remove(settings.COLLECTED_DATA_FILE)
        execfile(settings.TRANSFORMED_SOURCE_FILE)

        execution_tree = build_execution_tree(settings.COLLECTED_DATA_FILE)

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