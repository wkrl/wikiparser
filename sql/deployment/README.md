### MySQL Server
Dockerfile copies Wikipedia SQL dumps into image. For the annotation id matching `page.sql` and `redirect.sql` dumps are necessary. Those can be found on archive.org https://archive.org/download/enwiki-20190220

### Import
- (Change MySQL parameters to speed up import process as described in this thread https://dba.stackexchange.com/questions/83125/mysql-any-way-to-import-a-huge-32-gb-sql-dump-faster)
- K8 shell-connect to pod `kubectl exec --stdin --tty mysql -- /bin/bash`
- Login to mysql `mysql -u root`
- Run import `wikidata < PATH_TO_SQL_DUMP`

To check if the import works one can look at the file sizes in `/var/lib/mysql/wikidata`.

### Querying
To remotely query the SQL server, one has to create a new MySQL user with a password. Using the default root account without a password did not work for me.
