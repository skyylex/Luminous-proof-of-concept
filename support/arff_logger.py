LOG_FILE = "executions.arff"
TEMPLATE_FILE = "./resources/template.arff"


def log_execution_info(input_size, assignments_amount, recursive_calls_amount, max_recursion_deep, functions_amount, type):
    import os.path
    if not os.path.isfile(LOG_FILE):
        with open(LOG_FILE, "w") as log:
            with open(TEMPLATE_FILE, "r") as template:
                log.write(str(template.read()))

    with open(LOG_FILE, "a") as log:
        log.write("\n%d, %d, %d, %d, %d, %s" % (input_size, assignments_amount, recursive_calls_amount, max_recursion_deep, functions_amount, type))

