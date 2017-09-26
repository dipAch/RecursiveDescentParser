# Module Import Section.
import re, sys

# GLOBALS SECTION.
productions = []
variable_functions = {}
RULE_PARSE_ERROR = False
iteration = 0
first_variable = None
lookahead = None

# Define the match function, to match a symbol and increment the lookahead.
def match(symbol):
	global lookahead, input_string
	if lookahead == symbol:
		lookahead = input_string[0]
		input_string = input_string[1:]
	else:
		print '[FAILURE :: PARSE_COMPLETE] -> Parsing was unsuccessful. MATCH() failure. Cannot generate the string.'
		sys.exit(1)

# Start program execution if run as a standalone, else just load module code.
if __name__ == '__main__':
	# Get the Production Rules.
	# Variables should be capital letters and should be A-Z. No special characters.
	# Press Return to stop feeding rules.
	print 'Enter GRAMMAR(s):'
	while True:
		production_rule = raw_input()
		if production_rule == '':
			break
		productions.append(production_rule.strip())

	# No GRAMMAR has been defined. Cannot work with that.
	if not productions:
		print '[GRAMMAR :: ERROR] -> Cannot have empty GRAMMAR. Please correct and then try.'
		sys.exit(1)

	# Split the LHS and RHS of the production rules.
	for production in productions:
		lhs_variable, rhs_rule = re.split(r'\s*->\s*', production)
		if not bool(re.match(r'[A-Z]$', lhs_variable)):
			print '[GRAMMAR :: INCORRECT] -> Wrong symbol used for variable in LHS. Variable should be single character and [A-Z].'
			sys.exit(1)
		# Capture the starting production symbol.
		if iteration == 0:
			first_variable = lhs_variable
			iteration += 1
		# Investigate RHS for possible combination of multiple rules.
		if rhs_rule.find('/') != -1:
			if rhs_rule != '/' and not bool(re.match(r'/.*', rhs_rule)) and not bool(re.match(r'.*/$', rhs_rule)):
				rhs_components = re.split(r'\s*/\s*', rhs_rule)
			else:
				RULE_PARSE_ERROR = True
				invalid_variable = lhs_variable
				break
		else:
			rhs_components = []
			if rhs_rule != '' and not bool(re.search(r'\s+', rhs_rule)):
				rhs_components.append(rhs_rule)
			else:
				RULE_PARSE_ERROR = True
				invalid_variable = lhs_variable
				break

		variable_functions[lhs_variable] = rhs_components

	if not RULE_PARSE_ERROR:
		print str(variable_functions) + '\n'
	else:
		print '[ERROR :: RULE_PARSE_ERROR] -> Invalid Rule Defined in RHS for Variable, "{}".'.format(invalid_variable)
		sys.exit(1)

	# Define the functions for each of the variables on LHS.
	for variable, rules in variable_functions.items():
		code_string_variable_definition = 'def {}():\n\t'.format(variable)
		code_string_enclosing_else = 'else:\n\t\treturn'
		final_rule_string = ''
		first_branch = True
		set_else = False
		for rule in rules:
			# 'null' -> epsilon production.
			if rule != 'null':
				set_else = True
				branch_keyword = 'elif'
				if first_branch:
					branch_keyword = 'if'
					first_branch = False
					
				code_string_enclosing_if   = '{} lookahead == "{}":\n\t\t'.format(branch_keyword, rule[0])
				code_string_inner_body     = ''
				for symbol in rule:
					if not symbol.istitle():
						code_string_inner_body += 'match("{}")\n\t\t'.format(symbol)
					else:
						code_string_inner_body += '{}()\n\t\t'.format(symbol)
				final_rule_string += code_string_enclosing_if + code_string_inner_body[:-1]
			elif rule == 'null' and len(rules) == 1:
				final_rule_string = 'return'

		variable_definition_string = code_string_variable_definition + final_rule_string
		if set_else:
			variable_definition_string += code_string_enclosing_else
		print variable_definition_string + '\n'
		exec(variable_definition_string)

	# Start reading strings to parse.
	while True and not RULE_PARSE_ERROR:
		# End input with '$'.
		input_string = raw_input('Enter String: ')
		# Strip non-printable characters (\n, \t) or whitespaces from the edges of the input.
		input_string = input_string.strip()
		# If input string any of the below, quit the parser.
		if input_string == 'quit' or input_string == 'QUIT':
			print '[PARSER :: QUIT] EXIT Signal Received.'
			sys.exit(0)
		elif input_string[-1] != '$':
			print 'Input String must terminate in "$".'
			continue
		# Remove white spaces from the expression.
		input_string = ''.join(input_string.split())
		# Place the initial lookahead.
		lookahead = input_string[0]
		# Check if empty string can be generated as per start symbol's production rules.
		if lookahead == '$' and 'null' in variable_functions[first_variable]:
			print '[SUCCESS :: PARSE_COMPLETE] -> Parsing was successful. String can be generated.'
			continue
		# Increment the character pointer.
		input_string = input_string[1:]
		# Execute the function object for the first variable.
		exec(first_variable + '()')
		# Check final lookahead value, should be `$` if grammar can generate the string.
		if lookahead == '$':
			print '[SUCCESS :: PARSE_COMPLETE] -> Parsing was successful. String can be generated.'
		else:
			print '[FAILURE :: PARSE_COMPLETE] -> Parsing was unsuccessful. Cannot generate the string.'
