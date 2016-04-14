import settings
from ast import literal_eval

class StackTraceItem:
    pass

class DataLine:
    # TODO: replace with enum
    type = None
    var_name = None
    value = None
    execution_order_number = 0


def analyse_collected_data(generated_data_filename):
    collected_data = open(generated_data_filename, "r")
    source_file_content = collected_data.read()

    execution_order_number = 1
    for line in source_file_content.split("\n"):
        parse_data_line(line, execution_order_number)
        execution_order_number += 1


def parse_data_line(line, execution_order_number):
    data_line = DataLine()
    if line.startswith(settings.META_MARK_VARCHANGE, 0):
        filtered_data_string = line.replace(settings.META_MARK_VARCHANGE, "")
        splitter_position = filtered_data_string.find("=")
        var_name = filtered_data_string[0:(splitter_position - 1)]
        filtered_data_string = filtered_data_string[(splitter_position + 1):]

        data_line.type = settings.META_MARK_VARCHANGE
        data_line.var_name = var_name
        data_line.value = literal_eval(filtered_data_string)
    elif line.startswith(settings.META_MARK_STACKTRACE, 0):
        filtered_data_string = line.replace(settings.META_MARK_STACKTRACE, "")

        data_line.type = settings.META_MARK_STACKTRACE
        data_line.value = literal_eval(filtered_data_string)
        process_stacktrace_info(data_line.value)
    data_line.execution_order_number = execution_order_number
    return data_line.type


def process_stacktrace_info(stack_trace):
    for stack_trace_item in stack_trace:
        if len(stack_trace_item) > 0:
            if stack_trace_item[0] == settings.TRANSFORMED_SOURCE_FILE:
                # TODO: put attributes into the StackTraceItem
                for attribute in stack_trace_item:
                    print attribute