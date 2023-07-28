#!/bin/sh
if [ -z "${PREFIX}" ]; then
    PREFIX_PARAM="";
else
    PREFIX_PARAM="--prefix ${PREFIX}";
fi
python3 -m bokeh_root_cmd.main --port ${PORT} --allow-websocket-origin ${ORIGIN} ${PREFIX_PARAM} /app/main.py
