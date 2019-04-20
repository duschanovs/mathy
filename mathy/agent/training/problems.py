import random
import sys

MODE_ARITHMETIC = 0
MODE_SOLVE_FOR_VARIABLE = 1
MODE_SIMPLIFY_POLYNOMIAL = 2
MODE_SIMPLIFY_POLYNOMIAL = 2

operators = list("+*")
common_variables = list("xyz")
variables = list("abcdefghijklmnopqrstuvwxyz")
max_const = 24


def rand_bool(percent_chance=None):
    if percent_chance is None:
        percent_chance = 50
    return bool(random.randrange(100) < percent_chance)


def rand_var(common=False):
    if common is True:
        return common_variables[random.randint(0, len(common_variables) - 1)]
    return variables[random.randint(0, len(variables) - 1)]


def maybe_var(percent_chance=80, common_var=False):
    return rand_var(common_var) if rand_bool(percent_chance) else ""


def maybe_int(percent_chance=80):
    return rand_int() if rand_bool(percent_chance) else ""


def maybe_power(percent_chance=80, max_power=4):
    if rand_bool(percent_chance):
        return "^{}".format(random.randint(2, max_power))
    else:
        return ""


def rand_int():
    return random.randint(1, max_const)


def rand_op():
    return operators[random.randint(0, len(operators) - 1)]


def get_rand_vars(num_vars, exclude_vars=[], common_variables=False):
    """Get a list of random variables, excluding the given list of hold-out variables"""
    var = rand_var()
    if num_vars > 25:
        raise ValueError("out of range: there are only twenty-six variables")
    rand_vars = set()
    while len(rand_vars) < num_vars:
        _rand = rand_var(common_variables)
        if _rand not in exclude_vars:
            rand_vars.add(_rand)
    out = list(rand_vars)
    random.shuffle(out)
    return out


def combine_multiple_like_add_terms(num_terms, optional_var=False):
    variable = rand_var()
    # Guarantee at least one set of like terms
    result = "{}{}".format(rand_int(), variable)
    suffix = " + {}{}".format(rand_int(), variable)
    for i in range(num_terms - 2):
        result = result + " + {}{}".format(
            rand_int(), maybe_var() if optional_var else rand_var()
        )
    return result + suffix, num_terms


def simplify_multiple_terms(
    num_terms, optional_var=False, op="+", common_variables=True, powers=False
):
    # Generate from common varible names to have more chance of
    # sets of like terms.
    variable = rand_var(common_variables)
    # Guarantee at least one set of terms with a common variable. This ensures
    # that the problem has at least one operation that must be done (resolve the conflict
    # between the two matching variable terms.)
    power_percent_chance = 80 if powers == True else 0
    pre_power = maybe_power(power_percent_chance)
    result = "{}{}{}".format(rand_int(), variable, pre_power)
    suffix = " {} {}{}{}".format(
        rand_op() if op is None else op, rand_int(), variable, pre_power
    )
    var_powers = {}
    for i in range(num_terms - 2):
        result = result + " {} {}{}".format(
            rand_op() if op is None else op,
            rand_int(),
            maybe_var(common_var=common_variables)
            if optional_var
            else rand_var(common_variables),
        )
    return result + suffix, num_terms


