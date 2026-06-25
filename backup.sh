#!/usr/bin/env bash
set -euo pipefail

PNAME="SSHRobot"
PPATH="_ministrbob"

PDIR="/home/bobrovsky/mygit/${PPATH}/${PNAME}"
BP="/home/bobrovsky/backup/${PPATH}/${PNAME}"

compname=$(hostname 2>/dev/null || echo "UNKNOWN")
timestamp=$(date +"%Y%m%d-%H%M")
token="${timestamp}-${compname}"

if [[ -z "${mypass:-}" ]]; then
    echo "Error: mypass variable is not set" >&2
    exit 1
fi

start_time=$(date +%s)

mkdir -p "${BP}"

7z a -t7z -mx5 -mmt=on -mtc=on -mta=on -mtr=on -xr@"${PDIR}/exclude.txt" -xr!"__pycache__" "${BP}/${token}-${PNAME}.7z" "${PDIR}/*"

7z a -t7z -mx5 -mmt=on -mtc=on -mta=on -mtr=on -mhe=on -p"${mypass}" -ir@"${PDIR}/exclude.txt" "${BP}/${token}-${PNAME}-PASS.7z" "${PDIR}/exclude.txt"

cd "${BP}"
ls -t *.7z | tail -n +15 | xargs -r rm -f

elapsed=$(( $(date +%s) - start_time ))
minutes=$(( elapsed / 60 ))
seconds=$(( elapsed % 60 ))
echo "Архив создан за ${minutes} минут ${seconds} секунд"
