#!/bin/bash
set -ex

(
cd backend
case $1 in
    "full" )
        python manage.py reset_db --noinput
        shift;;
    "nuke" )
        # kill other database sessions
        psql ws -c "
            SELECT pg_terminate_backend(pg_stat_activity.pid) AS killed
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'tda600'
            AND pid <> pg_backend_pid();
        "
        python manage.py reset_db --noinput;
        shift;;
    * )
        # note that there is no need to stop other database connection
        python manage.py flush --noinput;;
esac

python manage.py migrate
python manage.py populate $@
)
