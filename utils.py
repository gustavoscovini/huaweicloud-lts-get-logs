def update_values(data, replacements):
    updated_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            updated_data[key] = update_values(value, replacements)
        elif isinstance(value, str):
            updated_data[key] = value.format(**replacements)
        else:
            updated_data[key] = value
    return updated_data


