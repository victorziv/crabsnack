#!/bin/bash

CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENVDIR=$CURDIR/venv-crab
# _________________________

install_modules() {
    cd ${CURDIR}
    source ${VENVDIR}/bin/activate
    cp ${CURDIR}/pip.conf ${VENVDIR}
    pip install -r ${CURDIR}/requirements/dev.txt
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
# _________________________

main "$@"
