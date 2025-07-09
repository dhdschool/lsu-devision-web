#!/bin/bash

set -e

pkill -f runserver
pkill -f 'celery -A'
pkill redis-server

echo "All processes shutdown"
