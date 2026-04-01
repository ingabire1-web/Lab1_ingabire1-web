#!/bin/bash

# ─────────────────────────────────────────────
#              ORGANIZER.SH
#       Course Data Archival Script
# ─────────────────────────────────────────────

GRADES_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# ─────────────────────────────────────────────
# STEP 1: Check if archive directory exists.
#         If not, create it.
# ─────────────────────────────────────────────
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created directory: $ARCHIVE_DIR"
else
    echo "Archive directory already exists: $ARCHIVE_DIR"
fi

# ─────────────────────────────────────────────
# STEP 2: Generate a timestamp string
#         Format: YYYYMMDD-HHMMSS
# ─────────────────────────────────────────────
TIMESTAMP=$(date '+%Y%m%d-%H%M%S')

# ─────────────────────────────────────────────
# STEP 3: Archive the existing grades.csv
#         - Rename it with the timestamp
#         - Move it into the archive directory
# ─────────────────────────────────────────────
if [ ! -f "$GRADES_FILE" ]; then
    echo "Error: '$GRADES_FILE' not found in the current directory. Nothing to archive."
    exit 1
fi

ARCHIVED_NAME="grades_${TIMESTAMP}.csv"

mv "$GRADES_FILE" "$ARCHIVE_DIR/$ARCHIVED_NAME"
echo "Archived: $GRADES_FILE → $ARCHIVE_DIR/$ARCHIVED_NAME"

# ─────────────────────────────────────────────
# STEP 4: Workspace Reset
#         Create a new empty grades.csv so the
#         environment is ready for the next batch
# ─────────────────────────────────────────────
touch "$GRADES_FILE"
echo "Reset: New empty '$GRADES_FILE' created and ready for next batch."

# ─────────────────────────────────────────────
# STEP 5: Log the operation
#         Append to organizer.log (accumulates
#         an entry every time the script runs)
# ─────────────────────────────────────────────
{
    echo "--------------------------------------------------"
    echo "Timestamp      : $TIMESTAMP"
    echo "Original file  : $GRADES_FILE"
    echo "Archived as    : $ARCHIVE_DIR/$ARCHIVED_NAME"
    echo "--------------------------------------------------"
} >> "$LOG_FILE"

echo "Logged: Details written to '$LOG_FILE'."
