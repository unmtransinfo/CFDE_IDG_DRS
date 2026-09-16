from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from psycopg2.errors import QueryCanceled
from sqlalchemy.exc import OperationalError, TimeoutError as PoolTimeoutError
from sqlalchemy.orm import Session
from app.models import ActTableFull
from app.models import Structures
from app.models import Identifier
from app.models import IdType
from app.models import Synonyms
from app.models import TargetClass
from app.models import TargetComponent
from app.models import TargetDictionary
from app.models import TargetGo
from app.models import TargetKeyword
from app.models import Td2tc
from app.models import Tdgo2tc
from app.models import Tdkey2tc
from app.models import OmopRelationship
from app.models import Product
from app.models import Struct2obprod
from app.models import Atc
from app.models import Struct2atc
from app.models import DrugClass
from app.models import Doid
from app.models import Faers
from app.models import FaersFemale
from app.models import FaersMale
from app.models import PkAz
from app.database import SessionLocal
from app.csv_utils import create_csv_response, create_tsv_response, generate_filename
from sqlalchemy import any_, func, text
from typing import Annotated, List

# Pagination bounds. Without them, negative or oversized values reach PostgreSQL and
# fail as a database error rather than a validation error. The maximum limit is above
# the largest table, so whole-table exports still work.
MAX_SKIP = 100_000_000
MAX_LIMIT = 1_000_000
Skip = Annotated[int, Query(ge=0, le=MAX_SKIP)]
Limit = Annotated[int, Query(ge=0, le=MAX_LIMIT)]

app = FastAPI(title="DrugCentral DRS API")

# PostgreSQL text cannot contain a NUL character; reject it here instead of failing
# inside the database driver with a 500.
@app.middleware("http")
async def reject_nul_in_path(request: Request, call_next):
    if "\x00" in request.scope.get("path", ""):
        return JSONResponse(status_code=422, content={"detail": "path contains a NUL character"})
    return await call_next(request)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Order every table query by its primary key, so skip/limit pages, exports and
# filtered results come back in the same order on every call.
def query_ordered(db: Session, model):
    return db.query(model).order_by(*model.__mapper__.primary_key)

# Database errors: return a clear status instead of a generic 500.
# QueryCanceled means the query exceeded statement_timeout (see app/database.py).
@app.exception_handler(OperationalError)
async def database_error_handler(request: Request, exc: OperationalError):
    if isinstance(exc.orig, QueryCanceled):
        return JSONResponse(status_code=504, content={"detail": "Database query timed out"})
    return JSONResponse(status_code=503, content={"detail": "Database unavailable"})

# Every pooled connection is in use and pool_timeout expired (see app/database.py).
@app.exception_handler(PoolTimeoutError)
async def database_busy_handler(request: Request, exc: PoolTimeoutError):
    return JSONResponse(status_code=503, content={"detail": "Database busy, try again later"})

# check if server is running ok
@app.get("/")
def root():
    return {"status": "ok"}

# check that the database is reachable; returns 503 (via the handler above) when it is not
@app.get("/health")
def health(db: Session = Depends(get_db)):
    dbversion = db.execute(text("SELECT max(version) FROM dbversion")).scalar()
    return {"status": "ok", "database": "ok", "dbversion": dbversion}

# TABLE 1:  act_table_full
@app.get("/act_table_full")
def read_act_table_full(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, ActTableFull).offset(skip).limit(limit).all()

@app.get("/act_table_full/act_id/{act_id}")
def read_act_table_full_by_act_id(act_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, ActTableFull).filter(ActTableFull.act_id == act_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="act_id not found")
    return result

@app.get("/act_table_full/struct_id/{struct_id}")
def read_act_table_full_by_struct_id(struct_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, ActTableFull).filter(ActTableFull.struct_id == struct_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="struct_id not found")
    return result

