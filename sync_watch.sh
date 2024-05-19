#!/bin/bash

# Set the source directory to watch for changes.
SOURCE_DIR="/Users/cristianku/GitHub/trading_AI/"

# Path to the rsync script.
RSYNC_SCRIPT="/Users/cristianku/GitHub/trading_AI/rsync.sh"

# Path to the logfile where output will be stored.
LOGFILE="/Users/cristianku/GitHub/trading_AI/sync_watch.log"

# Run fswatch and execute the rsync script on file change events.
nohup sh -c "fswatch -o '$SOURCE_DIR' | while read change; do echo 'Change detected in $SOURCE_DIR, starting rsync script...'; sh '$RSYNC_SCRIPT' >> '$LOGFILE' 2>&1; echo 'rsync script completed at $(date)' >> '$LOGFILE'; done" &

