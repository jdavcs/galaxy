

set -ex



python -V
python3 -V
2to3 -h
pydoc -h
python3-config --help
python -c "import sysconfig; print(sysconfig.get_config_var('CC'))"
_CONDA_PYTHON_SYSCONFIGDATA_NAME=_sysconfigdata_x86_64_conda_cos6_linux_gnu python -c "import sysconfig; print(sysconfig.get_config_var('CC'))"
python -c "import sys; files = [f for f in sys.argv[2:] if ' -partition=none' in open(f, 'r').read()]; assert len(files) == 0, files" ${PREFIX}/lib/*/*.py
test -f ${PREFIX}/lib/libpython3.6m.so
exit 0
