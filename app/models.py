from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, CHAR, Column, Date, DateTime, Double, ForeignKeyConstraint, Index, Integer, LargeBinary, PrimaryKeyConstraint, REAL, SmallInteger, String, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class ActionType(Base):
    __tablename__ = 'action_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql141210123613760'),
        UniqueConstraint('action_type', name='sql141210123613761'),
        {'comment': 'drug modulatory action types'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_type: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(200))
    parent_type: Mapped[Optional[str]] = mapped_column(String(50))

    act_table_full: Mapped[List['ActTableFull']] = relationship('ActTableFull', back_populates='action_type_')


class ApprovalType(Base):
    __tablename__ = 'approval_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql141031231522060'),
        UniqueConstraint('descr', name='sql141031231522061'),
        {'comment': 'listing of drug regulatory agencies'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descr: Mapped[Optional[str]] = mapped_column(String(200))

    approval: Mapped[List['Approval']] = relationship('Approval', back_populates='approval_type')


class Atc(Base):
    __tablename__ = 'atc'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql130424125636180'),
        UniqueConstraint('code', name='sql130424125636181'),
        {'comment': 'WHO ATC codes'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(CHAR(7))
    chemical_substance: Mapped[str] = mapped_column(String(250))
    l1_code: Mapped[str] = mapped_column(CHAR(1))
    l1_name: Mapped[str] = mapped_column(String(200))
    l2_code: Mapped[str] = mapped_column(CHAR(3))
    l2_name: Mapped[str] = mapped_column(String(200))
    l3_code: Mapped[str] = mapped_column(CHAR(4))
    l3_name: Mapped[str] = mapped_column(String(200))
    l4_code: Mapped[str] = mapped_column(CHAR(5))
    l4_name: Mapped[str] = mapped_column(String(200))
    chemical_substance_count: Mapped[Optional[int]] = mapped_column(Integer)

    struct2atc: Mapped[List['Struct2atc']] = relationship('Struct2atc', back_populates='atc')


class AttrType(Base):
    __tablename__ = 'attr_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql140410123913680'),
        UniqueConstraint('name', name='sql140410123913681'),
        {'comment': 'listing of generic attribute types'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(20))


class DataSource(Base):
    __tablename__ = 'data_source'
    __table_args__ = (
        PrimaryKeyConstraint('src_id', name='sql100517171435170'),
        {'comment': 'listing of datasources'}
    )

    src_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    source_name: Mapped[Optional[str]] = mapped_column(String(100))


class Dbversion(Base):
    __tablename__ = 'dbversion'
    __table_args__ = (
        PrimaryKeyConstraint('version', name='sql160415165555160'),
        {'comment': 'current database version'}
    )

    version: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    dtime: Mapped[datetime.datetime] = mapped_column(DateTime)


class DdiRisk(Base):
    __tablename__ = 'ddi_risk'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql140411131027290'),
        UniqueConstraint('risk', 'ddi_ref_id', name='ddi_risk_uq'),
        {'comment': 'Qualitative assesments of drug-drug interactions severity'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    risk: Mapped[str] = mapped_column(String(200))
    ddi_ref_id: Mapped[int] = mapped_column(Integer)

    ddi: Mapped[List['Ddi']] = relationship('Ddi', back_populates='ddi_risk_')


class Doid(Base):
    __tablename__ = 'doid'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql150425232401220'),
        UniqueConstraint('doid', name='sql150425232401221'),
        {'comment': 'listing on Disease-Ontology concepts'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[Optional[str]] = mapped_column(String(1000))
    doid: Mapped[Optional[str]] = mapped_column(String(50))
    url: Mapped[Optional[str]] = mapped_column(String(100))

    doid_xref: Mapped[List['DoidXref']] = relationship('DoidXref', back_populates='doid_')


class DrugClass(Base):
    __tablename__ = 'drug_class'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql140409195222370'),
        UniqueConstraint('name', name='sql140409195222371'),
        {'comment': 'groupings of drugs used to derive Drug-Drug and Drug class - Drug '
                'class interactions'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(500))
    is_group: Mapped[int] = mapped_column(SmallInteger, server_default=text('0'))
    source: Mapped[Optional[str]] = mapped_column(String(100))

    ddi: Mapped[List['Ddi']] = relationship('Ddi', foreign_keys='[Ddi.drug_class1]', back_populates='drug_class')
    ddi_: Mapped[List['Ddi']] = relationship('Ddi', foreign_keys='[Ddi.drug_class2]', back_populates='drug_class_')
    struct2drgclass: Mapped[List['Struct2drgclass']] = relationship('Struct2drgclass', back_populates='drug_class')


t_faers_top = Table(
    'faers_top', Base.metadata,
    Column('struct_id', Integer),
    Column('meddra_name', String(200))
)


class IdType(Base):
    __tablename__ = 'id_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql140607012055120'),
        UniqueConstraint('type', name='sql140607012055121'),
        {'comment': 'list external identifiers sources'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    url: Mapped[Optional[str]] = mapped_column(String(500))

    identifier: Mapped[List['Identifier']] = relationship('Identifier', back_populates='id_type_')


class InnStem(Base):
    __tablename__ = 'inn_stem'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql140212001438200'),
        UniqueConstraint('stem', name='sql140212001438201'),
        {'comment': 'listing of WHO INN stems based on '
                'http://www.who.int/medicines/services/inn/stembook/en/'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    definition: Mapped[str] = mapped_column(String(1000))
    stem: Mapped[Optional[str]] = mapped_column(String(50))
    national_name: Mapped[Optional[str]] = mapped_column(String(20))
    length: Mapped[Optional[int]] = mapped_column(SmallInteger)
    discontinued: Mapped[Optional[bool]] = mapped_column(Boolean)

    structures: Mapped[List['Structures']] = relationship('Structures', back_populates='inn_stem')


class Label(Base):
    __tablename__ = 'label'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql120404123647220'),
        {'comment': 'FDA drug labels SPL identifiers and categories'}
    )

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    title: Mapped[Optional[str]] = mapped_column(String(1000))
    effective_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    assigned_entity: Mapped[Optional[str]] = mapped_column(String(500))
    pdf_url: Mapped[Optional[str]] = mapped_column(String(500))

    prd2label: Mapped[List['Prd2label']] = relationship('Prd2label', back_populates='label')
    section: Mapped[List['Section']] = relationship('Section', back_populates='label')


class LincsSignature(Base):
    __tablename__ = 'lincs_signature'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql180509154922470'),
        UniqueConstraint('struct_id1', 'struct_id2', 'is_parent1', 'is_parent2', 'cell_id', name='sql180509154922471')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    struct_id1: Mapped[Optional[int]] = mapped_column(Integer)
    struct_id2: Mapped[Optional[int]] = mapped_column(Integer)
    is_parent1: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_parent2: Mapped[Optional[bool]] = mapped_column(Boolean)
    cell_id: Mapped[Optional[str]] = mapped_column(String(10))
    rmsd: Mapped[Optional[float]] = mapped_column(Double(53))
    rmsd_norm: Mapped[Optional[float]] = mapped_column(Double(53))
    pearson: Mapped[Optional[float]] = mapped_column(Double(53))
    euclid: Mapped[Optional[float]] = mapped_column(Double(53))


class ObExclusivityCode(Base):
    __tablename__ = 'ob_exclusivity_code'
    __table_args__ = (
        PrimaryKeyConstraint('code', name='sql161127133109120'),
        {'comment': 'Exclusivity codes from FDA Orange book'}
    )

    code: Mapped[str] = mapped_column(String(10), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(String(500))

    ob_exclusivity: Mapped[List['ObExclusivity']] = relationship('ObExclusivity', back_populates='ob_exclusivity_code')


t_ob_exclusivity_view = Table(
    'ob_exclusivity_view', Base.metadata,
    Column('struct_id', Integer),
    Column('strength', String(4000)),
    Column('trade_name', String(200)),
    Column('applicant', String(50)),
    Column('appl_type', CHAR(1)),
    Column('appl_no', CHAR(6)),
    Column('approval_date', Date),
    Column('type', String(5)),
    Column('dose_form', String(50)),
    Column('route', String(100)),
    Column('exclusivity_date', Date),
    Column('description', String(500))
)


class ObPatentUseCode(Base):
    __tablename__ = 'ob_patent_use_code'
    __table_args__ = (
        PrimaryKeyConstraint('code', name='sql161127133626130'),
        {'comment': 'Patent use codes from FDA Orange book'}
    )

    code: Mapped[str] = mapped_column(String(10), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(String(500))

    ob_patent: Mapped[List['ObPatent']] = relationship('ObPatent', back_populates='ob_patent_use_code')


t_ob_patent_view = Table(
    'ob_patent_view', Base.metadata,
    Column('struct_id', Integer),
    Column('strength', String(4000)),
    Column('patent_no', String(200)),
    Column('description', String(500)),
    Column('trade_name', String(200)),
    Column('applicant', String(50)),
    Column('appl_type', CHAR(1)),
    Column('appl_no', CHAR(6)),
    Column('type', String(5)),
    Column('dose_form', String(50)),
    Column('route', String(100)),
    Column('approval_date', Date),
    Column('patent_expire_date', Date)
)


class ObProduct(Base):
    __tablename__ = 'ob_product'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql161126154442460'),
        Index('ob_product_appno_idx', 'appl_no'),
        Index('ob_product_prodno_idx', 'product_no'),
        {'comment': 'FDA Orange book pharmaceutical products'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ingredient: Mapped[Optional[str]] = mapped_column(String(500))
    trade_name: Mapped[Optional[str]] = mapped_column(String(200))
    applicant: Mapped[Optional[str]] = mapped_column(String(50))
    strength: Mapped[Optional[str]] = mapped_column(String(500))
    appl_type: Mapped[Optional[str]] = mapped_column(CHAR(1))
    appl_no: Mapped[Optional[str]] = mapped_column(CHAR(6))
    te_code: Mapped[Optional[str]] = mapped_column(String(20))
    approval_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    rld: Mapped[Optional[int]] = mapped_column(SmallInteger)
    type: Mapped[Optional[str]] = mapped_column(String(5))
    applicant_full_name: Mapped[Optional[str]] = mapped_column(String(200))
    dose_form: Mapped[Optional[str]] = mapped_column(String(50))
    route: Mapped[Optional[str]] = mapped_column(String(100))
    product_no: Mapped[Optional[str]] = mapped_column(CHAR(3))

    struct2obprod: Mapped[List['Struct2obprod']] = relationship('Struct2obprod', back_populates='prod')


t_omop_relationship_doid_view = Table(
    'omop_relationship_doid_view', Base.metadata,
    Column('id', Integer),
    Column('struct_id', Integer),
    Column('concept_id', Integer),
    Column('relationship_name', String(256)),
    Column('concept_name', String(256)),
    Column('umls_cui', CHAR(8)),
    Column('snomed_full_name', String(500)),
    Column('cui_semantic_type', CHAR(4)),
    Column('snomed_conceptid', BigInteger),
    Column('doid', Text)
)


class Parentmol(Base):
    __tablename__ = 'parentmol'
    __table_args__ = (
        PrimaryKeyConstraint('cd_id', name='sql150523184351770'),
        UniqueConstraint('cas_reg_no', name='sql150523184644290'),
        UniqueConstraint('name', name='sql150523184621160'),
        {'comment': 'parent drug molecules for active ingredients formulated as '
                'prodrugs'}
    )

    cd_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(250))
    cas_reg_no: Mapped[Optional[str]] = mapped_column(String(50))
    inchi: Mapped[Optional[str]] = mapped_column(String(32672))
    nostereo_inchi: Mapped[Optional[str]] = mapped_column(String(32672))
    molfile: Mapped[Optional[str]] = mapped_column(Text)
    molimg: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    smiles: Mapped[Optional[str]] = mapped_column(String(32672))
    inchikey: Mapped[Optional[str]] = mapped_column(CHAR(27))

    struct: Mapped[List['Structures']] = relationship('Structures', secondary='struct2parent', back_populates='parent')
    synonyms: Mapped[List['Synonyms']] = relationship('Synonyms', back_populates='parent')


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql120412001426700'),
        UniqueConstraint('ndc_product_code', name='prd_ndc_uniq'),
        Index('sql120412004620930', 'ndc_product_code', unique=True),
        {'comment': 'pharmaceutical products associated with FDA drug labels'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ndc_product_code: Mapped[str] = mapped_column(String(20))
    form: Mapped[Optional[str]] = mapped_column(String(250))
    generic_name: Mapped[Optional[str]] = mapped_column(String(4000))
    product_name: Mapped[Optional[str]] = mapped_column(String(1000))
    route: Mapped[Optional[str]] = mapped_column(String(50))
    marketing_status: Mapped[Optional[str]] = mapped_column(String(500))
    active_ingredient_count: Mapped[Optional[int]] = mapped_column(Integer)

    prd2label: Mapped[List['Prd2label']] = relationship('Prd2label', back_populates='product')
    active_ingredient: Mapped[List['ActiveIngredient']] = relationship('ActiveIngredient', back_populates='product')


class PropertyType(Base):
    __tablename__ = 'property_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='symbol'),
        UniqueConstraint('symbol', name='symbol_unique')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[Optional[str]] = mapped_column(String(20))
    name: Mapped[Optional[str]] = mapped_column(String(80))
    symbol: Mapped[Optional[str]] = mapped_column(String(10))
    units: Mapped[Optional[str]] = mapped_column(String(10))


class ProteinType(Base):
    __tablename__ = 'protein_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql141203213631730'),
        UniqueConstraint('type', name='sql141203213631731'),
        {'comment': 'simple classification of protein types interacting with drugs'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(50))


class RefType(Base):
    __tablename__ = 'ref_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql140401160903570'),
        UniqueConstraint('type', name='sql140401160903571'),
        {'comment': 'listing of reference types'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(50))

    reference: Mapped[List['Reference']] = relationship('Reference', back_populates='ref_type')


class StructTypeDef(Base):
    __tablename__ = 'struct_type_def'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql141016095933600'),
        UniqueConstraint('type', name='sql141016095933601'),
        {'comment': 'simple classification of chemical entities in structures table'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[Optional[str]] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(200))

    structure_type: Mapped[List['StructureType']] = relationship('StructureType', back_populates='struct_type_def')


class TargetClass(Base):
    __tablename__ = 'target_class'
    __table_args__ = (
        PrimaryKeyConstraint('l1', name='sql130710170452610'),
        {'comment': 'ChEMBL-db target classification system, level 1 only'}
    )

    l1: Mapped[str] = mapped_column(String(50), primary_key=True)
    id: Mapped[int] = mapped_column(Integer)

    act_table_full: Mapped[List['ActTableFull']] = relationship('ActTableFull', back_populates='target_class_')


class TargetComponent(Base):
    __tablename__ = 'target_component'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql141203005155660'),
        UniqueConstraint('accession', name='sql141203005155670'),
        UniqueConstraint('swissprot', name='sql141203005155671'),
        {'comment': 'protein components of taregt interacting with drugs'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    accession: Mapped[Optional[str]] = mapped_column(String(20))
    swissprot: Mapped[Optional[str]] = mapped_column(String(20))
    organism: Mapped[Optional[str]] = mapped_column(String(150))
    name: Mapped[Optional[str]] = mapped_column(String(200))
    gene: Mapped[Optional[str]] = mapped_column(String(25))
    geneid: Mapped[Optional[int]] = mapped_column(BigInteger)
    tdl: Mapped[Optional[str]] = mapped_column(String(5))

    tdgo2tc: Mapped[List['Tdgo2tc']] = relationship('Tdgo2tc', back_populates='component')
    tdkey2tc: Mapped[List['Tdkey2tc']] = relationship('Tdkey2tc', back_populates='component')


class TargetDictionary(Base):
    __tablename__ = 'target_dictionary'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql141205191111190'),
        {'comment': 'target entities interacting with drugs'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    target_class: Mapped[str] = mapped_column(String(50), server_default=text("'Unclassified'::character varying"))
    protein_components: Mapped[int] = mapped_column(SmallInteger, server_default=text('0'))
    protein_type: Mapped[Optional[str]] = mapped_column(String(50))
    tdl: Mapped[Optional[str]] = mapped_column(String(500))

    td2tc: Mapped[List['Td2tc']] = relationship('Td2tc', back_populates='target')
    act_table_full: Mapped[List['ActTableFull']] = relationship('ActTableFull', back_populates='target')


class TargetGo(Base):
    __tablename__ = 'target_go'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql141211234759820'),
        {'comment': 'Gene Ontology terms'}
    )

    id: Mapped[str] = mapped_column(CHAR(10), primary_key=True)
    term: Mapped[Optional[str]] = mapped_column(String(200))
    type: Mapped[Optional[str]] = mapped_column(CHAR(1))

    tdgo2tc: Mapped[List['Tdgo2tc']] = relationship('Tdgo2tc', back_populates='go')


class TargetKeyword(Base):
    __tablename__ = 'target_keyword'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sql141211160454700'),
        {'comment': 'keywords extracted from Unirpot protein entries'}
    )

    id: Mapped[str] = mapped_column(CHAR(7), primary_key=True)
    descr: Mapped[Optional[str]] = mapped_column(String(4000))
    category: Mapped[Optional[str]] = mapped_column(String(50))
    keyword: Mapped[Optional[str]] = mapped_column(String(200))

    tdkey2tc: Mapped[List['Tdkey2tc']] = relationship('Tdkey2tc', back_populates='tdkey')


class VetprodType(Base):
    __tablename__ = 'vetprod_type'
    __table_args__ = (
        PrimaryKeyConstraint('appl_type', name='SQL0000000007-f0b3c086-0182-8659-7929-00007c5ff800'),
        Index('SQL0000000006-48928085-0182-8659-7929-00007c5ff800', 'id', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer)
    appl_type: Mapped[str] = mapped_column(CHAR(1), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(String(11))

    vetprod: Mapped[List['Vetprod']] = relationship('Vetprod', back_populates='vetprod_type')


class Ddi(Base):
    __tablename__ = 'ddi'
    __table_args__ = (
        ForeignKeyConstraint(['ddi_risk', 'ddi_ref_id'], ['ddi_risk.risk', 'ddi_risk.ddi_ref_id'], name='ddi_2_ddi_risk'),
        ForeignKeyConstraint(['drug_class1'], ['drug_class.name'], name='ddi_2_drug_class1'),
        ForeignKeyConstraint(['drug_class2'], ['drug_class.name'], name='ddi_2_drug_class2'),
        PrimaryKeyConstraint('id', name='sql140411131553960'),
        UniqueConstraint('drug_class1', 'drug_class2', 'ddi_ref_id', name='ddi_tuple_uq'),
        {'comment': 'Drug-Drug and Drug class - Drug class interaction table'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drug_class1: Mapped[str] = mapped_column(String(500))
    drug_class2: Mapped[str] = mapped_column(String(500))
    ddi_ref_id: Mapped[int] = mapped_column(Integer)
    ddi_risk: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(String(4000))
    source_id: Mapped[Optional[str]] = mapped_column(String(200))

    ddi_risk_: Mapped['DdiRisk'] = relationship('DdiRisk', back_populates='ddi')
    drug_class: Mapped['DrugClass'] = relationship('DrugClass', foreign_keys=[drug_class1], back_populates='ddi')
    drug_class_: Mapped['DrugClass'] = relationship('DrugClass', foreign_keys=[drug_class2], back_populates='ddi_')


class DoidXref(Base):
    __tablename__ = 'doid_xref'
    __table_args__ = (
        ForeignKeyConstraint(['doid'], ['doid.doid'], name='doid_xref_2_doid'),
        PrimaryKeyConstraint('id', name='sql150426005334630'),
        UniqueConstraint('doid', 'source', 'xref', name='sql150426005334632'),
        Index('xref_source_idx', 'xref', 'source'),
        {'comment': 'Disease-Ontology terms mappings to external resources'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    doid: Mapped[Optional[str]] = mapped_column(String(50))
    source: Mapped[Optional[str]] = mapped_column(String(50))
    xref: Mapped[Optional[str]] = mapped_column(String(50))

    doid_: Mapped[Optional['Doid']] = relationship('Doid', back_populates='doid_xref')


class ObExclusivity(Base):
    __tablename__ = 'ob_exclusivity'
    __table_args__ = (
        ForeignKeyConstraint(['exclusivity_code'], ['ob_exclusivity_code.code'], name='obexcl_2_exclcode'),
        PrimaryKeyConstraint('id', name='sql161127115514940'),
        {'comment': 'Exclusivity data for FDA Orange book pharmaceutical products'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    appl_type: Mapped[Optional[str]] = mapped_column(CHAR(1))
    appl_no: Mapped[Optional[str]] = mapped_column(CHAR(6))
    product_no: Mapped[Optional[str]] = mapped_column(CHAR(3))
    exclusivity_code: Mapped[Optional[str]] = mapped_column(String(10))
    exclusivity_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    ob_exclusivity_code: Mapped[Optional['ObExclusivityCode']] = relationship('ObExclusivityCode', back_populates='ob_exclusivity')


class ObPatent(Base):
    __tablename__ = 'ob_patent'
    __table_args__ = (
        ForeignKeyConstraint(['patent_use_code'], ['ob_patent_use_code.code'], name='obpat_2_usecode'),
        PrimaryKeyConstraint('id', name='sql161127120038110'),
        Index('ob_patent_applno_idx', 'appl_no'),
        Index('ob_patent_prodno_idx', 'product_no'),
        {'comment': 'Patent data for FDA Orange book pharmaceutical products'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    appl_type: Mapped[Optional[str]] = mapped_column(CHAR(1))
    appl_no: Mapped[Optional[str]] = mapped_column(CHAR(6))
    product_no: Mapped[Optional[str]] = mapped_column(CHAR(3))
    patent_no: Mapped[Optional[str]] = mapped_column(String(200))
    patent_expire_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    drug_substance_flag: Mapped[Optional[str]] = mapped_column(CHAR(1))
    drug_product_flag: Mapped[Optional[str]] = mapped_column(CHAR(1))
    patent_use_code: Mapped[Optional[str]] = mapped_column(String(10))
    delist_flag: Mapped[Optional[str]] = mapped_column(CHAR(1))

    ob_patent_use_code: Mapped[Optional['ObPatentUseCode']] = relationship('ObPatentUseCode', back_populates='ob_patent')


class Prd2label(Base):
    __tablename__ = 'prd2label'
    __table_args__ = (
        ForeignKeyConstraint(['label_id'], ['label.id'], name='prd_2_label'),
        ForeignKeyConstraint(['ndc_product_code'], ['product.ndc_product_code'], name='prd_2_prd'),
        PrimaryKeyConstraint('ndc_product_code', 'label_id', name='sql130919144750040'),
        UniqueConstraint('id', name='prd2label_id_key'),
        {'comment': 'mappings between FDA drug labels and pharmaceutical products '
                'associated with these labels'}
    )

    ndc_product_code: Mapped[str] = mapped_column(String(20), primary_key=True)
    label_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    id: Mapped[int] = mapped_column(Integer)

    label: Mapped['Label'] = relationship('Label', back_populates='prd2label')
    product: Mapped['Product'] = relationship('Product', back_populates='prd2label')


class Reference(Base):
    __tablename__ = 'reference'
    __table_args__ = (
        ForeignKeyConstraint(['type'], ['ref_type.type'], name='reference_2_reftype'),
        PrimaryKeyConstraint('id', name='sql141129210458570'),
        UniqueConstraint('document_id', name='sql141129210458573'),
        UniqueConstraint('doi', name='sql141129210458572'),
        UniqueConstraint('isbn10', name='sql141129210458574'),
        UniqueConstraint('pmid', name='sql141129210458571'),
        {'comment': 'external references for drug bioactivities and mechanism of '
                'action'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pmid: Mapped[Optional[int]] = mapped_column(Integer)
    doi: Mapped[Optional[str]] = mapped_column(String(50))
    document_id: Mapped[Optional[str]] = mapped_column(String(200))
    type: Mapped[Optional[str]] = mapped_column(String(50))
    authors: Mapped[Optional[str]] = mapped_column(String(4000))
    title: Mapped[Optional[str]] = mapped_column(String(500))
    isbn10: Mapped[Optional[str]] = mapped_column(CHAR(10))
    url: Mapped[Optional[str]] = mapped_column(String(1000))
    journal: Mapped[Optional[str]] = mapped_column(String(100))
    volume: Mapped[Optional[str]] = mapped_column(String(20))
    issue: Mapped[Optional[str]] = mapped_column(String(20))
    dp_year: Mapped[Optional[int]] = mapped_column(Integer)
    pages: Mapped[Optional[str]] = mapped_column(String(50))

    ref_type: Mapped[Optional['RefType']] = relationship('RefType', back_populates='reference')
    act_table_full: Mapped[List['ActTableFull']] = relationship('ActTableFull', foreign_keys='[ActTableFull.act_ref_id]', back_populates='act_ref')
    act_table_full_: Mapped[List['ActTableFull']] = relationship('ActTableFull', foreign_keys='[ActTableFull.moa_ref_id]', back_populates='moa_ref')


class Section(Base):
    __tablename__ = 'section'
    __table_args__ = (
        ForeignKeyConstraint(['label_id'], ['label.id'], name='section_2_label'),
        PrimaryKeyConstraint('id', name='sql120404123658530'),
        Index('sql120404123658531', 'label_id'),
        {'comment': 'FDA SPL drug label sections'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text_: Mapped[Optional[str]] = mapped_column('text', Text)
    label_id: Mapped[Optional[str]] = mapped_column(String(50))
    code: Mapped[Optional[str]] = mapped_column(String(20))
    title: Mapped[Optional[str]] = mapped_column(String(4000))

    label: Mapped[Optional['Label']] = relationship('Label', back_populates='section')


class Structures(Base):
    __tablename__ = 'structures'
    __table_args__ = (
        ForeignKeyConstraint(['stem'], ['inn_stem.stem'], name='struct_2_stem'),
        PrimaryKeyConstraint('cd_id', name='sql100501171817150'),
        UniqueConstraint('cas_reg_no', name='cas_reg_no_uq'),
        UniqueConstraint('id', name='uniq_structures_id'),
        Index('sql100501183943930', 'id', unique=True),
        Index('sql120418113711390', 'cas_reg_no'),
        {'comment': 'chemical entities in active pharmaceutical ingredients table'}
    )

    cd_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id: Mapped[int] = mapped_column(Integer)
    enhanced_stereo: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    cd_formula: Mapped[Optional[str]] = mapped_column(String(100))
    cd_molweight: Mapped[Optional[float]] = mapped_column(Double(53))
    clogp: Mapped[Optional[float]] = mapped_column(Double(53))
    alogs: Mapped[Optional[float]] = mapped_column(Double(53))
    cas_reg_no: Mapped[Optional[str]] = mapped_column(String(50))
    tpsa: Mapped[Optional[float]] = mapped_column(REAL)
    lipinski: Mapped[Optional[int]] = mapped_column(Integer)
    name: Mapped[Optional[str]] = mapped_column(String(250))
    no_formulations: Mapped[Optional[int]] = mapped_column(Integer)
    stem: Mapped[Optional[str]] = mapped_column(String(50))
    molfile: Mapped[Optional[str]] = mapped_column(Text)
    mrdef: Mapped[Optional[str]] = mapped_column(String(32672))
    arom_c: Mapped[Optional[int]] = mapped_column(Integer)
    sp3_c: Mapped[Optional[int]] = mapped_column(Integer)
    sp2_c: Mapped[Optional[int]] = mapped_column(Integer)
    sp_c: Mapped[Optional[int]] = mapped_column(Integer)
    halogen: Mapped[Optional[int]] = mapped_column(Integer)
    hetero_sp2_c: Mapped[Optional[int]] = mapped_column(Integer)
    rotb: Mapped[Optional[int]] = mapped_column(Integer)
    # molimg: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    o_n: Mapped[Optional[int]] = mapped_column(Integer)
    oh_nh: Mapped[Optional[int]] = mapped_column(Integer)
    inchi: Mapped[Optional[str]] = mapped_column(String(32672))
    smiles: Mapped[Optional[str]] = mapped_column(String(32672))
    rgb: Mapped[Optional[int]] = mapped_column(Integer, comment='number of rigid bonds')
    fda_labels: Mapped[Optional[int]] = mapped_column(Integer)
    inchikey: Mapped[Optional[str]] = mapped_column(String(27))
    status: Mapped[Optional[str]] = mapped_column(String(10))

    parent: Mapped[List['Parentmol']] = relationship('Parentmol', secondary='struct2parent', back_populates='struct')
    inn_stem: Mapped[Optional['InnStem']] = relationship('InnStem', back_populates='structures')
    vetprod: Mapped[List['Vetprod']] = relationship('Vetprod', secondary='vetprod2struct', back_populates='struct')
    act_table_full: Mapped[List['ActTableFull']] = relationship('ActTableFull', back_populates='struct')
    active_ingredient: Mapped[List['ActiveIngredient']] = relationship('ActiveIngredient', back_populates='struct')
    approval: Mapped[List['Approval']] = relationship('Approval', back_populates='struct')
    atc_ddd: Mapped[List['AtcDdd']] = relationship('AtcDdd', back_populates='struct')
    faers: Mapped[List['Faers']] = relationship('Faers', back_populates='struct')
    faers_female: Mapped[List['FaersFemale']] = relationship('FaersFemale', back_populates='struct')
    faers_male: Mapped[List['FaersMale']] = relationship('FaersMale', back_populates='struct')
    identifier: Mapped[List['Identifier']] = relationship('Identifier', back_populates='struct')
    omop_relationship: Mapped[List['OmopRelationship']] = relationship('OmopRelationship', back_populates='struct')
    pdb: Mapped[List['Pdb']] = relationship('Pdb', back_populates='struct')
    pharma_class: Mapped[List['PharmaClass']] = relationship('PharmaClass', back_populates='struct')
    pka: Mapped[List['Pka']] = relationship('Pka', back_populates='struct')
    struct2atc: Mapped[List['Struct2atc']] = relationship('Struct2atc', back_populates='struct')
    struct2drgclass: Mapped[List['Struct2drgclass']] = relationship('Struct2drgclass', back_populates='struct')
    struct2obprod: Mapped[List['Struct2obprod']] = relationship('Struct2obprod', back_populates='struct')
    structure_type: Mapped[List['StructureType']] = relationship('StructureType', back_populates='struct')
    synonyms: Mapped[List['Synonyms']] = relationship('Synonyms', back_populates='structures')
    vetomop: Mapped[List['Vetomop']] = relationship('Vetomop', back_populates='struct')


class Td2tc(Base):
    __tablename__ = 'td2tc'
    __table_args__ = (
        ForeignKeyConstraint(['target_id'], ['target_dictionary.id'], name='td2tc_2_td'),
        PrimaryKeyConstraint('target_id', 'component_id', name='sql141205191436250'),
        {'comment': 'mapping between drug target entities and protein components'}
    )

    target_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    component_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    target: Mapped['TargetDictionary'] = relationship('TargetDictionary', back_populates='td2tc')


class Tdgo2tc(Base):
    __tablename__ = 'tdgo2tc'
    __table_args__ = (
        ForeignKeyConstraint(['component_id'], ['target_component.id'], name='tdgo2tc_2_tc'),
        ForeignKeyConstraint(['go_id'], ['target_go.id'], name='tdgo2tc_2_go'),
        PrimaryKeyConstraint('id', name='sql141211235052890'),
        {'comment': 'mapping between protein components and GO terms'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    go_id: Mapped[str] = mapped_column(CHAR(10))
    component_id: Mapped[Optional[int]] = mapped_column(Integer)

    component: Mapped[Optional['TargetComponent']] = relationship('TargetComponent', back_populates='tdgo2tc')
    go: Mapped['TargetGo'] = relationship('TargetGo', back_populates='tdgo2tc')


class Tdkey2tc(Base):
    __tablename__ = 'tdkey2tc'
    __table_args__ = (
        ForeignKeyConstraint(['component_id'], ['target_component.id'], name='tdgo2tc_2_tc'),
        ForeignKeyConstraint(['tdkey_id'], ['target_keyword.id'], name='tdgo2tc_2_kw'),
        PrimaryKeyConstraint('id', name='sql141211195643960'),
        {'comment': 'mapping between protein components and Uniprot keywords'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tdkey_id: Mapped[str] = mapped_column(CHAR(7))
    component_id: Mapped[Optional[int]] = mapped_column(Integer)

    component: Mapped[Optional['TargetComponent']] = relationship('TargetComponent', back_populates='tdkey2tc')
    tdkey: Mapped['TargetKeyword'] = relationship('TargetKeyword', back_populates='tdkey2tc')


class Vetprod(Base):
    __tablename__ = 'vetprod'
    __table_args__ = (
        ForeignKeyConstraint(['appl_type'], ['vetprod_type.appl_type'], name='vetprod_2_vetprodtype'),
        PrimaryKeyConstraint('prodid', name='SQL0000000012-af8ec0b3-0182-8659-7929-00007c5ff800'),
        Index('SQL0000000013-67bb80b4-0182-8659-7929-00007c5ff800', 'appl_type'),
        Index('SQL0000000014-4fe880b5-0182-8659-7929-00007c5ff800', 'appl_no', unique=True)
    )

    prodid: Mapped[int] = mapped_column(Integer, primary_key=True)
    appl_type: Mapped[str] = mapped_column(CHAR(1))
    appl_no: Mapped[str] = mapped_column(CHAR(7))
    trade_name: Mapped[Optional[str]] = mapped_column(String(200))
    applicant: Mapped[Optional[str]] = mapped_column(String(100))
    active_ingredients_count: Mapped[Optional[int]] = mapped_column(Integer)

    vetprod_type: Mapped['VetprodType'] = relationship('VetprodType', back_populates='vetprod')
    struct: Mapped[List['Structures']] = relationship('Structures', secondary='vetprod2struct', back_populates='vetprod')


class ActTableFull(Base):
    __tablename__ = 'act_table_full'
    __table_args__ = (
        ForeignKeyConstraint(['act_ref_id'], ['reference.id'], name='bioact_2_ref'),
        ForeignKeyConstraint(['action_type'], ['action_type.action_type'], name='act_table_full_2_act_type'),
        ForeignKeyConstraint(['moa_ref_id'], ['reference.id'], name='moa_2_ref'),
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='act_table_full_2_struct'),
        ForeignKeyConstraint(['target_class'], ['target_class.l1'], name='act_table_full_2_target_class'),
        ForeignKeyConstraint(['target_id'], ['target_dictionary.id'], name='act_table_full_2_target_dict'),
        PrimaryKeyConstraint('act_id', name='sql160219095125231'),
        {'comment': 'bioactivity data aggregated from multiple resources'}
    )

    act_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    struct_id: Mapped[int] = mapped_column(Integer)
    target_id: Mapped[int] = mapped_column(Integer)
    target_name: Mapped[Optional[str]] = mapped_column(String(200))
    target_class: Mapped[Optional[str]] = mapped_column(String(50))
    accession: Mapped[Optional[str]] = mapped_column(String(1000))
    gene: Mapped[Optional[str]] = mapped_column(String(1000))
    swissprot: Mapped[Optional[str]] = mapped_column(String(1000))
    act_value: Mapped[Optional[float]] = mapped_column(Double(53))
    act_unit: Mapped[Optional[str]] = mapped_column(String(100))
    act_type: Mapped[Optional[str]] = mapped_column(String(100))
    act_comment: Mapped[Optional[str]] = mapped_column(String(1000))
    act_source: Mapped[Optional[str]] = mapped_column(String(100))
    relation: Mapped[Optional[str]] = mapped_column(String(5))
    moa: Mapped[Optional[int]] = mapped_column(SmallInteger)
    moa_source: Mapped[Optional[str]] = mapped_column(String(100))
    act_source_url: Mapped[Optional[str]] = mapped_column(String(500))
    moa_source_url: Mapped[Optional[str]] = mapped_column(String(500))
    action_type: Mapped[Optional[str]] = mapped_column(String(50))
    first_in_class: Mapped[Optional[int]] = mapped_column(SmallInteger)
    tdl: Mapped[Optional[str]] = mapped_column(String(500))
    act_ref_id: Mapped[Optional[int]] = mapped_column(Integer)
    moa_ref_id: Mapped[Optional[int]] = mapped_column(Integer)
    organism: Mapped[Optional[str]] = mapped_column(String(150))

    act_ref: Mapped[Optional['Reference']] = relationship('Reference', foreign_keys=[act_ref_id], back_populates='act_table_full')
    action_type_: Mapped[Optional['ActionType']] = relationship('ActionType', back_populates='act_table_full')
    moa_ref: Mapped[Optional['Reference']] = relationship('Reference', foreign_keys=[moa_ref_id], back_populates='act_table_full_')
    struct: Mapped['Structures'] = relationship('Structures', back_populates='act_table_full')
    target_class_: Mapped[Optional['TargetClass']] = relationship('TargetClass', back_populates='act_table_full')
    target: Mapped['TargetDictionary'] = relationship('TargetDictionary', back_populates='act_table_full')


class ActiveIngredient(Base):
    __tablename__ = 'active_ingredient'
    __table_args__ = (
        ForeignKeyConstraint(['ndc_product_code'], ['product.ndc_product_code'], name='active_ingredient_ndc_product_code_fkey'),
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='active_ingredient_2_struct'),
        PrimaryKeyConstraint('id', name='sql120404123859150'),
        Index('sql120404123859152', 'struct_id'),
        Index('sql120412004634310', 'ndc_product_code'),
        {'comment': 'active ingredients listed in FDA drug labels'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    active_moiety_unii: Mapped[Optional[str]] = mapped_column(String(20))
    active_moiety_name: Mapped[Optional[str]] = mapped_column(String(4000))
    unit: Mapped[Optional[str]] = mapped_column(String(20))
    quantity: Mapped[Optional[float]] = mapped_column(Double(53))
    substance_unii: Mapped[Optional[str]] = mapped_column(String(20))
    substance_name: Mapped[Optional[str]] = mapped_column(String(4000))
    ndc_product_code: Mapped[Optional[str]] = mapped_column(String(20))
    struct_id: Mapped[Optional[int]] = mapped_column(Integer)
    quantity_denom_unit: Mapped[Optional[str]] = mapped_column(String(20))
    quantity_denom_value: Mapped[Optional[float]] = mapped_column(Double(53))

    product: Mapped[Optional['Product']] = relationship('Product', back_populates='active_ingredient')
    struct: Mapped[Optional['Structures']] = relationship('Structures', back_populates='active_ingredient')


class Approval(Base):
    __tablename__ = 'approval'
    __table_args__ = (
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='approval_2_struct'),
        ForeignKeyConstraint(['type'], ['approval_type.descr'], name='approval_2_type'),
        PrimaryKeyConstraint('id', name='sql141031231617260'),
        UniqueConstraint('struct_id', 'type', name='sql141031231617263'),
        {'comment': 'approval dates by drug regualtory agencies'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    struct_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String(200))
    approval: Mapped[Optional[datetime.date]] = mapped_column(Date)
    applicant: Mapped[Optional[str]] = mapped_column(String(100))
    orphan: Mapped[Optional[bool]] = mapped_column(Boolean)

    struct: Mapped['Structures'] = relationship('Structures', back_populates='approval')
    approval_type: Mapped['ApprovalType'] = relationship('ApprovalType', back_populates='approval')


class AtcDdd(Base):
    __tablename__ = 'atc_ddd'
    __table_args__ = (
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='atc_ddd_2_struct'),
        PrimaryKeyConstraint('id', name='sql140512172435200'),
        {'comment': 'WHO Defined Daily Dose, the DDD is the assumed average '
                'maintenance dose per day for a drug used for its main indication '
                'in adults'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ddd: Mapped[float] = mapped_column(REAL)
    struct_id: Mapped[int] = mapped_column(Integer)
    atc_code: Mapped[Optional[str]] = mapped_column(CHAR(7))
    unit_type: Mapped[Optional[str]] = mapped_column(String(10))
    route: Mapped[Optional[str]] = mapped_column(String(20))
    comment: Mapped[Optional[str]] = mapped_column(String(100))

    struct: Mapped['Structures'] = relationship('Structures', back_populates='atc_ddd')


class Faers(Base):
    __tablename__ = 'faers'
    __table_args__ = (
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='faers_2_struct'),
        PrimaryKeyConstraint('id', name='sql180422234202640'),
        {'comment': 'Adverse events from FDA FAERS database'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meddra_name: Mapped[str] = mapped_column(String(200))
    meddra_code: Mapped[int] = mapped_column(BigInteger)
    struct_id: Mapped[Optional[int]] = mapped_column(Integer)
    level: Mapped[Optional[str]] = mapped_column(String(5))
    llr: Mapped[Optional[float]] = mapped_column(Double(53), comment='Likelihood Ratio based on method described in http://dx.doi.org/10.1198/jasa.2011.ap10243')
    llr_threshold: Mapped[Optional[float]] = mapped_column(Double(53), comment='Likelihood Ratio threshold based on method described in http://dx.doi.org/10.1198/jasa.2011.ap10243')
    drug_ae: Mapped[Optional[int]] = mapped_column(Integer, comment='number of patients taking drug and having adverse event')
    drug_no_ae: Mapped[Optional[int]] = mapped_column(Integer, comment='number of patients taking drug and not having adverse event')
    no_drug_ae: Mapped[Optional[int]] = mapped_column(Integer, comment='number of patients not taking drug and having adverse event')
    no_drug_no_ae: Mapped[Optional[int]] = mapped_column(Integer, comment='number of patients not taking drug and not having adverse event')

    struct: Mapped[Optional['Structures']] = relationship('Structures', back_populates='faers')


class FaersFemale(Base):
    __tablename__ = 'faers_female'
    __table_args__ = (
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='faers_female_2_struct'),
        PrimaryKeyConstraint('id', name='sql200913054200240')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meddra_name: Mapped[str] = mapped_column(String(200))
    meddra_code: Mapped[int] = mapped_column(BigInteger)
    struct_id: Mapped[Optional[int]] = mapped_column(Integer)
    level: Mapped[Optional[str]] = mapped_column(String(5))
    llr: Mapped[Optional[float]] = mapped_column(Double(53))
    llr_threshold: Mapped[Optional[float]] = mapped_column(Double(53))
    drug_ae: Mapped[Optional[int]] = mapped_column(Integer)
    drug_no_ae: Mapped[Optional[int]] = mapped_column(Integer)
    no_drug_ae: Mapped[Optional[int]] = mapped_column(Integer)
    no_drug_no_ae: Mapped[Optional[int]] = mapped_column(Integer)

    struct: Mapped[Optional['Structures']] = relationship('Structures', back_populates='faers_female')


t_faers_ger = Table(
    'faers_ger', Base.metadata,
    Column('id', Integer, nullable=False),
    Column('struct_id', Integer),
    Column('meddra_name', String(200), nullable=False),
    Column('meddra_code', BigInteger, nullable=False),
    Column('level', String(5)),
    Column('llr', Double(53)),
    Column('llr_threshold', Double(53)),
    Column('drug_ae', Integer),
    Column('drug_no_ae', Integer),
    Column('no_drug_ae', Integer),
    Column('no_drug_no_ae', Integer),
    ForeignKeyConstraint(['struct_id'], ['structures.id'], name='faers_ger_2_struct'),
    Index('SQL0000000000-fb160050-0182-81c2-aa9c-00001f0585e8', 'struct_id')
)


class FaersMale(Base):
    __tablename__ = 'faers_male'
    __table_args__ = (
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='faers_male_2_struct'),
        PrimaryKeyConstraint('id', name='sql200913054154500')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meddra_name: Mapped[str] = mapped_column(String(200))
    meddra_code: Mapped[int] = mapped_column(BigInteger)
    struct_id: Mapped[Optional[int]] = mapped_column(Integer)
    level: Mapped[Optional[str]] = mapped_column(String(5))
    llr: Mapped[Optional[float]] = mapped_column(Double(53))
    llr_threshold: Mapped[Optional[float]] = mapped_column(Double(53))
    drug_ae: Mapped[Optional[int]] = mapped_column(Integer)
    drug_no_ae: Mapped[Optional[int]] = mapped_column(Integer)
    no_drug_ae: Mapped[Optional[int]] = mapped_column(Integer)
    no_drug_no_ae: Mapped[Optional[int]] = mapped_column(Integer)

    struct: Mapped[Optional['Structures']] = relationship('Structures', back_populates='faers_male')


t_faers_ped = Table(
    'faers_ped', Base.metadata,
    Column('id', Integer, nullable=False),
    Column('struct_id', Integer),
    Column('meddra_name', String(200), nullable=False),
    Column('meddra_code', BigInteger, nullable=False),
    Column('level', String(5)),
    Column('llr', Double(53)),
    Column('llr_threshold', Double(53)),
    Column('drug_ae', Integer),
    Column('drug_no_ae', Integer),
    Column('no_drug_ae', Integer),
    Column('no_drug_no_ae', Integer),
    ForeignKeyConstraint(['struct_id'], ['structures.id'], name='faers_ped_2_struct'),
    Index('SQL0000000000-a352c053-0182-81bb-5234-00001f0067d8', 'struct_id')
)


t_humanim = Table(
    'humanim', Base.metadata,
    Column('struct_id', Integer),
    Column('human', Boolean),
    Column('animal', Boolean),
    ForeignKeyConstraint(['struct_id'], ['structures.id'], name='humanim_2_struct'),
    Index('SQL0000000000-6302404f-0182-82a6-63b4-00007c800000', 'struct_id')
)


class Identifier(Base):
    __tablename__ = 'identifier'
    __table_args__ = (
        ForeignKeyConstraint(['id_type'], ['id_type.type'], name='identifier_2_idtype'),
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='identifier_2_struct'),
        PrimaryKeyConstraint('id', name='sql140607225949710'),
        UniqueConstraint('identifier', 'id_type', 'struct_id', name='identifier_unique'),
        {'comment': 'mapping to external drug resouces'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    identifier: Mapped[str] = mapped_column(String(50))
    id_type: Mapped[str] = mapped_column(String(50))
    struct_id: Mapped[int] = mapped_column(Integer)
    parent_match: Mapped[Optional[bool]] = mapped_column(Boolean)

    id_type_: Mapped['IdType'] = relationship('IdType', back_populates='identifier')
    struct: Mapped['Structures'] = relationship('Structures', back_populates='identifier')


class OmopRelationship(Base):
    __tablename__ = 'omop_relationship'
    __table_args__ = (
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='omop_relationship_struct_id_fkey'),
        PrimaryKeyConstraint('id', name='sql121023161238820'),
        UniqueConstraint('struct_id', 'concept_id', name='omoprel_struct_concept_uq'),
        Index('sql121023161238850', 'struct_id'),
        {'comment': 'drug indications/contra-indications/off-label use based on OMOP '
                'v4 and manual annotations'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    struct_id: Mapped[int] = mapped_column(Integer)
    concept_id: Mapped[int] = mapped_column(Integer)
    relationship_name: Mapped[str] = mapped_column(String(256))
    concept_name: Mapped[str] = mapped_column(String(256))
    umls_cui: Mapped[Optional[str]] = mapped_column(CHAR(8))
    snomed_full_name: Mapped[Optional[str]] = mapped_column(String(500))
    cui_semantic_type: Mapped[Optional[str]] = mapped_column(CHAR(4))
    snomed_conceptid: Mapped[Optional[int]] = mapped_column(BigInteger)

    struct: Mapped['Structures'] = relationship('Structures', back_populates='omop_relationship')


class Pdb(Base):
    __tablename__ = 'pdb'
    __table_args__ = (
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='pdb_2_struct'),
        PrimaryKeyConstraint('id', name='sql150123095054720'),
        UniqueConstraint('struct_id', 'pdb', name='sql150123095054722'),
        {'comment': 'mapping to PDB protein-drug complexes'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    struct_id: Mapped[int] = mapped_column(Integer)
    pdb: Mapped[str] = mapped_column(CHAR(4))
    chain_id: Mapped[Optional[str]] = mapped_column(String(3))
    accession: Mapped[Optional[str]] = mapped_column(String(20))
    title: Mapped[Optional[str]] = mapped_column(String(1000))
    pubmed_id: Mapped[Optional[int]] = mapped_column(Integer)
    exp_method: Mapped[Optional[str]] = mapped_column(String(50))
    deposition_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    ligand_id: Mapped[Optional[str]] = mapped_column(String(20))

    struct: Mapped['Structures'] = relationship('Structures', back_populates='pdb')


class PharmaClass(Base):
    __tablename__ = 'pharma_class'
    __table_args__ = (
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='pharma_class_2_struct'),
        PrimaryKeyConstraint('id', name='sql150603161251830'),
        UniqueConstraint('struct_id', 'type', 'name', name='sql150603161251841'),
        {'comment': 'pharmacologic classifications of drugs from multiple resources'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(1000))
    struct_id: Mapped[Optional[int]] = mapped_column(Integer)
    class_code: Mapped[Optional[str]] = mapped_column(String(20))
    source: Mapped[Optional[str]] = mapped_column(String(100))

    struct: Mapped[Optional['Structures']] = relationship('Structures', back_populates='pharma_class')


class Pka(Base):
    __tablename__ = 'pka'
    __table_args__ = (
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='pka_2_struct'),
        PrimaryKeyConstraint('id', name='sql180408153602180'),
        {'comment': 'logarithm of acid dissociation constant calculated using MoKa '
                '3.0.0'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    struct_id: Mapped[int] = mapped_column(Integer)
    pka_type: Mapped[str] = mapped_column(CHAR(1))
    pka_level: Mapped[Optional[str]] = mapped_column(String(5))
    value: Mapped[Optional[float]] = mapped_column(Double(53))

    struct: Mapped['Structures'] = relationship('Structures', back_populates='pka')


t_property = Table(
    'property', Base.metadata,
    Column('id', Integer, nullable=False),
    Column('property_type_id', Integer),
    Column('property_type_symbol', String(10)),
    Column('struct_id', Integer),
    Column('value', Double(53)),
    Column('reference_id', Integer),
    Column('reference_type', String(50)),
    Column('source', String(80)),
    ForeignKeyConstraint(['property_type_symbol'], ['property_type.symbol'], name='prop_2_prop_type'),
    ForeignKeyConstraint(['struct_id'], ['structures.id'], name='prop_2_struct')
)


class Struct2atc(Base):
    __tablename__ = 'struct2atc'
    __table_args__ = (
        ForeignKeyConstraint(['atc_code'], ['atc.code'], name='struct2atc_2_atc'),
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='struct2atc_2_struct'),
        PrimaryKeyConstraint('struct_id', 'atc_code', name='sql120523120921130'),
        UniqueConstraint('id', name='struct2atc_id_key'),
        Index('sql120523120921131', 'struct_id'),
        {'comment': 'mapping between structures table and WHO ATC codes'}
    )

    struct_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    atc_code: Mapped[str] = mapped_column(CHAR(7), primary_key=True)
    id: Mapped[int] = mapped_column(Integer)

    atc: Mapped['Atc'] = relationship('Atc', back_populates='struct2atc')
    struct: Mapped['Structures'] = relationship('Structures', back_populates='struct2atc')


class Struct2drgclass(Base):
    __tablename__ = 'struct2drgclass'
    __table_args__ = (
        ForeignKeyConstraint(['drug_class_id'], ['drug_class.id'], name='struct2drgclass_2_drgclass'),
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='struct2drgclass_2_struct'),
        PrimaryKeyConstraint('id', name='sql140608153701270'),
        UniqueConstraint('struct_id', 'drug_class_id', name='sql140608153701271'),
        {'comment': 'mapping between structures and drug_class tables'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    struct_id: Mapped[int] = mapped_column(Integer)
    drug_class_id: Mapped[int] = mapped_column(Integer)

    drug_class: Mapped['DrugClass'] = relationship('DrugClass', back_populates='struct2drgclass')
    struct: Mapped['Structures'] = relationship('Structures', back_populates='struct2drgclass')


class Struct2obprod(Base):
    __tablename__ = 'struct2obprod'
    __table_args__ = (
        ForeignKeyConstraint(['prod_id'], ['ob_product.id'], name='struct_2_obprod'),
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='obprod_2_struct'),
        PrimaryKeyConstraint('struct_id', 'prod_id', name='sql161126154450310')
    )

    struct_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prod_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    strength: Mapped[Optional[str]] = mapped_column(String(4000))

    prod: Mapped['ObProduct'] = relationship('ObProduct', back_populates='struct2obprod')
    struct: Mapped['Structures'] = relationship('Structures', back_populates='struct2obprod')


t_struct2parent = Table(
    'struct2parent', Base.metadata,
    Column('struct_id', Integer, primary_key=True, nullable=False),
    Column('parent_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['parent_id'], ['parentmol.cd_id'], name='struct2parent_2_parent'),
    ForeignKeyConstraint(['struct_id'], ['structures.id'], name='struct2parent_2_struct'),
    PrimaryKeyConstraint('struct_id', 'parent_id', name='sql150529131801300'),
    comment='mapping between prodrugs in structures table and active parent molecules'
)


class StructureType(Base):
    __tablename__ = 'structure_type'
    __table_args__ = (
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='structure_type_2_struct'),
        ForeignKeyConstraint(['type'], ['struct_type_def.type'], name='structure_type_2_type'),
        PrimaryKeyConstraint('id', name='sql120925163230900'),
        UniqueConstraint('struct_id', 'type', name='struct_id_type_uq'),
        Index('sql120925163230920', 'struct_id'),
        Index('sql120925163230921', 'struct_id', 'type'),
        {'comment': 'mapping between chemical entities in structures table and types '
                'defined in struct_type_def'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(50), server_default=text("'UNKNOWN'::character varying"))
    struct_id: Mapped[Optional[int]] = mapped_column(Integer)

    struct: Mapped[Optional['Structures']] = relationship('Structures', back_populates='structure_type')
    struct_type_def: Mapped['StructTypeDef'] = relationship('StructTypeDef', back_populates='structure_type')


class Synonyms(Base):
    __tablename__ = 'synonyms'
    __table_args__ = (
        ForeignKeyConstraint(['id'], ['structures.id'], name='synonym_2_struct'),
        ForeignKeyConstraint(['parent_id'], ['parentmol.cd_id'], name='synonym_2_parent'),
        PrimaryKeyConstraint('syn_id', name='sql150826201920370'),
        UniqueConstraint('id', 'preferred_name', name='sql150826201920374'),
        UniqueConstraint('lname', name='syn_lname_uq'),
        UniqueConstraint('name', name='sql150826201920371'),
        UniqueConstraint('parent_id', 'preferred_name', name='sql150826201920375'),
        {'comment': 'unamiguous list of synonyms assigned to chemical entities in '
                'structures and parentmol tables'}
    )

    syn_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250))
    id: Mapped[Optional[int]] = mapped_column(Integer)
    preferred_name: Mapped[Optional[int]] = mapped_column(SmallInteger)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer)
    lname: Mapped[Optional[str]] = mapped_column(String(250), server_default=text("'GENERATED ALWAYS AS ( LCASE(NAME) )'::character varying"))

    structures: Mapped[Optional['Structures']] = relationship('Structures', back_populates='synonyms')
    parent: Mapped[Optional['Parentmol']] = relationship('Parentmol', back_populates='synonyms')


class Vetomop(Base):
    __tablename__ = 'vetomop'
    __table_args__ = (
        ForeignKeyConstraint(['struct_id'], ['structures.id'], name='vetomop_2_struct'),
        PrimaryKeyConstraint('omopid', name='SQL0000000018-6dd780d4-0182-8659-7929-00007c5ff800'),
        Index('SQL0000000019-560c80d5-0182-8659-7929-00007c5ff800', 'struct_id')
    )

    omopid: Mapped[int] = mapped_column(Integer, primary_key=True)
    struct_id: Mapped[Optional[int]] = mapped_column(Integer)
    species: Mapped[Optional[str]] = mapped_column(String(100))
    relationship_type: Mapped[Optional[str]] = mapped_column(String(50))
    concept_name: Mapped[Optional[str]] = mapped_column(String(500))

    struct: Mapped[Optional['Structures']] = relationship('Structures', back_populates='vetomop')


t_vetprod2struct = Table(
    'vetprod2struct', Base.metadata,
    Column('prodid', Integer),
    Column('struct_id', Integer),
    ForeignKeyConstraint(['prodid'], ['vetprod.prodid'], name='vetprodstruct_2_prod'),
    ForeignKeyConstraint(['struct_id'], ['structures.id'], name='vetprodstruct_2_struct'),
    Index('SQL0000000015-b278c0c3-0182-8659-7929-00007c5ff800', 'prodid'),
    Index('SQL0000000016-eaa980c4-0182-8659-7929-00007c5ff800', 'struct_id')
)


t_vettype = Table(
    'vettype', Base.metadata,
    Column('prodid', Integer),
    Column('type', String(3)),
    ForeignKeyConstraint(['prodid'], ['vetprod.prodid'], name='vettype_2_vetprod'),
    Index('SQL0000000017-d46b80cd-0182-8659-7929-00007c5ff800', 'prodid')
)
