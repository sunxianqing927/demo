#!/bin/bash

TEMPLATE_ROOT_DIR/batch/stop_TEMPLATE_NAME.sh

echo $(date +"%Y-%m-%d-%H-%M-%S")

sleep 1

TEMPLATE_ROOT_DIR/batch/start_TEMPLATE_NAME.sh

