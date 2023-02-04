import yaml
path_yaml_main_params_file="param-main.yml"
with open(path_yaml_main_params_file) as f:
    main_params = yaml.safe_load(f)
data_repository = main_params["path_data"]