@app.get("/act_table_full/target_class/{target_class}")
def read_act_table_full_by_target_class(target_class: str, db: Session = Depends(get_db)):
    result = query_ordered(db, ActTableFull).filter(func.trim(ActTableFull.target_class).icontains(target_class, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="target_class not found")
    return result

@app.get("/act_table_full/accession/{accession}")
def read_act_table_full_by_accession(accession: str, db: Session = Depends(get_db)):
    """Exact match (case-insensitive) on any entry of the pipe-separated list, e.g. P02919 matches 'P02918|P02919|...'."""
    result = query_ordered(db, ActTableFull).filter(accession.strip().upper() == any_(func.string_to_array(ActTableFull.accession, "|"))).all()
    if not result:
        raise HTTPException(status_code=404, detail="accession not found")
    return result

@app.get("/act_table_full/gene/{gene}")
def read_act_table_full_by_gene(gene: str, db: Session = Depends(get_db)):
    result = query_ordered(db, ActTableFull).filter(func.trim(ActTableFull.gene).icontains(gene, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="gene not found")
    return result

@app.get("/act_table_full/swissprot/{swissprot}")
def read_act_table_full_by_swissprot(swissprot: str, db: Session = Depends(get_db)):
    """Exact match (case-insensitive) on any entry of the pipe-separated list, e.g. PBPB_ECOLI."""
    result = query_ordered(db, ActTableFull).filter(swissprot.strip().upper() == any_(func.string_to_array(ActTableFull.swissprot, "|"))).all()
    if not result:
        raise HTTPException(status_code=404, detail="swissprot not found")
    return result

@app.get("/act_table_full/act_type/{act_type}")
def read_act_table_full_by_act_type(act_type: str, db: Session = Depends(get_db)):
    result = query_ordered(db, ActTableFull).filter(func.trim(ActTableFull.act_type).icontains(act_type, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="act_type not found")
    return result

@app.get("/act_table_full/organism/{organism}")
def read_act_table_full_by_organism(organism: str, db: Session = Depends(get_db)):
    result = query_ordered(db, ActTableFull).filter(func.trim(ActTableFull.organism).icontains(organism, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="organism not found")
    return result

# CSV/TSV Export for act_table_full
@app.get("/act_table_full/csv")
def export_act_table_full_csv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, ActTableFull).offset(skip).limit(limit).all()
    filename = generate_filename("act_table_full", "csv")
    return create_csv_response(data, filename)

@app.get("/act_table_full/tsv")
def export_act_table_full_tsv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, ActTableFull).offset(skip).limit(limit).all()
    filename = generate_filename("act_table_full", "tsv")
    return create_tsv_response(data, filename)


# TABLE 2:  structures
@app.get("/structures")
def read_structures(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, Structures).offset(skip).limit(limit).all()

@app.get("/structures/cd_id/{cd_id}")
def read_structures_by_cd_id(cd_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Structures).filter(Structures.cd_id == cd_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="cd_id not found")
    return result

@app.get("/structures/id/{id}")
def read_structures_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Structures).filter(Structures.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/structures/name/{name}")
def read_structures_by_name(name: str, db: Session = Depends(get_db)):
    result = query_ordered(db, Structures).filter(func.trim(Structures.name).icontains(name, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="name not found")
    return result

@app.get("/structures/smiles/{smiles}")
def read_structures_by_smiles(smiles: str, db: Session = Depends(get_db)):
    result = query_ordered(db, Structures).filter(func.trim(Structures.smiles).icontains(smiles, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="smiles not found")
    return result

@app.get("/structures/inchikey/{inchikey}")
def read_structures_by_inchikey(inchikey: str, db: Session = Depends(get_db)):
    """Exact match (case-insensitive), e.g. LIOLIMKSCNQPLV-UHFFFAOYSA-N."""
    result = query_ordered(db, Structures).filter(Structures.inchikey == inchikey.strip().upper()).all()
    if not result:
        raise HTTPException(status_code=404, detail="inchikey not found")
    return result

# CSV/TSV Export for structures
@app.get("/structures/csv")
def export_structures_csv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, Structures).offset(skip).limit(limit).all()
    filename = generate_filename("structures", "csv")
    # Exclude molfile column by default - it contains multi-line data that causes parsing issues
    return create_csv_response(data, filename, exclude_columns=['molfile'])

@app.get("/structures/tsv")
def export_structures_tsv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, Structures).offset(skip).limit(limit).all()
    filename = generate_filename("structures", "tsv")
    # Exclude molfile column by default - it contains multi-line data that causes parsing issues
    return create_tsv_response(data, filename, exclude_columns=['molfile'])


# TABLE 3:  Identifier
@app.get("/identifier")
def read_identifier(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, Identifier).offset(skip).limit(limit).all()

@app.get("/identifier/id/{id}")
def read_identifier_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Identifier).filter(Identifier.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/identifier/identifier/{identifier}")
def read_identifier_by_identifier(identifier: str, db: Session = Depends(get_db)):
    """Exact match, ignoring case and surrounding spaces, e.g. CHEMBL3188267."""
    result = query_ordered(db, Identifier).filter(func.upper(func.trim(Identifier.identifier)) == identifier.strip().upper()).all()
    if not result:
        raise HTTPException(status_code=404, detail="identifier not found")
    return result

@app.get("/identifier/id_type/{id_type}")
def read_identifier_by_id_type(id_type: str, db: Session = Depends(get_db)):
    result = query_ordered(db, Identifier).filter(func.trim(Identifier.id_type).icontains(id_type, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="id_type not found")
    return result

@app.get("/identifier/struct_id/{struct_id}")
def read_identifier_by_struct_id(struct_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Identifier).filter(Identifier.struct_id == struct_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="struct_id not found")
    return result


# Table 4: id_type
@app.get("/id_type")
def read_id_type(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, IdType).offset(skip).limit(limit).all()

@app.get("/id_type/id/{id}")
def read_id_type_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, IdType).filter(IdType.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/id_type/type/{type}")
def read_id_type_by_type(type: str, db: Session = Depends(get_db)):
    result = query_ordered(db, IdType).filter(func.trim(IdType.type).icontains(type, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="type not found")
    return result


# Table 5: synonyms
@app.get("/synonyms")
def read_synonyms(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, Synonyms).offset(skip).limit(limit).all()

@app.get("/synonyms/syn_id/{syn_id}")
def read_synonyms_by_syn_id(syn_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Synonyms).filter(Synonyms.syn_id == syn_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="syn_id not found")
    return result

@app.get("/synonyms/id/{id}")
def read_synonyms_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Synonyms).filter(Synonyms.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/synonyms/name/{name}")
def read_synonyms_by_name(name: str, db: Session = Depends(get_db)):
    result = query_ordered(db, Synonyms).filter(func.trim(Synonyms.name).icontains(name, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="name not found")
    return result

# CSV/TSV Export for synonyms
@app.get("/synonyms/csv")
def export_synonyms_csv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, Synonyms).offset(skip).limit(limit).all()
    filename = generate_filename("synonyms", "csv")
    return create_csv_response(data, filename)

@app.get("/synonyms/tsv")
def export_synonyms_tsv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, Synonyms).offset(skip).limit(limit).all()
    filename = generate_filename("synonyms", "tsv")
    return create_tsv_response(data, filename)

# Table 6: target_class
@app.get("/target_class")
def read_target_class(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, TargetClass).offset(skip).limit(limit).all()

@app.get("/target_class/id/{id}")
def read_target_class_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, TargetClass).filter(TargetClass.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/target_class/l1/{l1}")
def read_target_class_by_l1(l1: str, db: Session = Depends(get_db)):
    result = query_ordered(db, TargetClass).filter(func.trim(TargetClass.l1).icontains(l1, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="l1 not found")
    return result


# Table 7: target_component
@app.get("/target_component")
def read_target_component(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, TargetComponent).offset(skip).limit(limit).all()

@app.get("/target_component/id/{id}")
def read_target_component_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, TargetComponent).filter(TargetComponent.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/target_component/accession/{accession}")
def read_target_component_by_accession(accession: str, db: Session = Depends(get_db)):
    """Exact match (case-insensitive) on the UniProt accession, e.g. P08581."""
    result = query_ordered(db, TargetComponent).filter(TargetComponent.accession == accession.strip().upper()).all()
    if not result:
        raise HTTPException(status_code=404, detail="accession not found")
    return result

@app.get("/target_component/swissprot/{swissprot}")
def read_target_component_by_swissprot(swissprot: str, db: Session = Depends(get_db)):
    """Exact match (case-insensitive) on the SwissProt name, e.g. MET_HUMAN."""
    result = query_ordered(db, TargetComponent).filter(TargetComponent.swissprot == swissprot.strip().upper()).all()
    if not result:
        raise HTTPException(status_code=404, detail="swissprot not found")
    return result

@app.get("/target_component/organism/{organism}")
def read_target_component_by_organism(organism: str, db: Session = Depends(get_db)):
    result = query_ordered(db, TargetComponent).filter(func.trim(TargetComponent.organism).icontains(organism, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="organism not found")
    return result

@app.get("/target_component/gene/{gene}")
def read_target_component_by_gene(gene: str, db: Session = Depends(get_db)):
    result = query_ordered(db, TargetComponent).filter(func.trim(TargetComponent.gene).icontains(gene, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="gene not found")
    return result

# CSV/TSV Export for target_component
@app.get("/target_component/csv")
def export_target_component_csv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, TargetComponent).offset(skip).limit(limit).all()
    filename = generate_filename("target_component", "csv")
    return create_csv_response(data, filename)

@app.get("/target_component/tsv")
def export_target_component_tsv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, TargetComponent).offset(skip).limit(limit).all()
    filename = generate_filename("target_component", "tsv")
    return create_tsv_response(data, filename)


# Table 8: target_dictionary
@app.get("/target_dictionary")
def read_target_dictionary(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, TargetDictionary).offset(skip).limit(limit).all()

@app.get("/target_dictionary/id/{id}")
def read_target_dictionary_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, TargetDictionary).filter(TargetDictionary.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/target_dictionary/target_class/{target_class}")
def read_target_dictionary_by_target_class(target_class: str, db: Session = Depends(get_db)):
    result = query_ordered(db, TargetDictionary).filter(func.trim(TargetDictionary.target_class).icontains(target_class, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="target_class not found")
    return result


# Table 9: target_go
@app.get("/target_go")
def read_target_go(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, TargetGo).offset(skip).limit(limit).all()

@app.get("/target_go/id/{id}")
def read_target_go_by_id(id: str, db: Session = Depends(get_db)):
    """Exact match (case-insensitive) on the GO id, e.g. GO:0005737."""
    result = query_ordered(db, TargetGo).filter(TargetGo.id == id.strip().upper()).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/target_go/type/{type}")
def read_target_go_by_type(type: str, db: Session = Depends(get_db)):
    result = query_ordered(db, TargetGo).filter(func.trim(TargetGo.type).icontains(type, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="type not found")
    return result


# Table 10: target_keyword
@app.get("/target_keyword")
def read_target_keyword(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, TargetKeyword).offset(skip).limit(limit).all()

@app.get("/target_keyword/id/{id}")
def read_target_keyword_by_id(id: str, db: Session = Depends(get_db)):
    """Exact match (case-insensitive) on the UniProt keyword id, e.g. KW-0001."""
    result = query_ordered(db, TargetKeyword).filter(TargetKeyword.id == id.strip().upper()).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/target_keyword/category/{category}")
def read_target_keyword_by_category(category: str, db: Session = Depends(get_db)):
    result = query_ordered(db, TargetKeyword).filter(func.trim(TargetKeyword.category).icontains(category, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="category not found")
    return result

@app.get("/target_keyword/keyword/{keyword}")
def read_target_keyword_by_keyword(keyword: str, db: Session = Depends(get_db)):
    result = query_ordered(db, TargetKeyword).filter(func.trim(TargetKeyword.keyword).icontains(keyword, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="keyword not found")
    return result


# Table 11: td2tc
@app.get("/td2tc")
def read_td2tc(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, Td2tc).offset(skip).limit(limit).all()

@app.get("/td2tc/target_id/{target_id}")
def read_td2tc_by_target_id(target_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Td2tc).filter(Td2tc.target_id == target_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="target_id not found")
    return result

@app.get("/td2tc/component_id/{component_id}")
def read_td2tc_by_component_id(component_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Td2tc).filter(Td2tc.component_id == component_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="component_id not found")
    return result


# Table 12: tdgo2tc
@app.get("/tdgo2tc")
def read_tdgo2tc(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, Tdgo2tc).offset(skip).limit(limit).all()

@app.get("/tdgo2tc/id/{id}")
def read_tdgo2tc_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Tdgo2tc).filter(Tdgo2tc.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/tdgo2tc/go_id/{go_id}")
def read_tdgo2tc_by_go_id(go_id: str, db: Session = Depends(get_db)):
    """Exact match (case-insensitive) on the GO id, e.g. GO:0005737."""
    result = query_ordered(db, Tdgo2tc).filter(Tdgo2tc.go_id == go_id.strip().upper()).all()
    if not result:
        raise HTTPException(status_code=404, detail="go_id not found")
    return result

@app.get("/tdgo2tc/component_id/{component_id}")
def read_tdgo2tc_by_component_id(component_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Tdgo2tc).filter(Tdgo2tc.component_id == component_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="component_id not found")
    return result



# Table 13: tdkey2tc
@app.get("/tdkey2tc")
def read_tdkey2tc(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, Tdkey2tc).offset(skip).limit(limit).all()

@app.get("/tdkey2tc/id/{id}")
def read_tdkey2tc_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Tdkey2tc).filter(Tdkey2tc.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/tdkey2tc/tdkey_id/{tdkey_id}")
def read_tdkey2tc_by_tdkey_id(tdkey_id: str, db: Session = Depends(get_db)):
    """Exact match (case-insensitive) on the UniProt keyword id, e.g. KW-0001."""
    result = query_ordered(db, Tdkey2tc).filter(Tdkey2tc.tdkey_id == tdkey_id.strip().upper()).all()
    if not result:
        raise HTTPException(status_code=404, detail="tdkey_id not found")
    return result

@app.get("/tdkey2tc/component_id/{component_id}")
def read_tdkey2tc_by_component_id(component_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Tdkey2tc).filter(Tdkey2tc.component_id == component_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="component_id not found")
    return result



# Table 14: omop_relationship
@app.get("/omop_relationship")
def read_omop_relationship(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, OmopRelationship).offset(skip).limit(limit).all()

@app.get("/omop_relationship/id/{id}")
def read_omop_relationship_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, OmopRelationship).filter(OmopRelationship.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/omop_relationship/struct_id/{struct_id}")
def read_omop_relationship_by_struct_id(struct_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, OmopRelationship).filter(OmopRelationship.struct_id == struct_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="struct_id not found")
    return result

@app.get("/omop_relationship/concept_id/{concept_id}")
def read_omop_relationship_by_concept_id(concept_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, OmopRelationship).filter(OmopRelationship.concept_id == concept_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="concept_id not found")
    return result

@app.get("/omop_relationship/relationship_name/{relationship_name}")
def read_omop_relationship_by_relationship_name(relationship_name: str, db: Session = Depends(get_db)):
    result = query_ordered(db, OmopRelationship).filter(func.trim(OmopRelationship.relationship_name).icontains(relationship_name, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="relationship_name not found")
    return result

@app.get("/omop_relationship/concept_name/{concept_name}")
def read_omop_relationship_by_concept_name(concept_name: str, db: Session = Depends(get_db)):
    result = query_ordered(db, OmopRelationship).filter(func.trim(OmopRelationship.concept_name).icontains(concept_name, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="concept_name not found")
    return result

@app.get("/omop_relationship/umls_cui/{umls_cui}")
def read_omop_relationship_by_umls_cui(umls_cui: str, db: Session = Depends(get_db)):
    """Exact match (case-insensitive) on the UMLS CUI, e.g. C0000737."""
    result = query_ordered(db, OmopRelationship).filter(OmopRelationship.umls_cui == umls_cui.strip().upper()).all()
    if not result:
        raise HTTPException(status_code=404, detail="umls_cui not found")
    return result

@app.get("/omop_relationship/cui_semantic_type/{cui_semantic_type}")
def read_omop_relationship_by_cui_semantic_type(cui_semantic_type: str, db: Session = Depends(get_db)):
    result = query_ordered(db, OmopRelationship).filter(func.trim(OmopRelationship.cui_semantic_type).icontains(cui_semantic_type, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="cui_semantic_type not found")
    return result

@app.get("/omop_relationship/snomed_conceptid/{snomed_conceptid}")
def read_omop_relationship_by_snomed_conceptid(snomed_conceptid: int, db: Session = Depends(get_db)):
    result = query_ordered(db, OmopRelationship).filter(OmopRelationship.snomed_conceptid == snomed_conceptid).all()
    if not result:
        raise HTTPException(status_code=404, detail="snomed_conceptid not found")
    return result



# Table 15: product
@app.get("/product")
def read_product(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, Product).offset(skip).limit(limit).all()

@app.get("/product/id/{id}")
def read_product_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Product).filter(Product.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/product/ndc_product_code/{ndc_product_code}")
def read_product_by_ndc_product_code(ndc_product_code: str, db: Session = Depends(get_db)):
    """Exact match on the NDC product code, e.g. 0002-0152."""
    result = query_ordered(db, Product).filter(Product.ndc_product_code == ndc_product_code.strip()).all()
    if not result:
        raise HTTPException(status_code=404, detail="ndc_product_code not found")
    return result

@app.get("/product/product_name/{product_name}")
def read_product_by_product_name(product_name: str, db: Session = Depends(get_db)):
    result = query_ordered(db, Product).filter(func.trim(Product.product_name).icontains(product_name, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="product_name not found")
    return result

@app.get("/product/route/{route}")
def read_product_by_route(route: str, db: Session = Depends(get_db)):
    result = query_ordered(db, Product).filter(func.trim(Product.route).icontains(route, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="route not found")
    return result

# CSV/TSV Export for product
@app.get("/product/csv")
def export_product_csv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, Product).offset(skip).limit(limit).all()
    filename = generate_filename("product", "csv")
    return create_csv_response(data, filename)

@app.get("/product/tsv")
def export_product_tsv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, Product).offset(skip).limit(limit).all()
    filename = generate_filename("product", "tsv")
    return create_tsv_response(data, filename)



# Table 16: struct2obprod
@app.get("/struct2obprod")
def read_struct2obprod(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, Struct2obprod).offset(skip).limit(limit).all()

@app.get("/struct2obprod/struct_id/{struct_id}")
def read_struct2obprod_by_struct_id(struct_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Struct2obprod).filter(Struct2obprod.struct_id == struct_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="struct_id not found")
    return result

@app.get("/struct2obprod/prod_id/{prod_id}")
def read_struct2obprod_by_prod_id(prod_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Struct2obprod).filter(Struct2obprod.prod_id == prod_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="prod_id not found")
    return result



# Table 17: atc
@app.get("/atc")
def read_atc(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, Atc).offset(skip).limit(limit).all()

@app.get("/atc/id/{id}")
def read_atc_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Atc).filter(Atc.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/atc/code/{code}")
def read_atc_by_code(code: str, db: Session = Depends(get_db)):
    """ATC code prefix: a full 7-character code matches exactly; a shorter code (e.g. N02B) returns that ATC group."""
    result = query_ordered(db, Atc).filter(Atc.code.startswith(code.strip().upper(), autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="code not found")
    return result

@app.get("/atc/chemical_substance/{chemical_substance}")
def read_atc_by_chemical_substance(chemical_substance: str, db: Session = Depends(get_db)):
    result = query_ordered(db, Atc).filter(func.trim(Atc.chemical_substance).icontains(chemical_substance, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="chemical_substance not found")
    return result


# Table 18: struct2atc
@app.get("/struct2atc")
def read_struct2atc(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, Struct2atc).offset(skip).limit(limit).all()

@app.get("/struct2atc/struct_id/{struct_id}")
def read_struct2atc_by_struct_id(struct_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Struct2atc).filter(Struct2atc.struct_id == struct_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="struct_id not found")
    return result

@app.get("/struct2atc/atc_code/{atc_code}")
def read_struct2atc_by_atc_code(atc_code: str, db: Session = Depends(get_db)):
    """ATC code prefix: a full 7-character code matches exactly; a shorter code (e.g. N02B) returns that ATC group."""
    result = query_ordered(db, Struct2atc).filter(Struct2atc.atc_code.startswith(atc_code.strip().upper(), autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="atc_code not found")
    return result



# Table 19: drug_class
@app.get("/drug_class")
def read_drug_class(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, DrugClass).offset(skip).limit(limit).all()

@app.get("/drug_class/id/{id}")
def read_drug_class_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, DrugClass).filter(DrugClass.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/drug_class/name/{name}")
def read_drug_class_by_name(name: str, db: Session = Depends(get_db)):
    result = query_ordered(db, DrugClass).filter(func.trim(DrugClass.name).icontains(name, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="name not found")
    return result

@app.get("/drug_class/source/{source}")
def read_drug_class_by_source(source: str, db: Session = Depends(get_db)):
    result = query_ordered(db, DrugClass).filter(func.trim(DrugClass.source).icontains(source, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="source not found")
    return result


# Table 20: faers (all patients)
@app.get("/faers")
def read_faers(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, Faers).offset(skip).limit(limit).all()

@app.get("/faers/id/{id}")
def read_faers_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Faers).filter(Faers.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/faers/struct_id/{struct_id}")
def read_faers_by_struct_id(struct_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Faers).filter(Faers.struct_id == struct_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="struct_id not found")
    return result

@app.get("/faers/meddra_name/{meddra_name}")
def read_faers_by_meddra_name(meddra_name: str, db: Session = Depends(get_db)):
    result = query_ordered(db, Faers).filter(func.trim(Faers.meddra_name).icontains(meddra_name, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="meddra_name not found")
    return result

@app.get("/faers/meddra_code/{meddra_code}")
def read_faers_by_meddra_code(meddra_code: int, db: Session = Depends(get_db)):
    result = query_ordered(db, Faers).filter(Faers.meddra_code == meddra_code).all()
    if not result:
        raise HTTPException(status_code=404, detail="meddra_code not found")
    return result

# CSV/TSV Export for faers
@app.get("/faers/csv")
def export_faers_csv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, Faers).offset(skip).limit(limit).all()
    filename = generate_filename("faers", "csv")
    return create_csv_response(data, filename)

@app.get("/faers/tsv")
def export_faers_tsv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, Faers).offset(skip).limit(limit).all()
    filename = generate_filename("faers", "tsv")
    return create_tsv_response(data, filename)

# Filtered CSV/TSV Export for faers
@app.get("/faers/id/{id}/csv")
def export_faers_by_id_csv(id: int, db: Session = Depends(get_db)):
    data = query_ordered(db, Faers).filter(Faers.id == id).all()
    if not data:
        raise HTTPException(status_code=404, detail="id not found")
    filename = generate_filename("faers_id", "csv")
    return create_csv_response(data, filename)

@app.get("/faers/id/{id}/tsv")
def export_faers_by_id_tsv(id: int, db: Session = Depends(get_db)):
    data = query_ordered(db, Faers).filter(Faers.id == id).all()
    if not data:
        raise HTTPException(status_code=404, detail="id not found")
    filename = generate_filename("faers_id", "tsv")
    return create_tsv_response(data, filename)

@app.get("/faers/struct_id/{struct_id}/csv")
def export_faers_by_struct_id_csv(struct_id: int, db: Session = Depends(get_db)):
    data = query_ordered(db, Faers).filter(Faers.struct_id == struct_id).all()
    if not data:
        raise HTTPException(status_code=404, detail="struct_id not found")
    filename = generate_filename("faers_struct_id", "csv")
    return create_csv_response(data, filename)

@app.get("/faers/struct_id/{struct_id}/tsv")
def export_faers_by_struct_id_tsv(struct_id: int, db: Session = Depends(get_db)):
    data = query_ordered(db, Faers).filter(Faers.struct_id == struct_id).all()
    if not data:
        raise HTTPException(status_code=404, detail="struct_id not found")
    filename = generate_filename("faers_struct_id", "tsv")
    return create_tsv_response(data, filename)

@app.get("/faers/meddra_name/{meddra_name}/csv")
def export_faers_by_meddra_name_csv(meddra_name: str, db: Session = Depends(get_db)):
    data = query_ordered(db, Faers).filter(func.trim(Faers.meddra_name).icontains(meddra_name, autoescape=True)).all()
    if not data:
        raise HTTPException(status_code=404, detail="meddra_name not found")
    filename = generate_filename("faers_meddra_name", "csv")
    return create_csv_response(data, filename)

@app.get("/faers/meddra_name/{meddra_name}/tsv")
def export_faers_by_meddra_name_tsv(meddra_name: str, db: Session = Depends(get_db)):
    data = query_ordered(db, Faers).filter(func.trim(Faers.meddra_name).icontains(meddra_name, autoescape=True)).all()
    if not data:
        raise HTTPException(status_code=404, detail="meddra_name not found")
    filename = generate_filename("faers_meddra_name", "tsv")
    return create_tsv_response(data, filename)

@app.get("/faers/meddra_code/{meddra_code}/csv")
def export_faers_by_meddra_code_csv(meddra_code: int, db: Session = Depends(get_db)):
    data = query_ordered(db, Faers).filter(Faers.meddra_code == meddra_code).all()
    if not data:
        raise HTTPException(status_code=404, detail="meddra_code not found")
    filename = generate_filename("faers_meddra_code", "csv")
    return create_csv_response(data, filename)

@app.get("/faers/meddra_code/{meddra_code}/tsv")
def export_faers_by_meddra_code_tsv(meddra_code: int, db: Session = Depends(get_db)):
    data = query_ordered(db, Faers).filter(Faers.meddra_code == meddra_code).all()
    if not data:
        raise HTTPException(status_code=404, detail="meddra_code not found")
    filename = generate_filename("faers_meddra_code", "tsv")
    return create_tsv_response(data, filename)


# Table 21: faers_female
@app.get("/faers_female")
def read_faers_female(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, FaersFemale).offset(skip).limit(limit).all()

@app.get("/faers_female/id/{id}")
def read_faers_female_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, FaersFemale).filter(FaersFemale.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/faers_female/struct_id/{struct_id}")
def read_faers_female_by_struct_id(struct_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, FaersFemale).filter(FaersFemale.struct_id == struct_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="struct_id not found")
    return result

@app.get("/faers_female/meddra_name/{meddra_name}")
def read_faers_female_by_meddra_name(meddra_name: str, db: Session = Depends(get_db)):
    result = query_ordered(db, FaersFemale).filter(func.trim(FaersFemale.meddra_name).icontains(meddra_name, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="meddra_name not found")
    return result

@app.get("/faers_female/meddra_code/{meddra_code}")
def read_faers_female_by_meddra_code(meddra_code: int, db: Session = Depends(get_db)):
    result = query_ordered(db, FaersFemale).filter(FaersFemale.meddra_code == meddra_code).all()
    if not result:
        raise HTTPException(status_code=404, detail="meddra_code not found")
    return result

# CSV/TSV Export for faers_female
@app.get("/faers_female/csv")
def export_faers_female_csv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersFemale).offset(skip).limit(limit).all()
    filename = generate_filename("faers_female", "csv")
    return create_csv_response(data, filename)

@app.get("/faers_female/tsv")
def export_faers_female_tsv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersFemale).offset(skip).limit(limit).all()
    filename = generate_filename("faers_female", "tsv")
    return create_tsv_response(data, filename)

# Filtered CSV/TSV Export for faers_female
@app.get("/faers_female/id/{id}/csv")
def export_faers_female_by_id_csv(id: int, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersFemale).filter(FaersFemale.id == id).all()
    if not data:
        raise HTTPException(status_code=404, detail="id not found")
    filename = generate_filename("faers_female_id", "csv")
    return create_csv_response(data, filename)

@app.get("/faers_female/id/{id}/tsv")
def export_faers_female_by_id_tsv(id: int, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersFemale).filter(FaersFemale.id == id).all()
    if not data:
        raise HTTPException(status_code=404, detail="id not found")
    filename = generate_filename("faers_female_id", "tsv")
    return create_tsv_response(data, filename)

@app.get("/faers_female/struct_id/{struct_id}/csv")
def export_faers_female_by_struct_id_csv(struct_id: int, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersFemale).filter(FaersFemale.struct_id == struct_id).all()
    if not data:
        raise HTTPException(status_code=404, detail="struct_id not found")
    filename = generate_filename("faers_female_struct_id", "csv")
    return create_csv_response(data, filename)

@app.get("/faers_female/struct_id/{struct_id}/tsv")
def export_faers_female_by_struct_id_tsv(struct_id: int, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersFemale).filter(FaersFemale.struct_id == struct_id).all()
    if not data:
        raise HTTPException(status_code=404, detail="struct_id not found")
    filename = generate_filename("faers_female_struct_id", "tsv")
    return create_tsv_response(data, filename)

@app.get("/faers_female/meddra_name/{meddra_name}/csv")
def export_faers_female_by_meddra_name_csv(meddra_name: str, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersFemale).filter(func.trim(FaersFemale.meddra_name).icontains(meddra_name, autoescape=True)).all()
    if not data:
        raise HTTPException(status_code=404, detail="meddra_name not found")
    filename = generate_filename("faers_female_meddra_name", "csv")
    return create_csv_response(data, filename)

@app.get("/faers_female/meddra_name/{meddra_name}/tsv")
def export_faers_female_by_meddra_name_tsv(meddra_name: str, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersFemale).filter(func.trim(FaersFemale.meddra_name).icontains(meddra_name, autoescape=True)).all()
    if not data:
        raise HTTPException(status_code=404, detail="meddra_name not found")
    filename = generate_filename("faers_female_meddra_name", "tsv")
    return create_tsv_response(data, filename)

@app.get("/faers_female/meddra_code/{meddra_code}/csv")
def export_faers_female_by_meddra_code_csv(meddra_code: int, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersFemale).filter(FaersFemale.meddra_code == meddra_code).all()
    if not data:
        raise HTTPException(status_code=404, detail="meddra_code not found")
    filename = generate_filename("faers_female_meddra_code", "csv")
    return create_csv_response(data, filename)

@app.get("/faers_female/meddra_code/{meddra_code}/tsv")
def export_faers_female_by_meddra_code_tsv(meddra_code: int, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersFemale).filter(FaersFemale.meddra_code == meddra_code).all()
    if not data:
        raise HTTPException(status_code=404, detail="meddra_code not found")
    filename = generate_filename("faers_female_meddra_code", "tsv")
    return create_tsv_response(data, filename)


# Table 22: faers_male
@app.get("/faers_male")
def read_faers_male(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    return query_ordered(db, FaersMale).offset(skip).limit(limit).all()

@app.get("/faers_male/id/{id}")
def read_faers_male_by_id(id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, FaersMale).filter(FaersMale.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/faers_male/struct_id/{struct_id}")
def read_faers_male_by_struct_id(struct_id: int, db: Session = Depends(get_db)):
    result = query_ordered(db, FaersMale).filter(FaersMale.struct_id == struct_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="struct_id not found")
    return result

@app.get("/faers_male/meddra_name/{meddra_name}")
def read_faers_male_by_meddra_name(meddra_name: str, db: Session = Depends(get_db)):
    result = query_ordered(db, FaersMale).filter(func.trim(FaersMale.meddra_name).icontains(meddra_name, autoescape=True)).all()
    if not result:
        raise HTTPException(status_code=404, detail="meddra_name not found")
    return result

@app.get("/faers_male/meddra_code/{meddra_code}")
def read_faers_male_by_meddra_code(meddra_code: int, db: Session = Depends(get_db)):
    result = query_ordered(db, FaersMale).filter(FaersMale.meddra_code == meddra_code).all()
    if not result:
        raise HTTPException(status_code=404, detail="meddra_code not found")
    return result

# CSV/TSV Export for faers_male
@app.get("/faers_male/csv")
def export_faers_male_csv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersMale).offset(skip).limit(limit).all()
    filename = generate_filename("faers_male", "csv")
    return create_csv_response(data, filename)

@app.get("/faers_male/tsv")
def export_faers_male_tsv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersMale).offset(skip).limit(limit).all()
    filename = generate_filename("faers_male", "tsv")
    return create_tsv_response(data, filename)

# Filtered CSV/TSV Export for faers_male
@app.get("/faers_male/id/{id}/csv")
def export_faers_male_by_id_csv(id: int, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersMale).filter(FaersMale.id == id).all()
    if not data:
        raise HTTPException(status_code=404, detail="id not found")
    filename = generate_filename("faers_male_id", "csv")
    return create_csv_response(data, filename)

@app.get("/faers_male/id/{id}/tsv")
def export_faers_male_by_id_tsv(id: int, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersMale).filter(FaersMale.id == id).all()
    if not data:
        raise HTTPException(status_code=404, detail="id not found")
    filename = generate_filename("faers_male_id", "tsv")
    return create_tsv_response(data, filename)

@app.get("/faers_male/struct_id/{struct_id}/csv")
def export_faers_male_by_struct_id_csv(struct_id: int, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersMale).filter(FaersMale.struct_id == struct_id).all()
    if not data:
        raise HTTPException(status_code=404, detail="struct_id not found")
    filename = generate_filename("faers_male_struct_id", "csv")
    return create_csv_response(data, filename)

@app.get("/faers_male/struct_id/{struct_id}/tsv")
def export_faers_male_by_struct_id_tsv(struct_id: int, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersMale).filter(FaersMale.struct_id == struct_id).all()
    if not data:
        raise HTTPException(status_code=404, detail="struct_id not found")
    filename = generate_filename("faers_male_struct_id", "tsv")
    return create_tsv_response(data, filename)

@app.get("/faers_male/meddra_name/{meddra_name}/csv")
def export_faers_male_by_meddra_name_csv(meddra_name: str, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersMale).filter(func.trim(FaersMale.meddra_name).icontains(meddra_name, autoescape=True)).all()
    if not data:
        raise HTTPException(status_code=404, detail="meddra_name not found")
    filename = generate_filename("faers_male_meddra_name", "csv")
    return create_csv_response(data, filename)

@app.get("/faers_male/meddra_name/{meddra_name}/tsv")
def export_faers_male_by_meddra_name_tsv(meddra_name: str, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersMale).filter(func.trim(FaersMale.meddra_name).icontains(meddra_name, autoescape=True)).all()
    if not data:
        raise HTTPException(status_code=404, detail="meddra_name not found")
    filename = generate_filename("faers_male_meddra_name", "tsv")
    return create_tsv_response(data, filename)

@app.get("/faers_male/meddra_code/{meddra_code}/csv")
def export_faers_male_by_meddra_code_csv(meddra_code: int, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersMale).filter(FaersMale.meddra_code == meddra_code).all()
    if not data:
        raise HTTPException(status_code=404, detail="meddra_code not found")
    filename = generate_filename("faers_male_meddra_code", "csv")
    return create_csv_response(data, filename)

@app.get("/faers_male/meddra_code/{meddra_code}/tsv")
def export_faers_male_by_meddra_code_tsv(meddra_code: int, db: Session = Depends(get_db)):
    data = query_ordered(db, FaersMale).filter(FaersMale.meddra_code == meddra_code).all()
    if not data:
        raise HTTPException(status_code=404, detail="meddra_code not found")
    filename = generate_filename("faers_male_meddra_code", "tsv")
    return create_tsv_response(data, filename)


# Table 23: pk_az (predictions from AstraZeneca models, not measured values)
def query_pk_az_by_struct_id(db: Session, struct_id: int):
    result = db.query(PkAz).filter(PkAz.struct_id == struct_id).order_by(PkAz.type).all()
    if not result:
        raise HTTPException(status_code=404, detail="struct_id not found")
    return result

def query_pk_az_by_type(db: Session, type: str):
    result = db.query(PkAz).filter(func.lower(PkAz.type) == type.lower()).order_by(PkAz.struct_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="type not found")
    return result

@app.get("/pk_az")
def read_pk_az(skip: Skip = 0, limit: Limit = 10, db: Session = Depends(get_db)):
    """
    Predicted pharmacokinetic, toxicological, and safety properties for drugs, from predictive
    models developed and released by researchers at AstraZeneca. Values are model predictions,
    not measurements.

    - **struct_id**: drug identifier referencing structures.id
    - **type**: property type, e.g. `herg`, `hppb`, `solubility-dd`, `kinase-safety-class`
    - **value**: predicted numeric value; for the kinase safety/selectivity classes, the number of
      predicted kinase hits; for `pfas-class`, 1 = PFAS structural alert, 0 = none
    - **unit**: unit of the property, or `null`. For some types (`mh-clint`, `mppb`) the
      unit is missing in the source data rather than the property being unitless
    - **description**: description of the property; for the kinase classes, the predicted kinase hits
    - **similarity**: Tanimoto similarity to the nearest compound in the model training set
    - **confidence**: `Moderate` for similarity 0.65-0.79, `High` for 0.8-1.0. Together with
      `similarity` it is `null` only for `kinase-safety-class`, `kinase-selectivity-class`
      and `pfas-class`; `pld-class` has both, despite its name
    """
    return db.query(PkAz).order_by(PkAz.struct_id, PkAz.type).offset(skip).limit(limit).all()

@app.get("/pk_az/struct_id/{struct_id}")
def read_pk_az_by_struct_id(struct_id: int, db: Session = Depends(get_db)):
    """All predicted properties for one drug."""
    return query_pk_az_by_struct_id(db, struct_id)

@app.get("/pk_az/type/{type}")
def read_pk_az_by_type(type: str, db: Session = Depends(get_db)):
    """Predictions of one property type for all drugs (exact match, case-insensitive), e.g. `herg`."""
    return query_pk_az_by_type(db, type)

# CSV/TSV Export for pk_az
@app.get("/pk_az/csv")
def export_pk_az_csv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = db.query(PkAz).order_by(PkAz.struct_id, PkAz.type).offset(skip).limit(limit).all()
    filename = generate_filename("pk_az", "csv")
    return create_csv_response(data, filename)

@app.get("/pk_az/tsv")
def export_pk_az_tsv(skip: Skip = 0, limit: Limit = 1000, db: Session = Depends(get_db)):
    data = db.query(PkAz).order_by(PkAz.struct_id, PkAz.type).offset(skip).limit(limit).all()
    filename = generate_filename("pk_az", "tsv")
    return create_tsv_response(data, filename)

# Filtered CSV/TSV Export for pk_az
@app.get("/pk_az/struct_id/{struct_id}/csv")
def export_pk_az_by_struct_id_csv(struct_id: int, db: Session = Depends(get_db)):
    return create_csv_response(query_pk_az_by_struct_id(db, struct_id), generate_filename("pk_az_struct_id", "csv"))

@app.get("/pk_az/struct_id/{struct_id}/tsv")
def export_pk_az_by_struct_id_tsv(struct_id: int, db: Session = Depends(get_db)):
    return create_tsv_response(query_pk_az_by_struct_id(db, struct_id), generate_filename("pk_az_struct_id", "tsv"))

@app.get("/pk_az/type/{type}/csv")
def export_pk_az_by_type_csv(type: str, db: Session = Depends(get_db)):
    return create_csv_response(query_pk_az_by_type(db, type), generate_filename("pk_az_type", "csv"))

@app.get("/pk_az/type/{type}/tsv")
def export_pk_az_by_type_tsv(type: str, db: Session = Depends(get_db)):
    return create_tsv_response(query_pk_az_by_type(db, type), generate_filename("pk_az_type", "tsv"))












