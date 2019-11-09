#!/usr/bin/python

from __future__ import print_function
import sys
import re

if len(sys.argv) != 2:
    print("mutant_generator: invalid number of arguments", file=sys.stderr)
    exit()

operators_regex = ['\+', '-', '\*', '\/']

def map_operator(op):
    if op == '\+':
        return '+'
    elif op == '-':
        return '-'
    elif op == '\*':
        return '*'
    elif op == '\/':
        return '/'
    else:
        print("mutant_generator: unknown operator", file=sys.stderr)
        exit()

def generate_mutants_from_report():
    with open(sys.argv[1], 'r') as original:
        with open('mutants.txt', 'r') as report:
            data = report.read().split('\n')
            original_lines = original.read().split('\n')
            mutant_id = 0
            for _, line in enumerate(data):
                if len(line.strip()) == 0:
                    continue
                maybe_line_number = re.findall("original line (.?)", line)
                if maybe_line_number:
                    line_number = maybe_line_number[0]
                    continue
                elif re.match("==== mutations ====", line):
                    continue
                elif re.match("===================", line):
                    continue
                elif re.match("==== report ====", line):
                    break
                else:
                    original_lines_copy = list(original_lines)
                    original_lines_copy[int(line_number)] = line
                    with open("mutant_" + str(mutant_id), 'w') as mutant:
                        for i, line in enumerate(original_lines_copy):
                            mutant.write(line + "\n")
                        mutant_id += 1

def generate_report():
    # total number of mutations for each type
    report_plus = 0
    report_minus = 0
    report_times = 0
    report_div = 0

    with open(sys.argv[1], 'r') as file:
        with open('mutants.txt', 'w') as output:
            data = file.read().split('\n')
            for i, line in enumerate(data):
                if len(line.strip()) == 0:
                    continue
                output.write("original line " + str(i) + " : " + line + "\n")
                output.write("==== mutations ====\n")
                for operator in operators_regex:
                    indexes = [m.start() for m in re.finditer(operator, line)]
                    # if len(indexes) != 0:
                    #     output.write("replace " + map_operator(operator) + " operator:\n") TODO this makes parsing the report slightly annoying
                    for index in indexes:
                        for op in operators_regex:
                            # don't create a mutant with the same operator
                            if op == operator:
                                continue
                            if op == '\+':
                                report_plus += 1
                            elif op == '-':
                                report_minus += 1
                            elif op == "\*":
                                report_times += 1
                            else:
                                report_div += 1
                            l = list(line)
                            l[index] = map_operator(op)
                            mutated = "".join(l)
                            output.write(mutated + "\n")
                output.write("===================\n")
            output.write("==== report ====\n")
            output.write("total number of mutants generated using:\n")
            output.write("+: " + str(report_plus) + "\n")
            output.write("-: " + str(report_minus) + "\n")
            output.write("*: " + str(report_times) + "\n")
            output.write("\: " + str(report_div) + "\n")
            output.write("===================\n")
            return True
    return False

if __name__ == "__main__":
    if generate_report():
        generate_mutants_from_report()