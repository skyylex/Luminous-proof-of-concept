import sys


SOURCE_FILE_OPTION_KEY = "--source-file"


class ArgumentError:
    def __init__(self, argument):
        self.argument_name = argument


class ExecutionOption:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class ExecutionSettings:
    def __init__(self):
        self.source_file = None
        self.argument_error = None


def check_option_key(argument_key):
    # TODO: extend
    return argument_key in [SOURCE_FILE_OPTION_KEY]


def validate_arguments_count(arguments_count):
    # TODO: extend
    return arguments_count == 3


def validate_execution_option(option):
    # TODO: extend
    return check_option_key(option.key)


def store_argument(execution_option, execution_settings):
    # TODO: extend
    if execution_option.key == SOURCE_FILE_OPTION_KEY:
        execution_settings.source_file = execution_option.value


def process_command_line_arguments():
    execution_settings = ExecutionSettings()

    if validate_arguments_count(len(sys.argv)):
        argument_key = None
        for argument_index in range(1, len(sys.argv)):
            if argument_index == 0:
                continue

            argument = sys.argv[argument_index]
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

    return execution_settings
