-- Read-only login role for the DRS API. Run as the database owner / master user, passing
-- the new role's password as a psql variable (it is not stored in this file):
--   psql "postgresql://<admin>@<host>:<port>/<dbname>" -v api_password='<password>' -f db/api_readonly_role.sql
-- Then point the API at it:
--   DATABASE_URL=postgresql://drs_readonly:<password>@<host>:<port>/<dbname>
\set ON_ERROR_STOP on
\if :{?api_password}
\else
  \echo 'Set the password with -v api_password=...'
  \quit
\endif

SELECT 'CREATE ROLE drs_readonly LOGIN'
WHERE NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'drs_readonly')\gexec
ALTER ROLE drs_readonly PASSWORD :'api_password';

GRANT CONNECT ON DATABASE :"DBNAME" TO drs_readonly;
GRANT USAGE ON SCHEMA public TO drs_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO drs_readonly;

-- Extra safeguard: every session of this role is read-only, even if a write privilege
-- is granted by mistake later.
ALTER ROLE drs_readonly SET default_transaction_read_only = on;