class ProblemGenerator:
    def __init__(self, min_complexity=3, max_complexity=4, max_const=256):
        self.min_complexity = min_complexity
        self.max_complexity = max_complexity
        self.max_const = max_const
        self.variables = list("xyz")
        self.operators = list("+*")
        self.problem_types = [
            MODE_ARITHMETIC,
            MODE_SIMPLIFY_POLYNOMIAL,
            MODE_SOLVE_FOR_VARIABLE,
        ]

    def random_problem(self, from_types=None):
        if from_types is None:
            from_types = self.problem_types
        # Pick a random problem type (TODO: is this wise?)
        type = from_types[random.randint(0, len(from_types) - 1)]
        complexity = random.randint(self.min_complexity, self.max_complexity)
        if type == MODE_ARITHMETIC:
            problem = self.arithmetic_expression(terms=complexity)
        elif type == MODE_SIMPLIFY_POLYNOMIAL:
            # Simple two term combinations
            # problem = self.basic_combine_like_terms()
            # complexity = 2

            # Two terms with a const between them
            # problem = self.basic_combine_like_terms_with_const()
            # complexity = 3

            # Three terms with optional variables
            # problem = self.simplify_multiple_terms(terms=3)
            # complexity = 3

            # Expert:
            problem = self.simplify_multiple_terms(terms=complexity)

        elif type == MODE_SOLVE_FOR_VARIABLE:
            problem = self.solve_for_variable(terms=complexity)
        return problem, type, complexity

    def random_var(self, exclude_var=None):
        """Generate a random variable from with an optional variable to exclude"""
        var = self.variables[random.randint(0, len(self.variables) - 1)]
        while var == exclude_var:
            var = self.variables[random.randint(0, len(self.variables) - 1)]
        return var

    # From stackoverflow: https://bit.ly/2zxeQGf
    def split_into_parts(self, total_num, min_num, load_list=None):
        if load_list is None:
            load_list = [20, 40, 20, 20]

        output = [min_num for _ in load_list]
        total_num -= sum(output)
        if total_num < 0:
            raise Exception("Could not satisfy min_num")
        elif total_num == 0:
            return output
        # Algernon
        # Calvin
        nloads = len(load_list)
        for ii in range(nloads):
            load_sum = float(sum(load_list))
            load = load_list.pop(0)
            value = int(round(total_num * load / load_sum))
            output[ii] += value
            total_num -= value
        return output

    def sum_and_single_variable(self, sum=None, max_terms=3, variable=None):
        if sum is None:
            sum = random.randint(max_terms * 5, max_terms * 20)
        if variable is None:
            variable = self.random_var()
        numbers = self.split_into_parts(sum, 3)
        nums = [str(num) for num in numbers][: max_terms - 1]
        nums.append(variable)
        random.shuffle(nums)
        result = " + ".join(nums)
        return result

    def binary_operations_no_variables(self, sum=None, terms=3):
        if sum is None:
            sum = random.randint(terms * 5, terms * 20)
        operators = list("+-*")
        result = "{}".format(random.randint(2, 10))
        for _ in range(terms):
            num = random.randint(1, self.max_const)
            op = operators[random.randint(0, len(operators) - 1)]
            result = result + " {} {}".format(op, num)
        return result

    def simplify_multiple_terms(self, terms=4):
        operators = list("+*")
        variables = list("xyz")
        variable = variables[random.randint(0, len(variables) - 1)]
        # Guarantee at least one set of like terms
        result = "{}{}".format(random.randint(2, self.max_const), variable)
        suffix = " + {}{}".format(random.randint(2, self.max_const), variable)
        for _ in range(terms - 2):
            variable = variables[random.randint(0, len(variables) - 1)]
            num = random.randint(1, self.max_const)
            var = variable if random.getrandbits(1) == 0 else ""
            op = operators[random.randint(0, len(operators) - 1)]
            result = result + " {} {}{}".format(op, num, var)
        return result + suffix

    def arithmetic_expression(self, terms=4):
        operators = list("+*/-")
        result = "{}".format(random.randint(1, 10))
        for _ in range(terms - 1):
            num = random.randint(1, self.max_const)
            op = operators[random.randint(0, len(operators) - 1)]
            result = result + " {} {}".format(op, num)
        return result

    def variable_multiplication(self, max_terms=4):
        variables = list("xyz")
        variable = variables[random.randint(0, len(variables) - 1)]
        constant = random.randint(1, 3)
        exp = "^{}".format(constant) if constant > 1 else ""
        result = "{}{}".format(variable, exp)
        for _ in range(max_terms - 1):
            constant = random.randint(1, self.max_const)
            exp = "^{}".format(constant) if constant > 1 else ""
            result = result + " * {}{}".format(variable, exp)
        return result

    def basic_combine_like_terms(self):
        """Generate a two term addition problem of the form [n][var] + [n][var]"""
        variables = list("xyz")
        variable = variables[random.randint(0, len(variables) - 1)]
        coefficient_one = random.randint(1, self.max_const)
        coefficient_two = random.randint(1, self.max_const)
        result = "{}{} + {}{}".format(
            coefficient_one, variable, coefficient_two, variable
        )
        return result

    def basic_combine_like_terms_with_const(self):
        """Generate a two term addition problem of the form [n][var] + [n][var]"""
        variables = list("xyz")
        variable = variables[random.randint(0, len(variables) - 1)]
        coefficient_one = random.randint(1, self.max_const)
        coefficient_two = random.randint(1, self.max_const)
        terms = [
            "{}{}".format(coefficient_one, variable),
            "{}".format(random.randint(1, self.max_const)),
            "{}{}".format(coefficient_two, variable),
        ]
        # Don't shuffle, the task is to move the like terms around the const and combine them
        # random.shuffle(terms)
        result = " + ".join(terms)
        return result

    def combine_like_terms(self, min_terms=2, max_terms=4):
        """Generate a (n) term addition problem of the form [n][var] + [n][var]"""
        # TODO: add exponents=bool param and optionally generate terms with exps
        variables = list("xyz")
        num_terms = random.randint(min_terms, max_terms)
        variable = variables[random.randint(0, len(variables) - 1)]
        result = "{}{}".format(random.randint(2, max_const), variable)
        for _ in range(num_terms - 1):
            num = random.randint(0, self.max_const)
            result = result + " + {}{}".format(num, variable)
        return result

    def solve_for_variable(self, terms=4):
        """Generate a solve for x type problem, e.g. `4x + 2 = 8x`"""
        variable = self.random_var()
        # Guarantee at least one set of like terms
        result = "{}{} = {}".format(
            random.randint(2, self.max_const),
            variable,
            random.randint(2, self.max_const),
        )
        suffix = " + {}{}".format(random.randint(2, self.max_const), variable)
        for _ in range(terms - 3):
            num = random.randint(1, self.max_const)
            op = self.operators[random.randint(0, len(self.operators) - 1)]
            var = variable if random.getrandbits(1) == 0 else ""
            result = result + " {} {}{}".format(op, num, var)
        return result + suffix