import sys
import argparse

# Options
SOURCE_FILE_OPTION_KEY = "--source-file"
GENERATE_INPUT_OPTION = "--generate-input"
INPUT_SIZE_OPTION = "--input-size"

# Option values
INPUT_OPTION_NUM_LIST = "num_list"


class ArgumentError:
    def __init__(self, argument):
        self.argument_name = argument


class ExecutionOption:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class ExecutionSettings:
    def __init__(self, namespace, error=None):
        self.source_file = namespace.source_file
        self.input_generating_type = namespace.gen_input_type
        self.input_generating_size = namespace.gen_input_size
        self.argument_error = error


def check_option_key(argument_key):
    return argument_key in [SOURCE_FILE_OPTION_KEY, GENERATE_INPUT_OPTION, INPUT_SIZE_OPTION]


def validate_arguments_count(arguments_count):
    return arguments_count == 3 or arguments_count == 7


def validate_execution_option(option):
    # TODO: improve validation
    return check_option_key(option.key)


def store_argument(execution_option, execution_settings):
    if execution_option.key == SOURCE_FILE_OPTION_KEY:
        execution_settings.source_code_file = execution_option.value
    elif execution_option.key == GENERATE_INPUT_OPTION and execution_option.value == INPUT_OPTION_NUM_LIST:
        execution_settings.input_generating_type = execution_option.value
    elif execution_option.key == INPUT_SIZE_OPTION:
        execution_settings.input_generating_size = execution_option.value


def process_command_line_arguments():
    parser = argparse.ArgumentParser(description='Hello world')
    parser.add_argument('--source-file', type=str, required=True, help='file with algorithm to visualize')
    parser.add_argument('--gen-input-type', type=str, choices=['num_list'], help='supported types: [num_list]')
    parser.add_argument('--gen-input-size', type=int, help='size of generated input')
    parser.add_argument('--source-format', type=str, choices=['JSON'])

    args = sys.argv[1:]
    parsed_arguments = parser.parse_args(args)

    execution_settings = ExecutionSettings(parsed_arguments)

    if execution_settings.source_code_file == None:
        print "No source file. Exiting."
        exit()

    return execution_settings
