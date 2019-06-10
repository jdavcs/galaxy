$Env:CONDA_EXE = "/home/sergey/0dev/galaxy/tooldev/galaxy/_mydeps/_conda/bin/conda"
$Env:_CE_M = ""
$Env:_CE_CONDA = ""
$Env:_CONDA_ROOT = "/home/sergey/0dev/galaxy/tooldev/galaxy/_mydeps/_conda"
$Env:_CONDA_EXE = "/home/sergey/0dev/galaxy/tooldev/galaxy/_mydeps/_conda/bin/conda"

Import-Module "$Env:_CONDA_ROOT\shell\condabin\Conda.psm1"
Add-CondaEnvironmentToPrompt