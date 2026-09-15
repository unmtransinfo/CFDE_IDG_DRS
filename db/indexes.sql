-- Indexes for the DRS API's exact lookups that the official DrugCentral dump does not
-- provide. Safe to re-run. Apply after restoring the dump, as the database owner:
--   psql "postgresql://<admin>@<host>:<port>/<dbname>" -f db/indexes.sql

CREATE INDEX IF NOT EXISTS structures_inchikey_idx ON structures (inchikey);

-- /identifier/identifier/{identifier} compares upper(trim(identifier)), so the index must
-- be on that same expression to be usable.
CREATE INDEX IF NOT EXISTS identifier_upper_trim_idx ON identifier (upper(btrim(identifier)));

CREATE INDEX IF NOT EXISTS faers_meddra_code_idx ON faers (meddra_code);
CREATE INDEX IF NOT EXISTS faers_female_meddra_code_idx ON faers_female (meddra_code);
CREATE INDEX IF NOT EXISTS faers_male_meddra_code_idx ON faers_male (meddra_code);

CREATE INDEX IF NOT EXISTS omop_relationship_umls_cui_idx ON omop_relationship (umls_cui);
CREATE INDEX IF NOT EXISTS omop_relationship_concept_id_idx ON omop_relationship (concept_id);
CREATE INDEX IF NOT EXISTS omop_relationship_snomed_conceptid_idx ON omop_relationship (snomed_conceptid);

ANALYZE structures, identifier, faers, faers_female, faers_male, omop_relationship;
