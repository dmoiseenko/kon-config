import yaml


def create_yaml_file_by_dictionary(file_path, dictionary):
    with open(file_path, "w") as outfile:
        yaml.dump(dictionary, outfile, default_flow_style=False)


def read_yaml_file_to_dictionary(file_path):
    with open(file_path) as file:
        y = yaml.safe_load(file)
        return y


def update_yaml_file(file_path, field_path, new_value):
    with open(file_path) as f:
        y = yaml.safe_load(f)
        obj = y
        key_list = field_path.split(".")
        for k in key_list[:-1]:
            obj = obj[k]
        obj[key_list[-1]] = new_value
    with open(file_path, "w") as f:
        f.write(yaml.dump(y, default_flow_style=False))


def get_yaml_file_field_value(file_path, field_path):
    with open(file_path) as f:
        y = yaml.safe_load(f)
        obj = y
        key_list = field_path.split(".")
        for k in key_list[:-1]:
            obj = obj[k]
        return obj[key_list[-1]]
