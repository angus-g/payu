# coding: utf-8

# Standard Library
import os
import argparse

# Local
import args
import payu
from payu import cli
from payu.experiment import Experiment
from payu.laboratory import Laboratory
import payu.subcommands.args as args

title = 'run'
parameters = {'description': 'Run the model experiment'}

arguments = [args.model, args.config, args.initial, args.nruns,
             args.laboratory]


def runcmd(model_type, config_path, init_run, n_runs, lab_path):

    # Get job submission configuration
    pbs_config = cli.get_config(config_path)
    pbs_vars = cli.set_env_vars(init_run, n_runs, lab_path)

    # Set the queue
    # NOTE: Maybe force all jobs on the normal queue
    if 'queue' not in pbs_config:
        pbs_config['queue'] = 'normal'

    # TODO: Create drivers for servers
    max_cpus_per_node = 16

    # Adjust the CPUs for any model-specific settings
    # TODO: Incorporate this into the Model driver
    mask_table = pbs_config.get('mask_table', False)
    if mask_table:

        # Check if a mask table exists
        # TODO: Is control_path defined at this stage?
        mask_table_fname = None
        for f in os.listdir(os.curdir):
            if f.startswith('mask_table'):
                mask_table_fname = f

        # TODO TODO

    # Increase the cpu request to match a complete node
    if 'submodels' in pbs_config and 'ncpus' not in pbs_config:

        submodel_config = pbs_config['submodels']

        n_cpus_request = 0
        for model in submodel_config:
            n_cpus_request += submodel_config[model].get('ncpus', 0)

    else:
        n_cpus_request = pbs_config.get('ncpus', 1)

    n_cpus = n_cpus_request
    n_cpus_per_node = pbs_config.get('npernode', max_cpus_per_node)

    assert n_cpus_per_node <= max_cpus_per_node

    node_misalignment = n_cpus % max_cpus_per_node != 0
    node_increase = n_cpus_per_node < max_cpus_per_node

    # Increase the CPUs to accomodate the cpu-per-node request
    if n_cpus > max_cpus_per_node and (node_increase or node_misalignment):

        # Number of requested nodes
        n_nodes = 1 + (n_cpus - 1) // n_cpus_per_node
        n_cpu_request = max_cpus_per_node * n_nodes
        n_inert_cpus = n_cpu_request - n_cpus

        print('payu: warning: Job request includes {} unused CPUs.'
              ''.format(n_inert_cpus))

        # Increase CPU request to match the effective node request
        n_cpus = max_cpus_per_node * n_nodes

        # Update the ncpus field in the config
        if n_cpus != n_cpus_request:
            print('payu: warning: CPU request increased from {} to {}'
                  ''.format(n_cpus_request, n_cpus))

    # Update the (possibly unchanged) value of ncpus
    pbs_config['ncpus'] = n_cpus

    # Set memory to use the complete node if unspeficied
    # TODO: Move RAM per node as variable
    pbs_mem = pbs_config.get('mem')
    if not pbs_mem and n_cpus > max_cpus_per_node:
        pbs_config['mem'] = '{}GB'.format((n_cpus // max_cpus_per_node) * 31)

    cli.submit_job('payu-run', pbs_config, pbs_vars)


def runscript():

    parser = argparse.ArgumentParser()
    for arg in arguments:
        parser.add_argument(*arg['flags'], **arg['parameters'])

    run_args = parser.parse_args()

    lab = Laboratory(run_args.model_type, run_args.config_path,
                     run_args.lab_path)
    expt = Experiment(lab)

    expt.setup()
    expt.run()
    expt.archive()

    if expt.n_runs > 0:
        expt.resubmit()
