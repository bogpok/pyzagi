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