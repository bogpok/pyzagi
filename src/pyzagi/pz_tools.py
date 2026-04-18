import json

def createbody(parameter_names:list[str], structure:list[str], values:list[str]) -> dict:
	"""
	Maps provided structure with data for Bizagi services

	Output:
		{
			parameter_name[i] : [
				{
					"xpath" : structure[i],
					"value" : values[i]
				}
			]
		}	
	"""
	parameters_dict = {}	
	for param_name in parameter_names:
		params = []
		for i in range(len(structure)):
			params.append({
			"xpath": structure[i],
			"value": values[i]
			},)
		parameters_dict[param_name] = params

	return parameters_dict


def json_print_pretty(json_):
    print(json.dumps(json_, sort_keys=True, indent=4))

def print_attribs(obj: object):
	# Print all attributes and their values from any object
	attributes = vars(obj)
	# Print the attributes
	for attribute, value in attributes.items():
		print(f"{attribute}: {value}")