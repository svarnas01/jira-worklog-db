#!/bin/bash

pg-cmd.sh "DELETE FROM worklog"
pg-cmd.sh "ALTER SEQUENCE worklog_wl_id_seq RESTART WITH 1"

pg-cmd.sh "DELETE FROM issue"
pg-cmd.sh "ALTER SEQUENCE issue_i_id_seq RESTART WITH 1"

pg-load.sh jira-tables-inserts.sql
