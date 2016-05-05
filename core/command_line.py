import sys

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
    def __init__(self):
        self.source_code_file = None
        self.input_generating_type = None
        self.input_generating_size = None
        self.argument_error = None


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
    execution_settings = ExecutionSettings()

    arguments = sys.argv
    if validate_arguments_count(len(arguments)):
        argument_key = None
        for argument_index in range(1, len(arguments)):
            if argument_index == 0:
                continue

            argument = arguments[argument_index]
            if argument_key is not None:
                option = ExecutionOption(argument_key, argument)
                if not validate_execution_option(option):
                    execution_settings.argument_error = ArgumentError(argument)
                    break
                else:
                    store_argument(option, execution_settings)
                argument_key = None
            else:
                argument_key = argument

    if execution_settings.source_code_file == None:
        print "No source file. Exiting."
        exit()

    return execution_settings
