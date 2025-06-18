from fastapi import FastAPI, Depends, HTTPException
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
from app.database import SessionLocal
from urllib.parse import unquote
from sqlalchemy import func
from typing import List

app = FastAPI(title="DrugCentral DRS API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# check if server is running ok
@app.get("/")
def root():
    return {"status": "ok"}

# TABLE 1:  act_table_full
@app.get("/act_table_full")
def read_doid(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ActTableFull).offset(skip).limit(limit).all()

@app.get("/act_table_full/act_id/{act_id}")
def read_act_table_full_by_act_id(act_id: int, db: Session = Depends(get_db)):
    result = db.query(ActTableFull).filter(ActTableFull.act_id == act_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="act_id not found")
    return result

@app.get("/act_table_full/struct_id/{struct_id}")
def read_act_table_full_by_struct_id(struct_id: int, db: Session = Depends(get_db)):
    result = db.query(ActTableFull).filter(ActTableFull.struct_id == struct_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="struct_id not found")
    return result

@app.get("/act_table_full/target_class/{target_class}")
def read_act_table_full_by_target_class(target_class: str, db: Session = Depends(get_db)):
    decoded_target_class = unquote(target_class)
    result = db.query(ActTableFull).filter(func.trim(ActTableFull.target_class).ilike(f"%{decoded_target_class}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="target_class not found")
    return result

@app.get("/act_table_full/accession/{accession}")
def read_act_table_full_by_accession(accession: str, db: Session = Depends(get_db)):
    decoded_accession = unquote(accession)
    result = db.query(ActTableFull).filter(func.trim(ActTableFull.accession).ilike(f"%{decoded_accession}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="accession not found")
    return result

@app.get("/act_table_full/gene/{gene}")
def read_act_table_full_by_gene(gene: str, db: Session = Depends(get_db)):
    decoded_gene = unquote(gene)
    result = db.query(ActTableFull).filter(func.trim(ActTableFull.gene).ilike(f"%{decoded_gene}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="gene not found")
    return result

@app.get("/act_table_full/swissprot/{swissprot}")
def read_act_table_full_by_swissprot(swissprot: str, db: Session = Depends(get_db)):
    decoded_swissprot = unquote(swissprot)
    result = db.query(ActTableFull).filter(func.trim(ActTableFull.swissprot).ilike(f"%{decoded_swissprot}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="swissprot not found")
    return result

@app.get("/act_table_full/act_type/{act_type}")
def read_act_table_full_by_act_type(act_type: str, db: Session = Depends(get_db)):
    decoded_act_type = unquote(act_type)
    result = db.query(ActTableFull).filter(func.trim(ActTableFull.act_type).ilike(f"%{decoded_act_type}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="act_type not found")
    return result

@app.get("/act_table_full/organism/{organism}")
def read_act_table_full_by_organism(organism: str, db: Session = Depends(get_db)):
    decoded_organism = unquote(organism)
    result = db.query(ActTableFull).filter(func.trim(ActTableFull.organism).ilike(f"%{decoded_organism}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="organism not found")
    return result


# TABLE 2:  structures
@app.get("/structures")
def read_structures(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Structures).offset(skip).limit(limit).all()

@app.get("/structures/cd_id/{cd_id}")
def read_structures_by_cd_id(cd_id: int, db: Session = Depends(get_db)):
    result = db.query(Structures).filter(Structures.cd_id == cd_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="cd_id not found")
    return result

@app.get("/structures/id/{id}")
def read_structures_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(Structures).filter(Structures.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/structures/name/{name}")
def read_structures_by_name(name: str, db: Session = Depends(get_db)):
    decoded_name = unquote(name)
    result = db.query(Structures).filter(func.trim(Structures.name).ilike(f"%{decoded_name}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="name not found")
    return result

@app.get("/structures/smiles/{smiles}")
def read_structures_by_smiles(smiles: str, db: Session = Depends(get_db)):
    decoded_smiles = unquote(smiles)
    result = db.query(Structures).filter(func.trim(Structures.smiles).ilike(f"%{decoded_smiles}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="smiles not found")
    return result

@app.get("/structures/inchikey/{inchikey}")
def read_structures_by_inchikey(inchikey: str, db: Session = Depends(get_db)):
    decoded_inchikey = unquote(inchikey)
    result = db.query(Structures).filter(func.trim(Structures.inchikey).ilike(f"%{decoded_inchikey}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="inchikey not found")
    return result


# TABLE 3:  Identifier
@app.get("/identifier")
def read_identifier(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Identifier).offset(skip).limit(limit).all()

@app.get("/identifier/id/{id}")
def read_identifier_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(Identifier).filter(Identifier.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/identifier/identifier/{identifier}")
def read_identifier_by_identifier(identifier: str, db: Session = Depends(get_db)):
    decoded_identifier = unquote(identifier)
    result = db.query(Identifier).filter(func.trim(Identifier.identifier).ilike(f"%{decoded_identifier}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="identifier not found")
    return result

@app.get("/identifier/id_type/{id_type}")
def read_identifier_by_id_type(id_type: str, db: Session = Depends(get_db)):
    decoded_id_type = unquote(id_type)
    result = db.query(Identifier).filter(func.trim(Identifier.id_type).ilike(f"%{decoded_id_type}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="id_type not found")
    return result

@app.get("/identifier/struct_id/{struct_id}")
def read_identifier_by_struct_id(struct_id: int, db: Session = Depends(get_db)):
    result = db.query(Identifier).filter(Identifier.struct_id == struct_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="struct_id not found")
    return result


# Table 4: id_type
@app.get("/id_type")
def read_id_type(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(IdType).offset(skip).limit(limit).all()

@app.get("/id_type/id/{id}")
def read_id_type_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(IdType).filter(IdType.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/id_type/type/{type}")
def read_id_type_by_type(type: str, db: Session = Depends(get_db)):
    decoded_type = unquote(type)
    result = db.query(IdType).filter(func.trim(IdType.type).ilike(f"%{decoded_type}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="type not found")
    return result


# Table 5: synonyms
@app.get("/synonyms")
def read_synonyms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Synonyms).offset(skip).limit(limit).all()

@app.get("/synonyms/syn_id/{syn_id}")
def read_synonyms_by_syn_id(syn_id: int, db: Session = Depends(get_db)):
    result = db.query(Synonyms).filter(Synonyms.syn_id == syn_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="syn_id not found")
    return result

@app.get("/synonyms/id/{id}")
def read_synonyms_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(Synonyms).filter(Synonyms.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/synonyms/name/{name}")
def read_synonyms_by_name(name: str, db: Session = Depends(get_db)):
    decoded_name = unquote(name)
    result = db.query(Synonyms).filter(func.trim(Synonyms.name).ilike(f"%{decoded_name}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="name not found")
    return result

# Table 6: target_class
@app.get("/target_class")
def read_target_class(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(TargetClass).offset(skip).limit(limit).all()

@app.get("/target_class/id/{id}")
def read_target_class_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(TargetClass).filter(TargetClass.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/target_class/l1/{l1}")
def read_target_class_by_l1(l1: str, db: Session = Depends(get_db)):
    decoded_l1 = unquote(l1)
    result = db.query(TargetClass).filter(func.trim(TargetClass.l1).ilike(f"%{decoded_l1}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="l1 not found")
    return result


# Table 7: target_component
@app.get("/target_component")
def read_target_component(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(TargetComponent).offset(skip).limit(limit).all()

@app.get("/target_component/id/{id}")
def read_target_component_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(TargetComponent).filter(TargetComponent.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/target_component/accession/{accession}")
def read_target_component_by_accession(accession: str, db: Session = Depends(get_db)):
    decoded_accession = unquote(accession)
    result = db.query(TargetComponent).filter(func.trim(TargetComponent.accession).ilike(f"%{decoded_accession}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="accession not found")
    return result

@app.get("/target_component/swissprot/{swissprot}")
def read_target_component_by_swissprot(swissprot: str, db: Session = Depends(get_db)):
    decoded_swissprot = unquote(swissprot)
    result = db.query(TargetComponent).filter(func.trim(TargetComponent.swissprot).ilike(f"%{decoded_swissprot}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="swissprot not found")
    return result

@app.get("/target_component/organism/{organism}")
def read_target_component_by_organism(organism: str, db: Session = Depends(get_db)):
    decoded_organism = unquote(organism)
    result = db.query(TargetComponent).filter(func.trim(TargetComponent.organism).ilike(f"%{decoded_organism}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="organism not found")
    return result

@app.get("/target_component/gene/{gene}")
def read_target_component_by_gene(gene: str, db: Session = Depends(get_db)):
    decoded_gene = unquote(gene)
    result = db.query(TargetComponent).filter(func.trim(TargetComponent.gene).ilike(f"%{decoded_gene}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="gene not found")
    return result


# Table 8: target_dictionary
@app.get("/target_dictionary")
def read_target_dictionary(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(TargetDictionary).offset(skip).limit(limit).all()

@app.get("/target_dictionary/id/{id}")
def read_target_dictionary_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(TargetDictionary).filter(TargetDictionary.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/target_dictionary/target_class/{target_class}")
def read_target_dictionary_by_target_class(target_class: str, db: Session = Depends(get_db)):
    decoded_target_class = unquote(target_class)
    result = db.query(TargetDictionary).filter(func.trim(TargetDictionary.target_class).ilike(f"%{decoded_target_class}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="target_class not found")
    return result


# Table 9: target_go
@app.get("/target_go")
def read_target_go(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(TargetGo).offset(skip).limit(limit).all()

@app.get("/target_go/id/{id}")
def read_target_go_by_id(id: str, db: Session = Depends(get_db)):
    decoded_id = unquote(id)
    result = db.query(TargetGo).filter(func.trim(TargetGo.id).ilike(f"%{decoded_id}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/target_go/type/{type}")
def read_target_go_by_type(type: str, db: Session = Depends(get_db)):
    decoded_type = unquote(type)
    result = db.query(TargetGo).filter(func.trim(TargetGo.type).ilike(f"%{decoded_type}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="type not found")
    return result


# Table 10: target_keyword
@app.get("/target_keyword")
def read_target_keyword(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(TargetKeyword).offset(skip).limit(limit).all()

@app.get("/target_keyword/id/{id}")
def read_target_keyword_by_id(id: str, db: Session = Depends(get_db)):
    decoded_id = unquote(id)
    result = db.query(TargetKeyword).filter(func.trim(TargetKeyword.id).ilike(f"%{decoded_id}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/target_keyword/category/{category}")
def read_target_keyword_by_category(category: str, db: Session = Depends(get_db)):
    decoded_category = unquote(category)
    result = db.query(TargetKeyword).filter(func.trim(TargetKeyword.category).ilike(f"%{decoded_category}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="category not found")
    return result

@app.get("/target_keyword/keyword/{keyword}")
def read_target_keyword_by_keyword(keyword: str, db: Session = Depends(get_db)):
    decoded_keyword = unquote(keyword)
    result = db.query(TargetKeyword).filter(func.trim(TargetKeyword.keyword).ilike(f"%{decoded_keyword}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="keyword not found")
    return result


# Table 11: td2tc
@app.get("/td2tc")
def read_td2tc(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Td2tc).offset(skip).limit(limit).all()

@app.get("/td2tc/target_id/{target_id}")
def read_td2tc_by_target_id(target_id: int, db: Session = Depends(get_db)):
    result = db.query(Td2tc).filter(Td2tc.target_id == target_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="target_id not found")
    return result

@app.get("/td2tc/component_id/{component_id}")
def read_td2tc_by_component_id(component_id: int, db: Session = Depends(get_db)):
    result = db.query(Td2tc).filter(Td2tc.component_id == component_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="component_id not found")
    return result


# Table 12: tdgo2tc
@app.get("/tdgo2tc")
def read_tdgo2tc(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Tdgo2tc).offset(skip).limit(limit).all()

@app.get("/tdgo2tc/id/{id}")
def read_tdgo2tc_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(Tdgo2tc).filter(Tdgo2tc.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/tdgo2tc/go_id/{go_id}")
def read_tdgo2tc_by_go_id(go_id: str, db: Session = Depends(get_db)):
    decoded_go_id = unquote(go_id)
    result = db.query(Tdgo2tc).filter(func.trim(Tdgo2tc.go_id).ilike(f"%{decoded_go_id}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="go_id not found")
    return result

@app.get("/tdgo2tc/component_id/{component_id}")
def read_tdgo2tc_by_component_id(component_id: int, db: Session = Depends(get_db)):
    result = db.query(Tdgo2tc).filter(Tdgo2tc.component_id == component_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="component_id not found")
    return result



# Table 13: tdkey2tc
@app.get("/tdkey2tc")
def read_tdkey2tc(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Tdkey2tc).offset(skip).limit(limit).all()

@app.get("/tdkey2tc/id/{id}")
def read_tdkey2tc_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(Tdkey2tc).filter(Tdkey2tc.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/tdkey2tc/tdkey_id/{tdkey_id}")
def read_tdkey2tc_by_tdkey_id(tdkey_id: str, db: Session = Depends(get_db)):
    decoded_tdkey_id = unquote(tdkey_id)
    result = db.query(Tdkey2tc).filter(func.trim(Tdkey2tc.tdkey_id).ilike(f"%{decoded_tdkey_id}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="tdkey_id not found")
    return result

@app.get("/tdkey2tc/component_id/{component_id}")
def read_tdkey2tc_by_component_id(component_id: int, db: Session = Depends(get_db)):
    result = db.query(Tdkey2tc).filter(Tdkey2tc.component_id == component_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="component_id not found")
    return result



# Table 14: omop_relationship
@app.get("/omop_relationship")
def read_omop_relationship(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(OmopRelationship).offset(skip).limit(limit).all()

@app.get("/omop_relationship/id/{id}")
def read_omop_relationship_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(OmopRelationship).filter(OmopRelationship.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/omop_relationship/struct_id/{struct_id}")
def read_omop_relationship_by_struct_id(struct_id: int, db: Session = Depends(get_db)):
    result = db.query(OmopRelationship).filter(OmopRelationship.struct_id == struct_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="struct_id not found")
    return result

@app.get("/omop_relationship/concept_id/{concept_id}")
def read_omop_relationship_by_concept_id(concept_id: int, db: Session = Depends(get_db)):
    result = db.query(OmopRelationship).filter(OmopRelationship.concept_id == concept_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="concept_id not found")
    return result

@app.get("/omop_relationship/relationship_name/{relationship_name}")
def read_omop_relationship_by_relationship_name(relationship_name: str, db: Session = Depends(get_db)):
    decoded_relationship_name = unquote(relationship_name)
    result = db.query(OmopRelationship).filter(func.trim(OmopRelationship.relationship_name).ilike(f"%{decoded_relationship_name}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="relationship_name not found")
    return result

@app.get("/omop_relationship/concept_name/{concept_name}")
def read_omop_relationship_by_concept_name(concept_name: str, db: Session = Depends(get_db)):
    decoded_concept_name = unquote(concept_name)
    result = db.query(OmopRelationship).filter(func.trim(OmopRelationship.concept_name).ilike(f"%{decoded_concept_name}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="concept_name not found")
    return result

@app.get("/omop_relationship/umls_cui/{umls_cui}")
def read_omop_relationship_by_umls_cui(umls_cui: str, db: Session = Depends(get_db)):
    decoded_umls_cui = unquote(umls_cui)
    result = db.query(OmopRelationship).filter(func.trim(OmopRelationship.umls_cui).ilike(f"%{decoded_umls_cui}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="umls_cui not found")
    return result

@app.get("/omop_relationship/cui_semantic_type/{cui_semantic_type}")
def read_omop_relationship_by_cui_semantic_type(cui_semantic_type: str, db: Session = Depends(get_db)):
    decoded_cui_semantic_type = unquote(cui_semantic_type)
    result = db.query(OmopRelationship).filter(func.trim(OmopRelationship.cui_semantic_type).ilike(f"%{decoded_cui_semantic_type}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="cui_semantic_type not found")
    return result

@app.get("/omop_relationship/snomed_conceptid/{snomed_conceptid}")
def read_omop_relationship_by_snomed_conceptid(snomed_conceptid: int, db: Session = Depends(get_db)):
    result = db.query(OmopRelationship).filter(OmopRelationship.snomed_conceptid == snomed_conceptid).all()
    if not result:
        raise HTTPException(status_code=404, detail="snomed_conceptid not found")
    return result



# Table 15: product
@app.get("/product")
def read_product(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all()

@app.get("/product/id/{id}")
def read_product_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(Product).filter(Product.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/product/ndc_product_code/{ndc_product_code}")
def read_product_by_ndc_product_code(ndc_product_code: str, db: Session = Depends(get_db)):
    decoded_ndc_product_code = unquote(ndc_product_code)
    result = db.query(Product).filter(func.trim(Product.ndc_product_code).ilike(f"%{decoded_ndc_product_code}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="ndc_product_code not found")
    return result

@app.get("/product/product_name/{product_name}")
def read_product_by_product_name(product_name: str, db: Session = Depends(get_db)):
    decoded_product_name = unquote(product_name)
    result = db.query(Product).filter(func.trim(Product.product_name).ilike(f"%{decoded_product_name}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="product_name not found")
    return result

@app.get("/product/route/{route}")
def read_product_by_route(route: str, db: Session = Depends(get_db)):
    decoded_route = unquote(route)
    result = db.query(Product).filter(func.trim(Product.route).ilike(f"%{decoded_route}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="route not found")
    return result



# Table 16: struct2obprod
@app.get("/struct2obprod")
def read_struct2obprod(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Struct2obprod).offset(skip).limit(limit).all()

@app.get("/struct2obprod/struct_id/{struct_id}")
def read_struct2obprod_by_struct_id(struct_id: int, db: Session = Depends(get_db)):
    result = db.query(Struct2obprod).filter(Struct2obprod.struct_id == struct_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="struct_id not found")
    return result

@app.get("/struct2obprod/prod_id/{prod_id}")
def read_struct2obprod_by_prod_id(prod_id: int, db: Session = Depends(get_db)):
    result = db.query(Struct2obprod).filter(Struct2obprod.prod_id == prod_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="prod_id not found")
    return result



# Table 17: atc
@app.get("/atc")
def read_atc(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Atc).offset(skip).limit(limit).all()

@app.get("/atc/id/{id}")
def read_atc_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(Atc).filter(Atc.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/atc/code/{code}")
def read_atc_by_code(code: str, db: Session = Depends(get_db)):
    decoded_code = unquote(code)
    result = db.query(Atc).filter(func.trim(Atc.code).ilike(f"%{decoded_code}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="code not found")
    return result

@app.get("/atc/chemical_substance/{chemical_substance}")
def read_atc_by_chemical_substance(chemical_substance: str, db: Session = Depends(get_db)):
    decoded_chemical_substance = unquote(chemical_substance)
    result = db.query(Atc).filter(func.trim(Atc.chemical_substance).ilike(f"%{decoded_chemical_substance}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="chemical_substance not found")
    return result


# Table 18: struct2atc
@app.get("/struct2atc")
def read_struct2atc(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Struct2atc).offset(skip).limit(limit).all()

@app.get("/struct2atc/struct_id/{struct_id}")
def read_struct2atc_by_struct_id(struct_id: int, db: Session = Depends(get_db)):
    result = db.query(Struct2atc).filter(Struct2atc.struct_id == struct_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="struct_id not found")
    return result

@app.get("/struct2atc/atc_code/{atc_code}")
def read_struct2atc_by_atc_code(atc_code: str, db: Session = Depends(get_db)):
    decoded_atc_code = unquote(atc_code)
    result = db.query(Struct2atc).filter(func.trim(Struct2atc.atc_code).ilike(f"%{decoded_atc_code}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="atc_code not found")
    return result



# Table 19: drug_class
@app.get("/drug_class")
def read_drug_class(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(DrugClass).offset(skip).limit(limit).all()

@app.get("/drug_class/id/{id}")
def read_drug_class_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(DrugClass).filter(DrugClass.id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return result

@app.get("/drug_class/name/{name}")
def read_drug_class_by_name(name: str, db: Session = Depends(get_db)):
    decoded_name = unquote(name)
    result = db.query(DrugClass).filter(func.trim(DrugClass.name).ilike(f"%{decoded_name}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="name not found")
    return result

@app.get("/drug_class/source/{source}")
def read_drug_class_by_source(source: str, db: Session = Depends(get_db)):
    decoded_source = unquote(source)
    result = db.query(DrugClass).filter(func.trim(DrugClass.source).ilike(f"%{decoded_source}%")).all()
    if not result:
        raise HTTPException(status_code=404, detail="source not found")
    return result












