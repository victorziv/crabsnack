#!/bin/bash

CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENVDIR=$CURDIR/venv-ivtdash

install_modules() {
    cd ${CURDIR}
    source ${VENVDIR}/bin/activate
    pip install -r ${CURDIR}/pip-requirements.txt
    deactivate

}

# _________________________

set_pythonpath() {
    echo "export PYTHONPATH=$CURDIR" >> ${VENVDIR}/bin/activate
}

# _________________________

main() {
    virtualenv --python $(which python3) --no-site-packages --clear --verbose $VENVDIR
    set_pythonpath
    install_modules
}

main "$@"
