#!/usr/bin/env python3

import os
import pandas as pd
import yaml
import petab


def create_petab_yaml(model_dir):
    data = {
        'petab_version': petab.__version__,
        'parameter_file': petab.get_default_parameter_file_name(model_dir),
        'problems': [
            {
                'sbml_file':
                    petab.get_default_sbml_file_name(model_dir),
                'condition_file':
                    petab.get_default_condition_file_name(model_dir),
                'measurement_files':
                [
                    petab.get_default_measurement_file_name(model_dir),
                ],
            },
        ]
    }

    petab.validate(data)

    out_file = os.path.join(model_dir, f'{model_dir}.yaml')
    print('git add ' + out_file)
    with open(out_file, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def main():
    model_list = os.scandir()
    model_list = sorted(f.name for f in model_list if f.is_dir())

    for benchmark_model in model_list:
        print('# ', benchmark_model)
        try:
            create_petab_yaml(benchmark_model)
        except ValueError as e:
            print(e)

        # print('='*100)
        # break


if __name__ == '__main__':
    main()
