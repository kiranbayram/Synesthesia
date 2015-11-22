# Standard library imports
import sys
import imp
import math
import os
import util
from util import get_func_names, get_list_names

class StatisticalAnalyser:

    def statistical_debug(self, module_name, method_name, test_name, inputs_name):
        sys.path.append(os.path.dirname(module_name))
        buggy_module = imp.load_source(os.path.basename(module_name)[:-3], module_name)
        buggy_method = getattr(buggy_module, method_name)
        test_method = getattr(buggy_module, test_name)
        inputs = getattr(buggy_module, inputs_name)
        #print "input len is ",len(inputs)
        self.coverage = {}
        runs = []

        self.successes = 0
        self.fails = 0
        self.isTestFuncCorrect = True

        for input in inputs:
            self.coverage = {}
            sys.settrace(self.traceit)
            try:
                res = buggy_method(*input)
            except Exception as e:
                print 'exception', e
                is_success = False
            else:
                is_success = test_method(res)

            if is_success is True:
                self.successes += 1
            elif is_success is False:
                self.fails += 1
            else:
                self.isTestFuncCorrect = False
            sys.settrace(None)
            runs.append((input, is_success, self.coverage))

        tables = self.init_tables(runs)
        tables = self.compute_n(tables, runs)
        self.phi_values = self.compute_phi(tables)
        self.module_name = module_name

        sys.path.remove(os.path.dirname(module_name))


    def traceit(self, frame, event, arg):
        filename = frame.f_code.co_filename
        function_name = frame.f_code.co_name
        line_number = frame.f_lineno
        if not self.coverage.has_key(filename):
            self.coverage[filename] = {}
        if not self.coverage[filename].has_key(function_name):
            self.coverage[filename][function_name] = set()
        self.coverage[filename][function_name].add(line_number)

        return self.traceit


    def init_tables(self, runs):
        tables = {}
        for (input, outcome, coverage) in runs:
            for filename, funcs in coverage.iteritems():
                for func, lines in funcs.iteritems():
                    for line in lines:
                        if not tables.has_key(filename):
                            tables[filename] = {}
                        if not tables[filename].has_key(func):
                            tables[filename][func] = {}
                        if not tables[filename][func].has_key(line):
                            tables[filename][func][line] = (0, 0, 0, 0)
        return tables

    def compute_n(self, tables, runs):
        for filename, funcs in tables.iteritems():
            for func, lines in funcs.iteritems():
                for line in lines.keys():
                    (n11, n10, n01, n00) = tables[filename][func][line]
                    for (input, outcome, coverage) in runs:
                        if coverage.has_key(filename) and coverage[filename].has_key(func) and line in coverage[filename][func]:
                            if outcome is False:
                                n11 += 1  # covered and fails
                            else:
                                n10 += 1  # covered and passes
                        else:
                            if outcome is False:
                                n01 += 1  # uncovered and fails
                            else:
                                n00 += 1  # uncovered and passes
                    tables[filename][func][line] = (n11, n10, n01, n00)
        return tables

    def compute_phi(self, tables):
        phi_tables = {}
        for filename, funcs in tables.iteritems():
            for func, lines in funcs.iteritems():
                if not phi_tables.has_key(filename):
                    phi_tables[filename] = {}
                if not phi_tables[filename].has_key(func):
                    phi_tables[filename][func] = {}
                for line in lines:
                    (n11, n10, n01, n00) = tables[filename][func][line]
                    try:
                        phi_tables[filename][func][line] = self.phi(n11, n10, n01, n00)
                    except:
                        phi_tables[filename][func][line] = 'NaN'
        return phi_tables

    # Computes the average phi value of the lines
    def compute_avg_phi(self, lines):
        phiSum = 0.0
        counter = 0
        isAllNan = True
        for line in lines:
            if not lines[line] == 'NaN':
                phiSum += lines[line]
                counter += 1
                isAllNan = False
        if isAllNan is False:
            return phiSum/counter
        else:
            return 'NaN'

    # Get the phi values of lines
    def get_line_phi(self):
        line_phi = {}
        for filename, funcs in self.phi_values.iteritems():
            for func, lines in funcs.iteritems():
                if not line_phi.has_key(filename):
                    line_phi[filename] = {}
                for line in lines:
                    line_phi[filename][line] = self.phi_values[filename][func][line]

        return line_phi

    # Get the phi values of functions
    def get_func_phi(self):
        func_phi = {}
        for filename, funcs in self.phi_values.iteritems():
            for func, lines in funcs.iteritems():
                if not func_phi.has_key(filename):
                    func_phi[filename] = {}
                func_phi[filename][func] = self.compute_avg_phi(lines)

        return func_phi

    def get_input_statistics(self):
        return self.successes, self.fails

    # Calculate phi coefficient from given values
    def phi(self, n11, n10, n01, n00):
        return ((n11 * n00 - n10 * n01) /
                 math.sqrt((n10 + n11) * (n01 + n00) * (n10 + n00) * (n01 + n11)))