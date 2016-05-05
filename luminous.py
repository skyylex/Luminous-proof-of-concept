#!/usr/bin/python

from core import command_line
from core import settings
from core import source_transformer

from core.source_transformer import process_assign_node
from core.source_transformer import process_func_call_node
from core.source_transformer import process_func_declaration_node
from core.source_transformer import process_return_call_node
from core.source_transformer import SourceCodeInfo
from core.execution_tree_builder import build_function_calls
from core.source_transformer import apply_data_collectors

import ast
import os
import traceback
from operator import attrgetter
import pickle

from support import arff_logger
from support import data_generator

# TODO: investigate move to def main(). The problem is that "file_descriptor" in the transformed code becomes invisible in some places.
if __name__ == "__main__":
    user_configuration = command_line.process_command_line_arguments()

    if user_configuration.argument_error is not None:
        print "Error occured during command-line argument processing: " + str(user_configuration.argument_error)
    else:
        auto_generated_input = user_configuration.input_generating_type == command_line.INPUT_OPTION_NUM_LIST
        input_size = int(user_configuration.input_generating_size)

        if auto_generated_input:
            random_num_list = data_generator.generate_random_list(input_size, 1, 100)
            print "Generated list: " + str(random_num_list)
            with open(settings.INPUT_DATA_FILE, "wb") as input_file:
                pickle.dump(random_num_list, input_file)

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
                if "id" in node.func._fields and node.func.id != "open":
                    function_call = process_func_call_node(node)
                    function_calls.append(function_call)
                elif "id" not in node.func._fields and "value" not in node.func._fields:
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

        execution_function_calls = build_function_calls(settings.COLLECTED_DATA_FILE)

        # TODO move to separate
        unique_func_names = []
        for function_call in execution_function_calls:
            if not (function_call in unique_func_names):
                unique_func_names.append(function_call.name)

        # TODO move to separate

        arff_logger.log_execution_info(input_size, 0, 0, 0, 0, 0)