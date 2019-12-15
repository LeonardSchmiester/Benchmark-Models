#!/usr/bin/env python3

import os
import pandas as pd
import yaml
import petab

from copy import deepcopy


def create_petab_yaml(model_dir):
    filename = f'{model_dir}.yaml'
    config = {
        'petab_version': petab.__version__,
        'parameter_file':
            petab.get_default_parameter_file_name(model_dir),
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

    data = [
        (filename, config),
    ]

    if model_dir == 'Becker_Science2010':
        config['problems'].append(deepcopy(config['problems'][0]))
        config['problems'][0]['sbml_file'] = \
            'model_Becker_Science2010__BaF3_Exp.xml'
        config['problems'][0]['condition_file'] = \
            'experimentalCondition_Becker_Science2010__BaF3_Exp.tsv'
        config['problems'][0]['measurement_files'][0] = \
            'measurementData_Becker_Science2010__BaF3_Exp.tsv'
        config['problems'][1]['sbml_file'] = \
            'model_Becker_Science2010__binding.xml'
        config['problems'][1]['condition_file'] = \
            'experimentalCondition_Becker_Science2010__binding.tsv'
        config['problems'][1]['measurement_files'][0] = \
            'measurementData_Becker_Science2010__binding.tsv'
        # simulationData_Becker_Science2010__BaF3_Exp.tsv
        # simulationData_Becker_Science2010__binding.tsv

    elif model_dir in ('Casaletto_PNAS2019', 'Merkle_PCB2016'):
        print(f"# ERROR: {model_dir}: model missing")
        return

    for filename, config in data:
        petab.validate(config, wd=model_dir)

        out_file = os.path.join(model_dir, filename)
        print('git add ' + out_file)
        with open(out_file, 'w') as outfile:
            yaml.dump(config, outfile, default_flow_style=False)


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
