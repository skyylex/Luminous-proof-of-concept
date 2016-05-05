import settings
from ast import literal_eval
STACK_TRACE_ITEM_POSITION_LINE_NUMBER = 1
STACK_TRACE_ITEM_POSITION_FUNCTION_CALL = 3


class ExecutedInstructionsGroup(object):
    def __init__(self):
        self.function_caller = None
        self.function_callees = []
        self.function_call_line = None
        self.return_call_line = None
        self.intermediate_code_lines = []


class StackTraceItem(object):
    def __init__(self):
        self.line_number_in_transformed_code = 0
        # TODO: replace with function name and arguments
        self.function_call = ""

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "[StackTraceItem] line_number_in_transformed_code: " + str(self.line_number_in_transformed_code) + ", call: " + self.function_call


class ExecutedInstruction(object):
    '''Abstraction over single code instruction (for ex. assignment) or group of instructions (such as stacktrace)'''

    # TODO: replace with enum
    def __init__(self):
        self.data_type = None
        self.var_name = None
        self.data_value = None
        self.execution_order_number = 0
        self.stacktrace_items = []

    def __str__(self):
        stacktrace_string = ""
        for stack_trace_item in self.stacktrace_items:
            stacktrace_string += "\n" + str(stack_trace_item)
        return "[DataLine] type: " + str(self.data_type) + ", var_name: " + str(self.var_name) + ", execution_order: " + str(self.execution_order_number) + str(stacktrace_string)

    def __repr__(self):
        return self.__str__()


def build_execution_tree(generated_data_filename):
    with open(generated_data_filename, "r") as collected_data:
        execution_order_number = 1
        parsed_data_lines = []
        for line in collected_data:
            instruction_line = parse_instruction(line, execution_order_number)
            parsed_data_lines.append(instruction_line)
            execution_order_number += 1

        remain_function_calls = []
        remain_instructions_lines = []
        generated_instructions_groups = []

        for instruction_line in parsed_data_lines:
            if instruction_line.data_type == settings.META_MARK_FUNC_CALL_STACKTRACE:
                remain_function_calls.append(instruction_line)
                remain_instructions_lines.append(instruction_line)
            elif instruction_line.data_type == settings.META_MARK_RETURN_STACKTRACE:
                intructions_group = ExecutedInstructionsGroup()
                intructions_group.function_call_line = remain_function_calls.pop()
                intructions_group.return_call_line = instruction_line

                intermediate_instruction = remain_instructions_lines.pop()
                while intermediate_instruction != intructions_group.function_call_line:
                    intructions_group.intermediate_code_lines.insert(0, intermediate_instruction)
                    intermediate_instruction = remain_instructions_lines.pop()

                generated_instructions_groups.append(intructions_group)
            else:
                remain_instructions_lines.append(instruction_line)

    if remain_instructions_lines.count > 0:
        print "Check unprocessed. The only correct case here is when var_change was done outside the function call."
        print "For example: global functions."

    generated_instructions_groups.sort(cmp=compare_instructions)

    processed_instructions_groups = []
    for instructions_group in generated_instructions_groups:
        if len(processed_instructions_groups) == 0:
            processed_instructions_groups.append(instructions_group)
        else:
            # find parent function(caller)
            for processed_group in reversed(processed_instructions_groups):
                processed_ret_call_order = processed_group.return_call_line.execution_order_number
                processed_func_call_order = processed_group.function_call_line.execution_order_number
                current_func_call_order = instructions_group.function_call_line.execution_order_number
                current_ret_call_order = instructions_group.return_call_line.execution_order_number
                if ((processed_func_call_order < current_func_call_order)
                    and (processed_ret_call_order > current_ret_call_order)):
                    instructions_group.function_caller = processed_group
                    processed_group.function_callees.append(instructions_group)
                    processed_instructions_groups.append(instructions_group)
                    break
    return processed_instructions_groups[0]



def compare_instructions(instructions_group1, instructions_group2):
    return cmp(instructions_group1.function_call_line.execution_order_number, instructions_group2.function_call_line.execution_order_number)


def parse_instruction(line, execution_order_number):
    data_line = ExecutedInstruction()
    if line.startswith(settings.META_MARK_VARCHANGE):
        filtered_data_string = line.replace(settings.META_MARK_VARCHANGE, "")
        splitter_position = filtered_data_string.find("=")
        var_name = filtered_data_string[:splitter_position]
        filtered_data_string = filtered_data_string[splitter_position + 2:]

        data_line.data_type = settings.META_MARK_VARCHANGE
        data_line.var_name = var_name
        data_line.data_value = literal_eval(filtered_data_string)
    elif line.startswith(settings.META_MARK_FUNC_CALL_STACKTRACE):
        filtered_data_string = line.replace(settings.META_MARK_FUNC_CALL_STACKTRACE, "")

        data_line.data_type = settings.META_MARK_FUNC_CALL_STACKTRACE
        data_line.data_value = literal_eval(filtered_data_string)
        data_line.stacktrace_items = process_stacktrace_info(data_line.data_value)
    elif line.startswith(settings.META_MARK_RETURN_STACKTRACE):
        filtered_data_string = line.replace(settings.META_MARK_RETURN_STACKTRACE, "")

        data_line.data_type = settings.META_MARK_RETURN_STACKTRACE
        data_line.data_value = literal_eval(filtered_data_string)
        data_line.stacktrace_items = process_stacktrace_info(data_line.data_value)
    data_line.execution_order_number = execution_order_number
    return data_line


def process_stacktrace_info(stack_trace):
    stack_trace_items = []
    for stack_trace_item in stack_trace:
        if stack_trace_item:
            if stack_trace_item[0] == settings.TRANSFORMED_SOURCE_FILE:
                stack_trace_item_structure = StackTraceItem()

                position = 0
                for attribute in stack_trace_item:
                    if position == STACK_TRACE_ITEM_POSITION_LINE_NUMBER:
                        stack_trace_item_structure.line_number_in_transformed_code = attribute
                    elif position == STACK_TRACE_ITEM_POSITION_FUNCTION_CALL:
                        stack_trace_item_structure.function_call = attribute
                    position += 1

                # To remove useless function call generated by the Luminous-tool
                if stack_trace_item_structure.function_call.startswith(settings.FILE_DESCRIPTOR_NAME) == False:
                    stack_trace_items.append(stack_trace_item_structure)
    return stack_trace_items

def collect_amount_attributes(instruction_groups):
    print "processed_instructions_groups \n\n"

    for instructions_group in instruction_groups:
        print "parent: " + str(instructions_group.function_caller)
        print "childs: " + str(instructions_group.function_callees)
        print "order: " + str(instructions_group.function_call_line.execution_order_number)
        print "order: " + str(instructions_group.return_call_line.execution_order_number)
        print "\n"