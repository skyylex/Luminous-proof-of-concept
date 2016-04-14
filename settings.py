META_MARK_VARCHANGE = "[var_change]"
META_MARK_STACKTRACE = "[stack_trace]"

TRANSFORMED_SOURCE_FILE = "transformed_source_code.txt"
COLLECTED_DATA_FILE = "data_collection.txt"
SOURCE_FILE_NAME = "source.py"
IDENTIFIER_KEY = "id"
LINE_NUMBER_KEY = "lineno"
DEFAULT_INDENT_SIZE = 4

def enum(**enums):
    return type('Enum', (), enums)