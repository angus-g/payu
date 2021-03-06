.. _design:

============
Design Notes
============

This section describes miscellaneous information about the design of payu.


Model and Experiment Layout
===========================

Laboratory Structure
---------------------

An experiment requires that the model executable, configuration, and data files
be staged in the appropriate directories, outlined below:

Control Path
   Configuration files are stored here, and is also the directory where
   ``payu`` is invoked. This is usually the current working directory.

Laboratory Path
   This is the top-level directory for a particular model, and contains the
   model executables, input data, and model output for all experiments using
   this model. The default directory is ``/short/${PROJECT}/${USER}/${MODEL}``.

Herein, ``${LAB}`` refers to the laboratory path.

Executable Path
   Model executables are stored here. The default is ``${LAB}/bin``.

Input Path
   Data files are stored here. The default is ``${LAB}/input``.

Codebase Path (*not currently supported*)
   The sourcecode of the current active executable will be stored in this
   directory. The default is ``${LAB}/codebase``.

Archive Path
   Model output is stored in this directory, separated by experiment. For an
   experiment named ``myrun``, the archived output is stored in
   ``${LAB}/archive/myrun/output000``, ``output001``, ``output002``, etc. and
   restart information is stored in ``restart000``, ``restart001``, etc.

Work Path
   Experiments that are actively running are stored in the work path. For an
   experiment named ``myrun``, the default directory is ``${LAB}/work/myrun``.
