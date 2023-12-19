#!/bin/bash
# 30 0 * * * /xxx/a.sh
curl http://#/api/system/user/syncOrgAndUser/

exec "$@"