from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, CHAR, Column, Date, DateTime, Double, ForeignKeyConstraint, Index, Integer, LargeBinary, PrimaryKeyConstraint, REAL, SmallInteger, String, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


t_COPYOFDATAIKUTSHIRTS_PSH_humanim_prepared = Table(
    'COPYOFDATAIKUTSHIRTS_PSH_humanim_prepared', Base.metadata,
    Column('test', BigInteger),
    Column('human', Boolean),
    Column('animal', Boolean)
)


t_DEMO_TALK_TO_MOLECULES_log_file = Table(
    'DEMO_TALK_TO_MOLECULES_log_file', Base.metadata,
    Column('conversation_id', Text),
    Column('conversation_name', Text),
    Column('knowledge_bank_id', Text),
    Column('knowledge_bank_name', Text),
    Column('llm_name', Text),
    Column('user', Text),
    Column('message_id', Text),
    Column('question', Text),
    Column('filters', Text),
    Column('file_path', Text),
    Column('answer', Text),
    Column('sources', Text),
    Column('feedback_value', Text),
    Column('feedback_choice', Text),
    Column('feedback_message', Text),
    Column('timestamp', Text),
    Column('state', Text),
    Column('llm_context', Text),
    Column('generated_media', Text)
)


t_DEMO_TALK_TO_MOLECULES_metadata_sql = Table(
    'DEMO_TALK_TO_MOLECULES_metadata_sql', Base.metadata,
    Column('accession', Text),
    Column('component_description', Text),
    Column('tax_id', BigInteger),
    Column('organism', Text),
    Column('target_component_synonyms', Text),
    Column('studied_molecules', Text),
    Column('no_studied_molecules', BigInteger),
    Column('database', Text),
    Column('amino_acid_seq', Text)
)


t_DEMO_TALK_TO_MOLECULES_molecular_similarity_sql = Table(
    'DEMO_TALK_TO_MOLECULES_molecular_similarity_sql', Base.metadata,
    Column('new_molecules', Text),
    Column('new_molecule_id', Text),
    Column('studied_molecules', Text),
    Column('studied_molecule_id', Text),
    Column('similarity_score', Double(53)),
    Column('target_protein', Text)
)


t_DEMO_TALK_TO_MOLECULES_scored_molecules = Table(
    'DEMO_TALK_TO_MOLECULES_scored_molecules', Base.metadata,
    Column('molecule_id', Text),
    Column('canonical_smiles', Text),
    Column('MolWt', Double(53)),
    Column('MolLogP', Double(53)),
    Column('NumHAcceptors', BigInteger),
    Column('NumHDonors', BigInteger),
    Column('NumRotatableBonds', BigInteger),
    Column('NumHeteroatoms', BigInteger),
    Column('NumAromaticRings', BigInteger),
    Column('RingCount', BigInteger),
    Column('HeavyAtomCount', BigInteger),
    Column('TPSA', Double(53)),
    Column('QED', Double(53)),
    Column('Lipinskis_rule', Text),
    Column('pIC50_pred_P05093', REAL),
    Column('pIC50_pred_P11511', REAL),
    Column('toxicity_prediction', Text)
)


t_DEMO_TALK_TO_MOLECULES_studied_molecules_sql = Table(
    'DEMO_TALK_TO_MOLECULES_studied_molecules_sql', Base.metadata,
    Column('canonical_smiles', Text),
    Column('MolWt', Double(53)),
    Column('MolLogP', Double(53)),
    Column('NumHAcceptors', BigInteger),
    Column('NumHDonors', BigInteger),
    Column('NumRotatableBonds', BigInteger),
    Column('NumHeteroatoms', BigInteger),
    Column('NumAromaticRings', BigInteger),
    Column('RingCount', BigInteger),
    Column('HeavyAtomCount', BigInteger),
    Column('TPSA', Double(53)),
    Column('QED', Double(53)),
    Column('molecule_id', Text),
    Column('pIC50', Double(53)),
    Column('Target_Protein', Text)
)


t_DEMO_TALK_TO_MOLECULES_user_settings = Table(
    'DEMO_TALK_TO_MOLECULES_user_settings', Base.metadata,
    Column('user', Text),
    Column('profile', Text),
    Column('last_updated', DateTime(True))
)


t_EMERGENCYOPTIMIZATION_disease_percent = Table(
    'EMERGENCYOPTIMIZATION_disease_percent', Base.metadata,
    Column('State_name', Text),
    Column('County_name', Text),
    Column('Percent_All_Teeth_Lost_Disease_county', Double(53)),
    Column('Percent_Arthritis_Disease_county', Double(53)),
    Column('Percent_COPD_Disease_county', Double(53)),
    Column('Percent_Cancer_except_skin_Disease_county', Double(53)),
    Column('Percent_Coronary_Heart_Disease_county', Double(53)),
    Column('Percent_Current_Asthma_Disease_county', Double(53)),
    Column('Percent_Depression_Disease_county', Double(53)),
    Column('Percent_Diabetes_Disease_county', Double(53)),
    Column('Percent_Obesity_Disease_county', Double(53)),
    Column('Percent_Stroke_Disease_county', Double(53)),
    Column('All_Teeth_Lost_Disease_county_Percentile', Double(53)),
    Column('Arthritis_Disease_county_Percentile', Double(53)),
    Column('COPD_Disease_county_Percentile', Double(53)),
    Column('Cancer_except_skin_county_Percentile', Double(53)),
    Column('Coronary_Heart_Disease_county_Percentile', Double(53)),
    Column('Current_Asthma_Disease_county_Percentile', Double(53)),
    Column('Depression_Disease_county_Percentile', Double(53)),
    Column('Diabetes_Disease_county_Percentile', Double(53)),
    Column('Obesity_Disease_county_Percentile', Double(53)),
    Column('Stroke_Disease_county_Percentile', Double(53))
)


t_EMERGENCYOPTIMIZATION_population = Table(
    'EMERGENCYOPTIMIZATION_population', Base.metadata,
    Column('County_name', Text),
    Column('State_name', Text),
    Column('Population_tract', Double(53))
)


t_FDAGUIDANCEDOC_logfiles = Table(
    'FDAGUIDANCEDOC_logfiles', Base.metadata,
    Column('conversation_id', Text),
    Column('conversation_name', Text),
    Column('knowledge_bank_id', Text),
    Column('knowledge_bank_name', Text),
    Column('llm_name', Text),
    Column('user', Text),
    Column('message_id', Text),
    Column('question', Text),
    Column('filters', Text),
    Column('file_path', Text),
    Column('answer', Text),
    Column('sources', Text),
    Column('feedback_value', Text),
    Column('feedback_choice', Text),
    Column('feedback_message', Text),
    Column('timestamp', Text),
    Column('state', Text),
    Column('llm_context', Text),
    Index('conversation_id_index', 'conversation_id'),
    Index('timestamp_index', 'timestamp'),
    Index('user_index', 'user')
)


t_MOLECULARPROPERTYPREDICTIONLLM_metadata_sql = Table(
    'MOLECULARPROPERTYPREDICTIONLLM_metadata_sql', Base.metadata,
    Column('accession', Text),
    Column('component_description', Text),
    Column('tax_id', BigInteger),
    Column('organism', Text),
    Column('target_component_synonyms', Text),
    Column('studied_molecules', Text),
    Column('no_studied_molecules', BigInteger),
    Column('database', Text),
    Column('amino_acid_seq', Text)
)


t_MOLECULARPROPERTYPREDICTIONLLM_molecular_similarity_sql = Table(
    'MOLECULARPROPERTYPREDICTIONLLM_molecular_similarity_sql', Base.metadata,
    Column('new_molecules', Text),
    Column('new_molecule_id', Text),
    Column('studied_molecules', Text),
    Column('studied_molecule_id', Text),
    Column('similarity_score', Double(53)),
    Column('target_protein', Text),
    Column('molecular_vectors', Text)
)


t_MOLECULARPROPERTYPREDICTIONLLM_scored_molecules = Table(
    'MOLECULARPROPERTYPREDICTIONLLM_scored_molecules', Base.metadata,
    Column('molecule_id', Text),
    Column('canonical_smiles', Text),
    Column('MolWt', Double(53)),
    Column('MolLogP', Double(53)),
    Column('NumHAcceptors', BigInteger),
    Column('NumHDonors', BigInteger),
    Column('NumRotatableBonds', BigInteger),
    Column('NumHeteroatoms', BigInteger),
    Column('NumAromaticRings', BigInteger),
    Column('RingCount', BigInteger),
    Column('HeavyAtomCount', BigInteger),
    Column('TPSA', Double(53)),
    Column('QED', Double(53)),
    Column('Lipinskis_rule', Text),
    Column('pIC50_pred_P05093', REAL),
    Column('pIC50_pred_P11511', REAL),
    Column('toxicity_prediction', Text)
)


t_OBJECTDETECTION_YOLO_testtt_prepared = Table(
    'OBJECTDETECTION_YOLO_testtt_prepared', Base.metadata,
    Column('id', Integer),
    Column('rr', BigInteger),
    Column('approval', DateTime(True)),
    Column('type', String(200)),
    Column('applicant', String(100)),
    Column('orphan', Boolean)
)


t_QS_DATAPROCML_FINAL_historical_transactions = Table(
    'QS_DATAPROCML_FINAL_historical_transactions', Base.metadata,
    Column('transaction_id', BigInteger),
    Column('authorized_flag', BigInteger),
    Column('purchase_date', Text),
    Column('card_id', Text),
    Column('merchant_id', Text),
    Column('merchant_category_id', BigInteger),
    Column('item_category', Text),
    Column('purchase_amount', Double(53)),
    Column('signature_provided', BigInteger)
)


t_QS_DATAPROCML_FINAL_new_transactions = Table(
    'QS_DATAPROCML_FINAL_new_transactions', Base.metadata,
    Column('transaction_id', BigInteger),
    Column('purchase_date', Text),
    Column('card_id', Text),
    Column('merchant_id', Text),
    Column('merchant_category_id', BigInteger),
    Column('item_category', Text),
    Column('purchase_amount', Double(53)),
    Column('signature_provided', BigInteger)
)


t_SOL_OMNI_PHARMA_12_40fB29Pb_history = Table(
    'SOL_OMNI_PHARMA_12_40fB29Pb_history', Base.metadata,
    Column('conversation_id', Text),
    Column('conversation_name', Text),
    Column('knowledge_bank_id', Text),
    Column('knowledge_bank_name', Text),
    Column('llm_name', Text),
    Column('user', Text),
    Column('message_id', Text),
    Column('question', Text),
    Column('filters', Text),
    Column('file_path', Text),
    Column('answer', Text),
    Column('sources', Text),
    Column('feedback_value', Text),
    Column('feedback_choice', Text),
    Column('feedback_message', Text),
    Column('timestamp', Text),
    Column('state', Text),
    Column('llm_context', Text),
    Column('generated_media', Text)
)


t_SOL_OMNI_PHARMA_12_40fB29Pb_profile = Table(
    'SOL_OMNI_PHARMA_12_40fB29Pb_profile', Base.metadata,
    Column('user', Text),
    Column('profile', Text),
    Column('last_updated', DateTime)
)


t_SOL_OMNI_PHARMA_12_NyR4YFsf_history = Table(
    'SOL_OMNI_PHARMA_12_NyR4YFsf_history', Base.metadata,
    Column('conversation_id', Text),
    Column('conversation_name', Text),
    Column('knowledge_bank_id', Text),
    Column('knowledge_bank_name', Text),
    Column('llm_name', Text),
    Column('user', Text),
    Column('message_id', Text),
    Column('question', Text),
    Column('filters', Text),
    Column('file_path', Text),
    Column('answer', Text),
    Column('sources', Text),
    Column('feedback_value', Text),
    Column('feedback_choice', Text),
    Column('feedback_message', Text),
    Column('timestamp', Text),
    Column('state', Text),
    Column('llm_context', Text),
    Column('generated_media', Text)
)


t_SOL_OMNI_PHARMA_12_NyR4YFsf_profile = Table(
    'SOL_OMNI_PHARMA_12_NyR4YFsf_profile', Base.metadata,
    Column('user', Text),
    Column('profile', Text),
    Column('last_updated', DateTime)
)


t_SOL_OMNI_PHARMA_12_Z6uFNJRH_history = Table(
    'SOL_OMNI_PHARMA_12_Z6uFNJRH_history', Base.metadata,
    Column('conversation_id', Text),
    Column('conversation_name', Text),
    Column('knowledge_bank_id', Text),
    Column('knowledge_bank_name', Text),
    Column('llm_name', Text),
    Column('user', Text),
    Column('message_id', Text),
    Column('question', Text),
    Column('filters', Text),
    Column('file_path', Text),
    Column('answer', Text),
    Column('sources', Text),
    Column('feedback_value', Text),
    Column('feedback_choice', Text),
    Column('feedback_message', Text),
    Column('timestamp', Text),
    Column('state', Text),
    Column('llm_context', Text),
    Column('generated_media', Text)
)


t_SOL_OMNI_PHARMA_12_Z6uFNJRH_profile = Table(
    'SOL_OMNI_PHARMA_12_Z6uFNJRH_profile', Base.metadata,
    Column('user', Text),
    Column('profile', Text),
    Column('last_updated', DateTime)
)


t_SOL_OMNI_PHARMA_12_history = Table(
    'SOL_OMNI_PHARMA_12_history', Base.metadata,
    Column('conversation_id', Text),
    Column('conversation_name', Text),
    Column('knowledge_bank_id', Text),
    Column('knowledge_bank_name', Text),
    Column('llm_name', Text),
    Column('user', Text),
    Column('message_id', Text),
    Column('question', Text),
    Column('filters', Text),
    Column('file_path', Text),
    Column('answer', Text),
    Column('sources', Text),
    Column('feedback_value', Text),
    Column('feedback_choice', Text),
    Column('feedback_message', Text),
    Column('timestamp', Text),
    Column('state', Text),
    Column('llm_context', Text),
    Column('generated_media', Text)
)


t_SOL_OMNI_PHARMA_12_profile = Table(
    'SOL_OMNI_PHARMA_12_profile', Base.metadata,
    Column('user', Text),
    Column('profile', Text),
    Column('last_updated', DateTime)
)


t_SOL_OMNI_PHARMA_12_scored_data_sql = Table(
    'SOL_OMNI_PHARMA_12_scored_data_sql', Base.metadata,
    Column('account_id', Text),
    Column('brand_name', Text),
    Column('parent_account_id', Text),
    Column('parent_account_type', Text),
    Column('account_specialty', Text),
    Column('email_preferences', Text),
    Column('account_tenure', Double(53)),
    Column('facetoface_success', BigInteger),
    Column('facetoface_avg_time_min', BigInteger),
    Column('webcall_attempt', BigInteger),
    Column('webcall_success', BigInteger),
    Column('webcall_avg_time_min', BigInteger),
    Column('phone_attempt', BigInteger),
    Column('phone_success', BigInteger),
    Column('phone_avg_time_min', BigInteger),
    Column('nb_emails_sent_attempt', BigInteger),
    Column('nb_emails_open_success', BigInteger),
    Column('website_vists_success', BigInteger),
    Column('website_traffic_avg_time_min', BigInteger),
    Column('web_channel_referral', BigInteger),
    Column('web_channel_paid', BigInteger),
    Column('web_channel_organic search', BigInteger),
    Column('product_id', Text),
    Column('campaign_id', Text),
    Column('llm_output_1_notes_sentiment', Text),
    Column('llm_output_1_channel_webcall', BigInteger),
    Column('llm_output_1_channel_facetoface', BigInteger),
    Column('llm_output_1_channel_phone', BigInteger),
    Column('llm_output_1_channel_website', BigInteger),
    Column('llm_output_1_channel_email', BigInteger),
    Column('proba_0', Double(53)),
    Column('proba_1', Double(53)),
    Column('prediction', Text),
    Column('explanations', Text),
    Column('smmd_savedModelId', Text),
    Column('smmd_modelVersion', Text),
    Column('smmd_fullModelId', Text),
    Column('smmd_predictionTime', DateTime(True))
)


t_SOL_PHARMACOVIGILANCE_dAgikQYW_Demographics_faers_input = Table(
    'SOL_PHARMACOVIGILANCE_dAgikQYW_Demographics_faers_input', Base.metadata,
    Column('primaryid', Text),
    Column('caseid', Text),
    Column('caseversion', Text),
    Column('i_f_code', Text),
    Column('event_dt', Text),
    Column('mfr_dt', Text),
    Column('init_fda_dt', Text),
    Column('fda_dt', Text),
    Column('rept_cod', Text),
    Column('auth_num', Text),
    Column('mfr_num', Text),
    Column('mfr_sndr', Text),
    Column('lit_ref', Text),
    Column('age', Double(53)),
    Column('age_cod', Double(53)),
    Column('age_grp', Text),
    Column('sex', Text),
    Column('e_sub', Text),
    Column('wt', Text),
    Column('wt_cod', Text),
    Column('rept_dt', Text),
    Column('to_mfr', Text),
    Column('occp_cod', Text),
    Column('reporter_country', Text),
    Column('occr_country', Text),
    Column('age_years', Double(53))
)


t_SOL_PHARMACOVIGILANCE_dAgikQYW_FDA_products_input = Table(
    'SOL_PHARMACOVIGILANCE_dAgikQYW_FDA_products_input', Base.metadata,
    Column('ApplNo', Text),
    Column('ProductNo', Text),
    Column('Form', Text),
    Column('Strength', Text),
    Column('ReferenceDrug', Text),
    Column('DrugName', Text),
    Column('ActiveIngredient', Text),
    Column('ReferenceStandard', Text)
)


t_SOL_PHARMACOVIGILANCE_dAgikQYW_Indication_faers_input = Table(
    'SOL_PHARMACOVIGILANCE_dAgikQYW_Indication_faers_input', Base.metadata,
    Column('primaryid', Text),
    Column('caseid', Text),
    Column('indi_drug_seq', Text),
    Column('indi_pt', Text)
)


t_SOL_PHARMACOVIGILANCE_dAgikQYW_Medication_faers_input = Table(
    'SOL_PHARMACOVIGILANCE_dAgikQYW_Medication_faers_input', Base.metadata,
    Column('primaryid', Text),
    Column('caseid', Text),
    Column('drug_seq', Text),
    Column('role_cod', Text),
    Column('drugname', Text),
    Column('prod_ai', Text),
    Column('val_vbm', Text),
    Column('route', Text),
    Column('dose_vbm', Text),
    Column('cum_dose_chr', Text),
    Column('cum_dose_unit', Text),
    Column('dechal', Text),
    Column('rechal', Text),
    Column('lot_num', Text),
    Column('exp_dt', Text),
    Column('nda_num', Text),
    Column('dose_amt', Text),
    Column('dose_unit', Text),
    Column('dose_form', Text),
    Column('dose_freq', Text)
)


t_SOL_PHARMACOVIGILANCE_dAgikQYW_Outcome_faers_input = Table(
    'SOL_PHARMACOVIGILANCE_dAgikQYW_Outcome_faers_input', Base.metadata,
    Column('primaryid', Text),
    Column('caseid', Text),
    Column('outc_cod', Text),
    Column('seriousness', BigInteger)
)


t_SOL_PHARMACOVIGILANCE_dAgikQYW_Reaction_faers_input = Table(
    'SOL_PHARMACOVIGILANCE_dAgikQYW_Reaction_faers_input', Base.metadata,
    Column('primaryid', Text),
    Column('caseid', Text),
    Column('pt', Text),
    Column('drug_rec_act', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_08627f50fdcb734724ddaf20aa8ab073 = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_08627f50fdcb734724ddaf20aa8ab073', Base.metadata,
    Column('drug', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_1e4135e989687eacef1e9491866a11bd = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_1e4135e989687eacef1e9491866a11bd', Base.metadata,
    Column('drug', Text),
    Column('adverse_event', Text),
    Column('PRR_all', Double(53)),
    Column('Warning_PRR_all', Text),
    Column('Warning_PRR_flag', Text),
    Column('PRR_F', Double(53)),
    Column('PRR_M', Double(53)),
    Column('ROR_all', Double(53)),
    Column('ROR_F', Double(53)),
    Column('ROR_M', Double(53)),
    Column('PRR_CI_L_all', Double(53)),
    Column('PRR_CI_L_F', Double(53)),
    Column('PRR_CI_L_M', Double(53)),
    Column('ROR_CI_L_all', Double(53)),
    Column('Warning_ROR_all', Text),
    Column('Warning_ROR_flag', Text),
    Column('ROR_CI_L_F', Double(53)),
    Column('Warning_ROR_F', Text),
    Column('Warning_ROR_flag_F', BigInteger),
    Column('ROR_CI_L_M', Double(53)),
    Column('Warning_ROR_M', Text),
    Column('Warning_ROR_flag_M', BigInteger),
    Column('EBGM_all', Double(53)),
    Column('EBGM_F', Double(53)),
    Column('EBGM_M', Double(53)),
    Column('drug_event_occur', BigInteger),
    Column('drugother_eventother_occur', BigInteger),
    Column('drugother_event_occur', BigInteger),
    Column('drug_eventother_occur', BigInteger),
    Column('drug_percentage_freq', Double(53)),
    Column('event_percentage_freq', Double(53))
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_38bb4cecef81382fd433af1e3d0e29cd = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_38bb4cecef81382fd433af1e3d0e29cd', Base.metadata,
    Column('primaryid', BigInteger),
    Column('sex', Text),
    Column('age', Double(53)),
    Column('drug', Text),
    Column('adverse_event', Text),
    Column('manufacturer', Text),
    Column('event_date', DateTime(True)),
    Column('event_date_year', Double(53)),
    Column('report_type', Text),
    Column('reporter', Text),
    Column('reporter_country', Text),
    Column('age_group', Text),
    Column('route', Text),
    Column('drug_interactions', BigInteger),
    Column('Interaction_detected', Text),
    Column('indication', Text),
    Column('indication_unknown', BigInteger),
    Column('total_medications', BigInteger),
    Column('outcome', Text),
    Column('seriousness', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_6ae0a567aafe7f0e3493143e4bf22adf = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_6ae0a567aafe7f0e3493143e4bf22adf', Base.metadata,
    Column('primaryid', Text),
    Column('total_medications', BigInteger)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_CM = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_CM', Base.metadata,
    Column('primaryid', Text),
    Column('drug_seq', Text),
    Column('role_cod', Text),
    Column('drugname', Text),
    Column('route', Text),
    Column('nda_num', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Demographics_faers_clean = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Demographics_faers_clean', Base.metadata,
    Column('primaryid', Text),
    Column('event_date', DateTime(True)),
    Column('event_date_year', BigInteger),
    Column('event_date_month', BigInteger),
    Column('rept_cod', Text),
    Column('mfr_sndr', Text),
    Column('sex', Text),
    Column('occp_cod', Text),
    Column('occr_country', Text),
    Column('age_years', Text),
    Column('age_group', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Demographics_faers_distinct = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Demographics_faers_distinct', Base.metadata,
    Column('primaryid', Text),
    Column('event_dt', Text),
    Column('rept_cod', Text),
    Column('mfr_sndr', Text),
    Column('sex', Text),
    Column('occp_cod', Text),
    Column('occr_country', Text),
    Column('age_years', Double(53))
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Demographics_faers_input = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Demographics_faers_input', Base.metadata,
    Column('primaryid', Text),
    Column('caseid', Text),
    Column('caseversion', Text),
    Column('i_f_code', Text),
    Column('event_dt', Text),
    Column('mfr_dt', Text),
    Column('init_fda_dt', Text),
    Column('fda_dt', Text),
    Column('rept_cod', Text),
    Column('auth_num', Text),
    Column('mfr_num', Text),
    Column('mfr_sndr', Text),
    Column('lit_ref', Text),
    Column('age', Double(53)),
    Column('age_cod', Double(53)),
    Column('age_grp', Text),
    Column('sex', Text),
    Column('e_sub', Text),
    Column('wt', Text),
    Column('wt_cod', Text),
    Column('rept_dt', Text),
    Column('to_mfr', Text),
    Column('occp_cod', Text),
    Column('reporter_country', Text),
    Column('occr_country', Text),
    Column('age_years', Double(53))
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Drug_I = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Drug_I', Base.metadata,
    Column('primaryid', Text),
    Column('drug_seq', Text),
    Column('role_cod', Text),
    Column('drugname', Text),
    Column('route', Text),
    Column('nda_num', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Drug_I_by_primaryid = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Drug_I_by_primaryid', Base.metadata,
    Column('primaryid', Text),
    Column('drugname_distinct', BigInteger),
    Column('drugname_concat', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Drug_PS = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Drug_PS', Base.metadata,
    Column('primaryid', Text),
    Column('drug_seq', Text),
    Column('role_cod', Text),
    Column('drugname', Text),
    Column('route', Text),
    Column('nda_num', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Drug_PS_joined = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Drug_PS_joined', Base.metadata,
    Column('primaryid', Text),
    Column('drug_seq', Text),
    Column('role_cod', Text),
    Column('drugname', Text),
    Column('route', Text),
    Column('nda_num', Text),
    Column('drugname_distinct', BigInteger),
    Column('drug_interactions', Text),
    Column('Interaction_detected', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Drug_faers = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Drug_faers', Base.metadata,
    Column('primaryid', Text),
    Column('drug_seq', Text),
    Column('drugname', Text),
    Column('route', Text),
    Column('drugname_distinct', BigInteger),
    Column('Interaction_detected', Text),
    Column('indi_pt', Text),
    Column('total_medications', BigInteger),
    Column('fda_DrugName', Text),
    Column('drug', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Drugs_PS_indications = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Drugs_PS_indications', Base.metadata,
    Column('primaryid', Text),
    Column('drug_seq', Text),
    Column('role_cod', Text),
    Column('drugname', Text),
    Column('route', Text),
    Column('nda_num', Text),
    Column('drugname_distinct', BigInteger),
    Column('Interaction_detected', Text),
    Column('indi_pt', Text),
    Column('total_medications', BigInteger)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_FDA_products_distinct = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_FDA_products_distinct', Base.metadata,
    Column('ApplNo', Text),
    Column('DrugName', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_FDA_products_input = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_FDA_products_input', Base.metadata,
    Column('ApplNo', Text),
    Column('ProductNo', Text),
    Column('Form', Text),
    Column('Strength', Text),
    Column('ReferenceDrug', Text),
    Column('DrugName', Text),
    Column('ActiveIngredient', Text),
    Column('ReferenceStandard', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Indication_faers_distinct = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Indication_faers_distinct', Base.metadata,
    Column('primaryid', Text),
    Column('indi_drug_seq', Text),
    Column('indi_pt', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Indication_faers_input = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Indication_faers_input', Base.metadata,
    Column('primaryid', Text),
    Column('caseid', Text),
    Column('indi_drug_seq', Text),
    Column('indi_pt', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Medication_faers_distinct = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Medication_faers_distinct', Base.metadata,
    Column('primaryid', Text),
    Column('drug_seq', Text),
    Column('role_cod', Text),
    Column('drugname', Text),
    Column('route', Text),
    Column('nda_num', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Medication_faers_input = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Medication_faers_input', Base.metadata,
    Column('primaryid', Text),
    Column('caseid', Text),
    Column('drug_seq', Text),
    Column('role_cod', Text),
    Column('drugname', Text),
    Column('prod_ai', Text),
    Column('val_vbm', Text),
    Column('route', Text),
    Column('dose_vbm', Text),
    Column('cum_dose_chr', Text),
    Column('cum_dose_unit', Text),
    Column('dechal', Text),
    Column('rechal', Text),
    Column('lot_num', Text),
    Column('exp_dt', Text),
    Column('nda_num', Text),
    Column('dose_amt', Text),
    Column('dose_unit', Text),
    Column('dose_form', Text),
    Column('dose_freq', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Outcome_faers_distinct = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Outcome_faers_distinct', Base.metadata,
    Column('primaryid', Text),
    Column('outc_cod', Text),
    Column('seriousness', BigInteger)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Outcome_faers_input = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Outcome_faers_input', Base.metadata,
    Column('primaryid', Text),
    Column('caseid', Text),
    Column('outc_cod', Text),
    Column('seriousness', BigInteger)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Reaction_faers_distinct = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Reaction_faers_distinct', Base.metadata,
    Column('primaryid', Text),
    Column('pt', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Reaction_faers_input = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Reaction_faers_input', Base.metadata,
    Column('primaryid', Text),
    Column('caseid', Text),
    Column('pt', Text),
    Column('drug_rec_act', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Report_faers_distinct_filters = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Report_faers_distinct_filters', Base.metadata,
    Column('age_group', Text),
    Column('adverse_event', Text),
    Column('reporter', Text),
    Column('reporter_country', Text),
    Column('drug', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Reports_Faers_warning = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Reports_Faers_warning', Base.metadata,
    Column('drug', Text),
    Column('adverse_event', Text),
    Column('PRR', Double(53)),
    Column('ROR', Double(53)),
    Column('PRR_CI_L', Double(53)),
    Column('PRR_CI_U', Double(53)),
    Column('ROR_CI_L', Double(53)),
    Column('Warning_ROR', Text),
    Column('Warning_ROR_flag', BigInteger),
    Column('ROR_CI_U', Double(53)),
    Column('EBGM', Double(53)),
    Column('drug_event_occur', BigInteger),
    Column('drugother_eventother_occur', BigInteger),
    Column('drugother_event_occur', BigInteger),
    Column('drug_eventother_occur', BigInteger),
    Column('drug_percentage_freq', Double(53)),
    Column('event_percentage_freq', Double(53)),
    Column('primaryid', BigInteger),
    Column('total_medications', BigInteger),
    Column('event_date_year', Double(53)),
    Column('manufacturer', Text),
    Column('age_group', Text),
    Column('outcome', Text),
    Column('seriousness', Text),
    Column('reporter_country', Text),
    Column('reporter', Text),
    Column('indication', Text),
    Column('drug_interactions', BigInteger),
    Column('Interaction_detected', Text),
    Column('indication_unknown', Boolean),
    Column('Gender', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Reports_faers_anonymization = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Reports_faers_anonymization', Base.metadata,
    Column('primaryid', BigInteger),
    Column('adverse_event', Text),
    Column('event_date', DateTime(True)),
    Column('event_date_year', Double(53)),
    Column('report_type', Text),
    Column('manufacturer', Text),
    Column('sex', Text),
    Column('reporter', Text),
    Column('reporter_country', Text),
    Column('age', Double(53)),
    Column('age_group', Text),
    Column('route', Text),
    Column('drug_interactions', BigInteger),
    Column('Interaction_detected', Boolean),
    Column('indication', Text),
    Column('indication_unknown', BigInteger),
    Column('total_medications', BigInteger),
    Column('drug', Text),
    Column('outcome', Text),
    Column('seriousness', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Reports_faers_deduplicate = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Reports_faers_deduplicate', Base.metadata,
    Column('primaryid', BigInteger),
    Column('sex', Text),
    Column('age', Double(53)),
    Column('drug', Text),
    Column('adverse_event', Text),
    Column('manufacturer', Text),
    Column('event_date', DateTime(True)),
    Column('event_date_year', Double(53)),
    Column('report_type', Text),
    Column('reporter', Text),
    Column('reporter_country', Text),
    Column('age_group', Text),
    Column('route', Text),
    Column('drug_interactions', BigInteger),
    Column('Interaction_detected', Text),
    Column('indication', Text),
    Column('indication_unknown', BigInteger),
    Column('total_medications', BigInteger),
    Column('outcome', Text),
    Column('seriousness', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Reports_faers_info = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Reports_faers_info', Base.metadata,
    Column('primaryid', Text),
    Column('pt', Text),
    Column('event_date', DateTime(True)),
    Column('event_date_year', BigInteger),
    Column('rept_cod', Text),
    Column('mfr_sndr', Text),
    Column('sex', Text),
    Column('occp_cod', Text),
    Column('occr_country', Text),
    Column('age_years', Text),
    Column('age_group', Text),
    Column('route', Text),
    Column('drugname_distinct', BigInteger),
    Column('Interaction_detected', Text),
    Column('indi_pt', Text),
    Column('total_medications', BigInteger),
    Column('drug', Text),
    Column('outc_cod', Text),
    Column('seriousness', BigInteger),
    Column('serious_report', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_Reports_faers_renamed = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_Reports_faers_renamed', Base.metadata,
    Column('primaryid', Text),
    Column('adverse_event', Text),
    Column('event_date', DateTime(True)),
    Column('event_date_year', BigInteger),
    Column('report_type', Text),
    Column('manufacturer', Text),
    Column('sex', Text),
    Column('reporter', Text),
    Column('reporter_country', Text),
    Column('age', Text),
    Column('age_group', Text),
    Column('route', Text),
    Column('drug_interactions', BigInteger),
    Column('Interaction_detected', Boolean),
    Column('indication', Text),
    Column('indication_unknown', BigInteger),
    Column('total_medications', BigInteger),
    Column('drug', Text),
    Column('outcome', Text),
    Column('seriousness', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_a8b254c4af1caa40109616a71537fafe = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_a8b254c4af1caa40109616a71537fafe', Base.metadata,
    Column('drug', Text),
    Column('adverse_event', Text),
    Column('PRR_all', Double(53)),
    Column('Warning_PRR_all', Text),
    Column('Warning_PRR_flag', Text),
    Column('PRR_F', Double(53)),
    Column('PRR_M', Double(53)),
    Column('ROR_all', Double(53)),
    Column('ROR_F', Double(53)),
    Column('ROR_M', Double(53)),
    Column('PRR_CI_L_all', Double(53)),
    Column('PRR_CI_L_F', Double(53)),
    Column('PRR_CI_L_M', Double(53)),
    Column('ROR_CI_L_all', Double(53)),
    Column('Warning_ROR_all', Text),
    Column('Warning_ROR_flag', Text),
    Column('ROR_CI_L_F', Double(53)),
    Column('Warning_ROR_F', Text),
    Column('Warning_ROR_flag_F', BigInteger),
    Column('ROR_CI_L_M', Double(53)),
    Column('Warning_ROR_M', Text),
    Column('Warning_ROR_flag_M', BigInteger),
    Column('EBGM_all', Double(53)),
    Column('EBGM_F', Double(53)),
    Column('EBGM_M', Double(53)),
    Column('drug_event_occur', BigInteger),
    Column('drugother_eventother_occur', BigInteger),
    Column('drugother_event_occur', BigInteger),
    Column('drug_eventother_occur', BigInteger),
    Column('drug_percentage_freq', Double(53)),
    Column('event_percentage_freq', Double(53))
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_disproportionality_pairs_F = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_disproportionality_pairs_F', Base.metadata,
    Column('drug', Text),
    Column('adverse_event', Text),
    Column('PRR', Double(53)),
    Column('ROR', Double(53)),
    Column('PRR_CI_L', Double(53)),
    Column('PRR_CI_U', Double(53)),
    Column('ROR_CI_L', Double(53)),
    Column('ROR_CI_U', Double(53)),
    Column('EBGM', Double(53)),
    Column('drug_event_occur', BigInteger),
    Column('drugother_eventother_occur', BigInteger),
    Column('drugother_event_occur', BigInteger),
    Column('drug_eventother_occur', BigInteger),
    Column('drug_percentage_freq', Double(53)),
    Column('event_percentage_freq', Double(53)),
    Column('primaryid', BigInteger),
    Column('total_medications', BigInteger),
    Column('event_date_year', Double(53)),
    Column('manufacturer', Text),
    Column('age_group', Text),
    Column('outcome', Text),
    Column('seriousness', Text),
    Column('reporter_country', Text),
    Column('reporter', Text),
    Column('indication', Text),
    Column('drug_interactions', BigInteger),
    Column('Interaction_detected', Boolean),
    Column('indication_unknown', BigInteger)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_disproportionality_pairs_M = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_disproportionality_pairs_M', Base.metadata,
    Column('drug', Text),
    Column('adverse_event', Text),
    Column('PRR', Double(53)),
    Column('ROR', Double(53)),
    Column('PRR_CI_L', Double(53)),
    Column('PRR_CI_U', Double(53)),
    Column('ROR_CI_L', Double(53)),
    Column('ROR_CI_U', Double(53)),
    Column('EBGM', Double(53)),
    Column('drug_event_occur', BigInteger),
    Column('drugother_eventother_occur', BigInteger),
    Column('drugother_event_occur', BigInteger),
    Column('drug_eventother_occur', BigInteger),
    Column('drug_percentage_freq', Double(53)),
    Column('event_percentage_freq', Double(53)),
    Column('primaryid', BigInteger),
    Column('total_medications', BigInteger),
    Column('event_date_year', Double(53)),
    Column('manufacturer', Text),
    Column('age_group', Text),
    Column('outcome', Text),
    Column('seriousness', Text),
    Column('reporter_country', Text),
    Column('reporter', Text),
    Column('indication', Text),
    Column('drug_interactions', BigInteger),
    Column('Interaction_detected', Boolean),
    Column('indication_unknown', BigInteger)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_disproportionality_pairs_stack = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_disproportionality_pairs_stack', Base.metadata,
    Column('drug', Text),
    Column('adverse_event', Text),
    Column('PRR', Double(53)),
    Column('ROR', Double(53)),
    Column('PRR_CI_L', Double(53)),
    Column('PRR_CI_U', Double(53)),
    Column('ROR_CI_L', Double(53)),
    Column('ROR_CI_U', Double(53)),
    Column('EBGM', Double(53)),
    Column('drug_event_occur', BigInteger),
    Column('drugother_eventother_occur', BigInteger),
    Column('drugother_event_occur', BigInteger),
    Column('drug_eventother_occur', BigInteger),
    Column('drug_percentage_freq', Double(53)),
    Column('event_percentage_freq', Double(53)),
    Column('primaryid', BigInteger),
    Column('total_medications', BigInteger),
    Column('event_date_year', Double(53)),
    Column('manufacturer', Text),
    Column('age_group', Text),
    Column('outcome', Text),
    Column('seriousness', Text),
    Column('reporter_country', Text),
    Column('reporter', Text),
    Column('indication', Text),
    Column('drug_interactions', BigInteger),
    Column('Interaction_detected', Text),
    Column('indication_unknown', BigInteger),
    Column('Gender', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_disproportionality_stats = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_disproportionality_stats', Base.metadata,
    Column('drug', Text),
    Column('adverse_event', Text),
    Column('PRR_all', Double(53)),
    Column('PRR_F', Double(53)),
    Column('PRR_M', Double(53)),
    Column('ROR_all', Double(53)),
    Column('ROR_F', Double(53)),
    Column('ROR_M', Double(53)),
    Column('PRR_CI_L_all', Double(53)),
    Column('PRR_CI_L_F', Double(53)),
    Column('PRR_CI_L_M', Double(53)),
    Column('ROR_CI_L_all', Double(53)),
    Column('ROR_CI_L_F', Double(53)),
    Column('ROR_CI_L_M', Double(53)),
    Column('EBGM_all', Double(53)),
    Column('EBGM_F', Double(53)),
    Column('EBGM_M', Double(53)),
    Column('drug_event_occur', BigInteger),
    Column('drugother_eventother_occur', BigInteger),
    Column('drugother_event_occur', BigInteger),
    Column('drug_eventother_occur', BigInteger),
    Column('drug_percentage_freq', Double(53)),
    Column('event_percentage_freq', Double(53))
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_population_F = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_population_F', Base.metadata,
    Column('primaryid', BigInteger),
    Column('sex', Text),
    Column('age', Double(53)),
    Column('drug', Text),
    Column('adverse_event', Text),
    Column('manufacturer', Text),
    Column('event_date', DateTime(True)),
    Column('event_date_year', Double(53)),
    Column('report_type', Text),
    Column('reporter', Text),
    Column('reporter_country', Text),
    Column('age_group', Text),
    Column('route', Text),
    Column('drug_interactions', BigInteger),
    Column('Interaction_detected', Text),
    Column('indication', Text),
    Column('indication_unknown', BigInteger),
    Column('total_medications', BigInteger),
    Column('outcome', Text),
    Column('seriousness', Text)
)


t_SOL_PHARMACOVIGILANCE_qzJrh0Bu_population_M = Table(
    'SOL_PHARMACOVIGILANCE_qzJrh0Bu_population_M', Base.metadata,
    Column('primaryid', BigInteger),
    Column('sex', Text),
    Column('age', Double(53)),
    Column('drug', Text),
    Column('adverse_event', Text),
    Column('manufacturer', Text),
    Column('event_date', DateTime(True)),
    Column('event_date_year', Double(53)),
    Column('report_type', Text),
    Column('reporter', Text),
    Column('reporter_country', Text),
    Column('age_group', Text),
    Column('route', Text),
    Column('drug_interactions', BigInteger),
    Column('Interaction_detected', Text),
    Column('indication', Text),
    Column('indication_unknown', BigInteger),
    Column('total_medications', BigInteger),
    Column('outcome', Text),
    Column('seriousness', Text)
)


t_SOL_PRODUCT_RECO__item_family_affinities = Table(
    'SOL_PRODUCT_RECO__item_family_affinities', Base.metadata,
    Column('item_family', String(419000)),
    Column('user_id', String(419000)),
    Column('score', Double(53))
)


t_SOL_PRODUCT_RECO__item_family_affinities_for_learning = Table(
    'SOL_PRODUCT_RECO__item_family_affinities_for_learning', Base.metadata,
    Column('item_family', String(419000)),
    Column('user_id', String(419000)),
    Column('score', Double(53))
)


t_SOL_PRODUCT_RECO__item_main_color_affinities = Table(
    'SOL_PRODUCT_RECO__item_main_color_affinities', Base.metadata,
    Column('item_main_color', String(419000)),
    Column('user_id', String(419000)),
    Column('score', Double(53))
)


t_SOL_PRODUCT_RECO__item_main_color_affinities_for_learning = Table(
    'SOL_PRODUCT_RECO__item_main_color_affinities_for_learning', Base.metadata,
    Column('item_main_color', String(419000)),
    Column('user_id', String(419000)),
    Column('score', Double(53))
)


t_SOL_PRODUCT_RECO__item_type_affinities = Table(
    'SOL_PRODUCT_RECO__item_type_affinities', Base.metadata,
    Column('item_type', String(419000)),
    Column('user_id', String(419000)),
    Column('score', Double(53))
)


t_SOL_PRODUCT_RECO__item_type_affinities_for_learning = Table(
    'SOL_PRODUCT_RECO__item_type_affinities_for_learning', Base.metadata,
    Column('item_type', String(419000)),
    Column('user_id', String(419000)),
    Column('score', Double(53))
)


t_SOL_PRODUCT_RECO__item_universe_affinities = Table(
    'SOL_PRODUCT_RECO__item_universe_affinities', Base.metadata,
    Column('item_universe', String(419000)),
    Column('user_id', String(419000)),
    Column('score', Double(53))
)


t_SOL_PRODUCT_RECO__item_universe_affinities_for_learning = Table(
    'SOL_PRODUCT_RECO__item_universe_affinities_for_learning', Base.metadata,
    Column('item_universe', String(419000)),
    Column('user_id', String(419000)),
    Column('score', Double(53))
)


t_SOL_PRODUCT_RECO_collaborative_filtering_set = Table(
    'SOL_PRODUCT_RECO_collaborative_filtering_set', Base.metadata,
    Column('date', DateTime(True)),
    Column('user_id', String(419000)),
    Column('item_id', String(419000)),
    Column('is_item_to_keep', String(419000)),
    Column('is_user_to_keep', String(419000)),
    Column('week_scope', String(419000)),
    Column('at_date_user_n_interactions', BigInteger),
    Column('at_date_user_n_interactions_sum', BigInteger),
    Column('at_date_user_last_transaction_rank', BigInteger),
    Column('user_total_interactions_outlier_threshold', Double(53)),
    Column('user_age', BigInteger),
    Column('user_age_cluster', String(419000)),
    Column('item_universe', String(419000)),
    Column('item_family', String(419000)),
    Column('item_type', String(419000)),
    Column('item_main_color', String(419000)),
    Column('is_interaction_to_keep', String(419000))
)


t_SOL_PRODUCT_RECO_date_weeks = Table(
    'SOL_PRODUCT_RECO_date_weeks', Base.metadata,
    Column('date', DateTime(True)),
    Column('year', BigInteger),
    Column('week_of_year', BigInteger),
    Column('past_week_rank', BigInteger),
    Column('week_scope', Text)
)


t_SOL_PRODUCT_RECO_item_affinities = Table(
    'SOL_PRODUCT_RECO_item_affinities', Base.metadata,
    Column('item_id', String(419000)),
    Column('user_id', String(419000)),
    Column('score', Double(53))
)


t_SOL_PRODUCT_RECO_item_affinities_for_learning = Table(
    'SOL_PRODUCT_RECO_item_affinities_for_learning', Base.metadata,
    Column('item_id', String(419000)),
    Column('user_id', String(419000)),
    Column('score', Double(53))
)


t_SOL_PRODUCT_RECO_item_similarities = Table(
    'SOL_PRODUCT_RECO_item_similarities', Base.metadata,
    Column('item_id_1', String(419000)),
    Column('item_id_2', String(419000)),
    Column('similarity', Double(53))
)


t_SOL_PRODUCT_RECO_machine_learning_set = Table(
    'SOL_PRODUCT_RECO_machine_learning_set', Base.metadata,
    Column('date', DateTime(True)),
    Column('user_id', String(419000)),
    Column('item_id', String(419000)),
    Column('is_item_to_keep', String(419000)),
    Column('is_user_to_keep', String(419000)),
    Column('week_scope', String(419000)),
    Column('at_date_user_n_interactions', BigInteger),
    Column('at_date_user_n_interactions_sum', BigInteger),
    Column('at_date_user_last_transaction_rank', BigInteger),
    Column('user_total_interactions_outlier_threshold', Double(53)),
    Column('user_age', BigInteger),
    Column('user_age_cluster', String(419000)),
    Column('item_universe', String(419000)),
    Column('item_family', String(419000)),
    Column('item_type', String(419000)),
    Column('item_main_color', String(419000)),
    Column('is_interaction_to_keep', String(419000))
)


t_SOL_PRODUCT_RECO_user_item_interactions = Table(
    'SOL_PRODUCT_RECO_user_item_interactions', Base.metadata,
    Column('date', DateTime(True)),
    Column('user_id', String(419000)),
    Column('item_id', String(419000)),
    Column('is_item_to_keep', String(419000)),
    Column('is_user_to_keep', String(419000)),
    Column('week_scope', String(419000)),
    Column('at_date_user_n_interactions', BigInteger),
    Column('at_date_user_n_interactions_sum', BigInteger),
    Column('at_date_user_last_transaction_rank', BigInteger),
    Column('user_total_interactions_outlier_threshold', Double(53)),
    Column('user_age', BigInteger),
    Column('user_age_cluster', String(419000)),
    Column('item_universe', String(419000)),
    Column('item_family', String(419000)),
    Column('item_type', String(419000)),
    Column('item_main_color', String(419000)),
    Column('is_interaction_to_keep', String(419000))
)


t_TESTGEORGIA_1_hist = Table(
    'TESTGEORGIA_1_hist', Base.metadata,
    Column('conversation_id', Text),
    Column('conversation_name', Text),
    Column('knowledge_bank_id', Text),
    Column('knowledge_bank_name', Text),
    Column('llm_name', Text),
    Column('user', Text),
    Column('message_id', Text),
    Column('question', Text),
    Column('filters', Text),
    Column('file_path', Text),
    Column('answer', Text),
    Column('sources', Text),
    Column('feedback_value', Text),
    Column('feedback_choice', Text),
    Column('feedback_message', Text),
    Column('timestamp', Text),
    Column('state', Text),
    Column('llm_context', Text),
    Column('generated_media', Text)
)


t_TESTGEORGIA_1_prof = Table(
    'TESTGEORGIA_1_prof', Base.metadata,
    Column('user', Text),
    Column('profile', Text),
    Column('last_updated', DateTime)
)


t_TESTS_PARAMETERS_ANALYZER_xE7qyFTA_07c43569c6a779a89b082ec2d931 = Table(
    'TESTS_PARAMETERS_ANALYZER_xE7qyFTA_07c43569c6a779a89b082ec2d931', Base.metadata,
    Column('Unnamed: 0.1', BigInteger),
    Column('Unnamed: 0', BigInteger),
    Column('CQ_SUP_10', BigInteger),
    Column('CQ_SUP_20', Double(53)),
    Column('Bourrelet_SUP_Alpha', String(419000)),
    Column('Metrage_Total', BigInteger),
    Column('Date', DateTime(True)),
    Column('Numero_Serie_Frontal', BigInteger),
    Column('Metrage_Serie_Frontal', BigInteger),
    Column('Numero_Equipe', BigInteger),
    Column('Identifiant_Equipe', String(419000)),
    Column('Identifiant_Recette', String(419000)),
    Column('Acceleration_Calandre', Double(53)),
    Column('Vitesse_Calandre', Double(53)),
    Column('Vitesse_Calandre_Stable_100_metres', Double(53)),
    Column('Vitesse_Calandre_Stable_200_metres', Double(53)),
    Column('Vitesse_Calandre_Stable_500_metres', Double(53)),
    Column('Bande_SUP_Epaisseur', Double(53)),
    Column('Bande_SUP_Temperature', Double(53)),
    Column('Bande_SUP_Vitesse_Tapis', Double(53)),
    Column('Bande_SUP_Vitesse_Outils', Double(53)),
    Column('Bande_SUP_Ecartement_Couteaux', Double(53)),
    Column('Bande_SUP_Position_Entrefer_Outils', Double(53)),
    Column('Bande_SUP_Rupture_Approvisionnement', BigInteger),
    Column('Bourrelet_SUP_Trancanneur_Position', Double(53)),
    Column('Bourrelet_SUP_Trancanneur_Pause_Gauche', Double(53)),
    Column('Bourrelet_SUP_Trancanneur_Pause_Droite', Double(53)),
    Column('Bourrelet_SUP_Zone7_LG_Hauteur', Double(53)),
    Column('Bourrelet_SUP_Zone6_Hauteur', Double(53)),
    Column('Bourrelet_SUP_Zone5_Hauteur', Double(53)),
    Column('Bourrelet_SUP_Zone4_Hauteur', Double(53)),
    Column('Bourrelet_SUP_Zone3_Hauteur', Double(53)),
    Column('Bourrelet_SUP_Zone2_Hauteur', Double(53)),
    Column('Bourrelet_SUP_Zone1_LD_Hauteur', Double(53)),
    Column('Bourrelet_SUP_Hauteur_Moyenne', Double(53)),
    Column('Bourrelet_SUP_Hauteur_Ecart_Type_Largeur', Double(53)),
    Column('Bourrelet_SUP_Hauteur_Ecart_Type_Temporel', Double(53)),
    Column('Bourrelet_SUP_Zone7_LG_Temperature_Interne', String(419000)),
    Column('Bourrelet_SUP_Zone6_Temperature_Interne', String(419000)),
    Column('Bourrelet_SUP_Zone5_Temperature_Interne', String(419000)),
    Column('Bourrelet_SUP_Zone4_Temperature_Interne', String(419000)),
    Column('Bourrelet_SUP_Zone3_Temperature_Interne', String(419000)),
    Column('Bourrelet_SUP_Zone2_Temperature_Interne', String(419000)),
    Column('Bourrelet_SUP_Zone1_LD_Temperature_Interne', String(419000)),
    Column('Bourrelet_SUP_PN_Temperature_Surface', String(419000)),
    Column('Bourrelet_SUP_PN_Temperature_Interne', String(419000)),
    Column('Bourrelet_SUP_CG_Temperature_Interne', String(419000)),
    Column('Bourrelet_SUP_CD_Temperature_Interne', String(419000)),
    Column('Bourrelet_SUP_Temps_Sejour', BigInteger),
    Column('Skim_Epaisseur_SUP_Droite', Double(53)),
    Column('Skim_Epaisseur_SUP_Gauche', Double(53)),
    Column('C1_Intensite_Variateur', Double(53)),
    Column('C2_Intensite_Variateur', Double(53)),
    Column('Skim_Epaisseur_SUP_Moyenne', Double(53)),
    Column('C1/C2_Droite_Position_Entrefer', Double(53)),
    Column('C1/C2_Gauche_Position_Entrefer', Double(53)),
    Column('C2/C1_Friction', Double(53)),
    Column('C2_Temperature_Eau_Sortie', Double(53)),
    Column('C1_Temperature_Eau_Sortie', Double(53)),
    Column('C1_Temperature_Eau_Delta', Double(53)),
    Column('C2_Temperature_Eau_Delta', Double(53)),
    Column('C2/C1_Ratio_Intensites_Variateur', Double(53)),
    Column('C1/C2_Moyenne_Position_Entrefer', Double(53)),
    Column('defect_binary', String(419000))
)


t_TESTS_PARAMETERS_ANALYZER_xE7qyFTA_saved_studies = Table(
    'TESTS_PARAMETERS_ANALYZER_xE7qyFTA_saved_studies', Base.metadata,
    Column('study_id', String(419000)),
    Column('date', String(419000)),
    Column('user', String(419000)),
    Column('target', String(419000)),
    Column('target_info', String(419000)),
    Column('date_column', String(419000)),
    Column('date_range', String(419000)),
    Column('initial_state', String(419000)),
    Column('final_state', String(419000)),
    Column('ratio', String(419000)),
    Column('variables', String(419000)),
    Column('analysis_variables', String(419000))
)


t_TUT_LLM_PROMPTRECIPE_product_reviews_db = Table(
    'TUT_LLM_PROMPTRECIPE_product_reviews_db', Base.metadata,
    Column('text', Text),
    Column('product_category', Text)
)


t_TUT_LLM_PROMPTRECIPE_product_reviews_db_generated = Table(
    'TUT_LLM_PROMPTRECIPE_product_reviews_db_generated', Base.metadata,
    Column('text', Text),
    Column('product_category', Text),
    Column('llm_output', Text),
    Column('llm_validation_status', Text),
    Column('llm_raw_response', Text),
    Column('llm_error_message', Text),
    Column('llm_raw_query', Text)
)


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


class IjcConnectItems(Base):
    __tablename__ = 'ijc_connect_items'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_ijc_connect_items'),
        Index('index_ijc_connect_items', 'type', 'username', unique=True)
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    type: Mapped[str] = mapped_column(String(200))
    username: Mapped[Optional[str]] = mapped_column(String(128))
    data: Mapped[Optional[str]] = mapped_column(Text)


class IjcConnectStructures(Base):
    __tablename__ = 'ijc_connect_structures'
    __table_args__ = (
        PrimaryKeyConstraint('id', 'structure_hash', name='pk_ijc_connect_structures'),
    )

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    structure_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    structure: Mapped[Optional[str]] = mapped_column(Text)


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


t_my_first_dbt_model = Table(
    'my_first_dbt_model', Base.metadata,
    Column('id', Integer)
)


t_my_second_dbt_model = Table(
    'my_second_dbt_model', Base.metadata,
    Column('id', Integer)
)


t_node_92e17488_ABBVIE_DEMO_abbvie_new_data_feats_feats = Table(
    'node-92e17488_ABBVIE_DEMO_abbvie_new_data_feats_feats', Base.metadata,
    Column('Division', Text),
    Column('Date', DateTime(True)),
    Column('Paid_Views', Text),
    Column('Organic_Views', Text),
    Column('Google_Impressions', Text),
    Column('Email_Impressions', Text),
    Column('Facebook_Impressions', Text),
    Column('Affiliate_Impressions', Text),
    Column('Overall_Views', Text),
    Column('Sales', Text),
    Column('day_Date', BigInteger),
    Column('dow_Date', BigInteger),
    Column('month_Date', BigInteger),
    Column('hour_Date', BigInteger),
    Column('week_Date', BigInteger),
    Column('year_Date', BigInteger),
    Column('day_Date_1', BigInteger),
    Column('dow_Date_1', BigInteger),
    Column('month_Date_1', BigInteger),
    Column('hour_Date_1', BigInteger),
    Column('week_Date_1', BigInteger),
    Column('year_Date_1', BigInteger)
)


t_node_92e17488_DATAIKUMLOPSDEMO01_churn_modelling_demo_01_joined = Table(
    'node-92e17488_DATAIKUMLOPSDEMO01_churn_modelling_demo_01_joined', Base.metadata,
    Column('RowNumber', Text),
    Column('CustomerId', Text),
    Column('Surname', Text),
    Column('CreditScore', Text),
    Column('Geography', Text),
    Column('Gender', Text),
    Column('Age', Text),
    Column('Tenure', Text),
    Column('Balance', Text),
    Column('NumOfProducts', Text),
    Column('HasCrCard', Text),
    Column('IsActiveMember', Text),
    Column('EstimatedSalary', Text),
    Column('Exited', Text),
    Column('AgeGroup', Text),
    Column('CreditScoreCategory', Text),
    Column('BalanceSalaryRatio', Text),
    Column('TenureGroup', Text),
    Column('ProductsPerBalance', Text),
    Column('Geography_Germany', Text),
    Column('Geography_Spain', Text)
)


t_node_92e17488_MLOPSDEMOFG01_combined_feature_group_online = Table(
    'node-92e17488_MLOPSDEMOFG01_combined_feature_group_online', Base.metadata,
    Column('order_id', Text),
    Column('customer_id', Text),
    Column('product_id', Text),
    Column('purchase_amount', Double(53)),
    Column('is_reordered', BigInteger),
    Column('purchased_on', DateTime(True)),
    Column('event_time', Text),
    Column('n_days_since_last_purchase', Double(53)),
    Column('sex', BigInteger),
    Column('is_married', BigInteger),
    Column('age_18-29', Text),
    Column('age_30-39', Text),
    Column('age_40-49', Text),
    Column('age_50-59', Text),
    Column('age_60-69', Text),
    Column('age_70-plus', Text),
    Column('n_days_active', Double(53)),
    Column('category_baby_food_formula', Text),
    Column('category_baking_ingredients', Text),
    Column('category_candy_chocolate', Text),
    Column('category_chips_pretzels', Text),
    Column('category_cleaning_products', Text),
    Column('category_coffee', Text),
    Column('category_cookies_cakes', Text),
    Column('category_crackers', Text),
    Column('category_energy_granola_bars', Text),
    Column('category_frozen_meals', Text),
    Column('category_hair_care', Text),
    Column('category_ice_cream_ice', Text),
    Column('category_juice_nectars', Text),
    Column('category_packaged_cheese', Text),
    Column('category_refrigerated', Text),
    Column('category_soup_broth_bouillon', Text),
    Column('category_spices_seasonings', Text),
    Column('category_tea', Text),
    Column('category_vitamins_supplements', Text),
    Column('category_yogurt', Text)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_brand_prescribed = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_brand_prescribed', Base.metadata,
    Column('brand_prescribed', BigInteger),
    Column('count', BigInteger),
    Column('percentage', Double(53))
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_final_merged_dat = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_final_merged_dat', Base.metadata,
    Column('physician_id', BigInteger),
    Column('product_id', Text),
    Column('year', BigInteger),
    Column('quarter', BigInteger),
    Column('total_representative_visits', BigInteger),
    Column('total_sample_dropped', BigInteger),
    Column('saving_cards_dropped', BigInteger),
    Column('vouchers_dropped', BigInteger),
    Column('total_seminar_as_attendee', BigInteger),
    Column('total_seminar_as_speaker', BigInteger),
    Column('physician_hospital_affiliation', BigInteger),
    Column('physician_in_group_practice', BigInteger),
    Column('brand_web_impressions', BigInteger),
    Column('brand_ehr_impressions', BigInteger),
    Column('brand_enews_impressions', BigInteger),
    Column('brand_mobile_impressions', BigInteger),
    Column('brand_organic_web_visits', BigInteger),
    Column('brand_paidsearch_visits', BigInteger),
    Column('total_competitor_prescription', BigInteger),
    Column('new_prescriptions', BigInteger),
    Column('physician_segment', Text),
    Column('brand_prescribed', BigInteger),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('physician_gender', Text),
    Column('physician_tenure', Text),
    Column('physician_age', Double(53)),
    Column('physician_speciality', Text),
    Column('total_prescriptions', BigInteger),
    Column('brand_name', Text),
    Column('unit_price', BigInteger)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_final_processed_ = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_final_processed_', Base.metadata,
    Column('physician_id', BigInteger),
    Column('total_representative_visits', BigInteger),
    Column('total_sample_dropped', BigInteger),
    Column('saving_cards_dropped', BigInteger),
    Column('vouchers_dropped', BigInteger),
    Column('total_seminar_as_attendee', BigInteger),
    Column('total_seminar_as_speaker', BigInteger),
    Column('physician_hospital_affiliation', BigInteger),
    Column('physician_in_group_practice', BigInteger),
    Column('brand_web_impressions', BigInteger),
    Column('brand_ehr_impressions', BigInteger),
    Column('brand_enews_impressions', BigInteger),
    Column('brand_mobile_impressions', BigInteger),
    Column('brand_organic_web_visits', BigInteger),
    Column('brand_paidsearch_visits', BigInteger),
    Column('total_competitor_prescription', BigInteger),
    Column('new_prescriptions', BigInteger),
    Column('brand_prescribed', BigInteger),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('physician_age', Double(53)),
    Column('total_prescriptions', BigInteger),
    Column('unit_price', BigInteger),
    Column('physician_gender_M', Text),
    Column('physician_tenure_30-39', Text),
    Column('physician_tenure_Above 40', Text),
    Column('physician_tenure_less than 15', Text),
    Column('physician_speciality_other', Text),
    Column('physician_speciality_urology', Text),
    Column('year_2019', Text),
    Column('year_2020', Text),
    Column('quarter_2', Text),
    Column('quarter_3', Text),
    Column('quarter_4', Text)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_gender_wise_mean = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_gender_wise_mean', Base.metadata,
    Column('physician_gender', Text),
    Column('physician_id', Double(53)),
    Column('year', Double(53)),
    Column('quarter', Double(53)),
    Column('total_representative_visits', Double(53)),
    Column('total_sample_dropped', Double(53)),
    Column('saving_cards_dropped', Double(53)),
    Column('vouchers_dropped', Double(53)),
    Column('total_seminar_as_attendee', Double(53)),
    Column('total_seminar_as_speaker', Double(53)),
    Column('physician_hospital_affiliation', Double(53)),
    Column('physician_in_group_practice', Double(53)),
    Column('brand_web_impressions', Double(53)),
    Column('brand_ehr_impressions', Double(53)),
    Column('brand_enews_impressions', Double(53)),
    Column('brand_mobile_impressions', Double(53)),
    Column('brand_organic_web_visits', Double(53)),
    Column('brand_paidsearch_visits', Double(53)),
    Column('total_competitor_prescription', Double(53)),
    Column('new_prescriptions', Double(53)),
    Column('brand_prescribed', Double(53)),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('physician_age', Double(53)),
    Column('total_prescriptions', Double(53)),
    Column('unit_price', Double(53))
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_impressions_1 = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_impressions_1', Base.metadata,
    Column('brand_web_impressions', BigInteger),
    Column('brand_ehr_impressions', BigInteger),
    Column('brand_enews_impressions', BigInteger),
    Column('brand_mobile_impressions', BigInteger),
    Column('brand_organic_web_visits', BigInteger),
    Column('brand_paidsearch_visits', BigInteger)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_normalized_x_tes = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_normalized_x_tes', Base.metadata,
    Column('physician_hospital_affiliation', BigInteger),
    Column('physician_in_group_practice', BigInteger),
    Column('brand_enews_impressions', BigInteger),
    Column('brand_organic_web_visits', BigInteger),
    Column('brand_paidsearch_visits', BigInteger),
    Column('physician_age', Double(53)),
    Column('unit_price', BigInteger),
    Column('physician_gender_M', BigInteger),
    Column('physician_tenure_30-39', BigInteger),
    Column('physician_tenure_Above 40', BigInteger),
    Column('physician_tenure_less than 15', BigInteger),
    Column('physician_speciality_other', BigInteger),
    Column('physician_speciality_urology', BigInteger),
    Column('year_2019', BigInteger),
    Column('year_2020', BigInteger),
    Column('quarter_2', BigInteger),
    Column('quarter_3', BigInteger),
    Column('quarter_4', BigInteger),
    Column('total_representative_visits', Double(53)),
    Column('total_sample_dropped', Double(53)),
    Column('saving_cards_dropped', Double(53)),
    Column('vouchers_dropped', Double(53)),
    Column('total_seminar_as_attendee', Double(53)),
    Column('total_seminar_as_speaker', Double(53)),
    Column('brand_web_impressions', Double(53)),
    Column('brand_ehr_impressions', Double(53)),
    Column('brand_mobile_impressions', Double(53)),
    Column('total_competitor_prescription', Double(53)),
    Column('new_prescriptions', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('total_prescriptions', Double(53))
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_normalized_x_tra = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_normalized_x_tra', Base.metadata,
    Column('physician_hospital_affiliation', BigInteger),
    Column('physician_in_group_practice', BigInteger),
    Column('brand_enews_impressions', BigInteger),
    Column('brand_organic_web_visits', BigInteger),
    Column('brand_paidsearch_visits', BigInteger),
    Column('physician_age', Double(53)),
    Column('unit_price', BigInteger),
    Column('physician_gender_M', BigInteger),
    Column('physician_tenure_30-39', BigInteger),
    Column('physician_tenure_Above 40', BigInteger),
    Column('physician_tenure_less than 15', BigInteger),
    Column('physician_speciality_other', BigInteger),
    Column('physician_speciality_urology', BigInteger),
    Column('year_2019', BigInteger),
    Column('year_2020', BigInteger),
    Column('quarter_2', BigInteger),
    Column('quarter_3', BigInteger),
    Column('quarter_4', BigInteger),
    Column('total_representative_visits', Double(53)),
    Column('total_sample_dropped', Double(53)),
    Column('saving_cards_dropped', Double(53)),
    Column('vouchers_dropped', Double(53)),
    Column('total_seminar_as_attendee', Double(53)),
    Column('total_seminar_as_speaker', Double(53)),
    Column('brand_web_impressions', Double(53)),
    Column('brand_ehr_impressions', Double(53)),
    Column('brand_mobile_impressions', Double(53)),
    Column('total_competitor_prescription', Double(53)),
    Column('new_prescriptions', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('total_prescriptions', Double(53))
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_physician_affili = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_physician_affili', Base.metadata,
    Column('physician_id', BigInteger),
    Column('product_id', Text),
    Column('year', BigInteger),
    Column('quarter', BigInteger),
    Column('total_representative_visits', BigInteger),
    Column('total_sample_dropped', BigInteger),
    Column('saving_cards_dropped', BigInteger),
    Column('vouchers_dropped', BigInteger),
    Column('total_seminar_as_attendee', BigInteger),
    Column('total_seminar_as_speaker', BigInteger),
    Column('physician_hospital_affiliation', BigInteger),
    Column('physician_in_group_practice', BigInteger),
    Column('brand_web_impressions', BigInteger),
    Column('brand_ehr_impressions', BigInteger),
    Column('brand_enews_impressions', BigInteger),
    Column('brand_mobile_impressions', BigInteger),
    Column('brand_organic_web_visits', BigInteger),
    Column('brand_paidsearch_visits', BigInteger),
    Column('total_competitor_prescription', BigInteger),
    Column('new_prescriptions', BigInteger),
    Column('physician_segment', Text),
    Column('brand_prescribed', BigInteger),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('physician_gender', Text),
    Column('physician_tenure', Text),
    Column('physician_age', Double(53)),
    Column('physician_speciality', Text),
    Column('total_prescriptions', BigInteger),
    Column('brand_name', Text),
    Column('unit_price', BigInteger),
    Column('affiliation', Text)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_physician_specia = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_physician_specia', Base.metadata,
    Column('physician_speciality', Text),
    Column('new_prescriptions', BigInteger)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_processed_omnich = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_processed_omnich', Base.metadata,
    Column('physician_id', BigInteger),
    Column('product_id', Text),
    Column('year', BigInteger),
    Column('quarter', Text),
    Column('total_representative_visits', BigInteger),
    Column('total_sample_dropped', BigInteger),
    Column('saving_cards_dropped', BigInteger),
    Column('vouchers_dropped', BigInteger),
    Column('total_seminar_as_attendee', BigInteger),
    Column('total_seminar_as_speaker', BigInteger),
    Column('physician_hospital_affiliation', BigInteger),
    Column('physician_in_group_practice', BigInteger),
    Column('brand_web_impressions', BigInteger),
    Column('brand_ehr_impressions', BigInteger),
    Column('brand_enews_impressions', BigInteger),
    Column('brand_mobile_impressions', BigInteger),
    Column('brand_organic_web_visits', BigInteger),
    Column('brand_paidsearch_visits', BigInteger),
    Column('total_competitor_prescription', BigInteger),
    Column('new_prescriptions', BigInteger),
    Column('physician_segment', Text),
    Column('brand_prescribed', BigInteger),
    Column('total_patient_with_insurance_plan', Double(53))
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_product_data = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_product_data', Base.metadata,
    Column('product_id', Text),
    Column('brand_name', Text),
    Column('unit_price', BigInteger)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_providers_input_ = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_providers_input_', Base.metadata,
    Column('physician_id', BigInteger),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('physician_gender', Text),
    Column('physician_tenure', Text),
    Column('physician_age', BigInteger),
    Column('physician_speciality', Text)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_quarter_wise_mea = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_quarter_wise_mea', Base.metadata,
    Column('quarter', BigInteger),
    Column('physician_id', Double(53)),
    Column('year', Double(53)),
    Column('total_representative_visits', Double(53)),
    Column('total_sample_dropped', Double(53)),
    Column('saving_cards_dropped', Double(53)),
    Column('vouchers_dropped', Double(53)),
    Column('total_seminar_as_attendee', Double(53)),
    Column('total_seminar_as_speaker', Double(53)),
    Column('physician_hospital_affiliation', Double(53)),
    Column('physician_in_group_practice', Double(53)),
    Column('brand_web_impressions', Double(53)),
    Column('brand_ehr_impressions', Double(53)),
    Column('brand_enews_impressions', Double(53)),
    Column('brand_mobile_impressions', Double(53)),
    Column('brand_organic_web_visits', Double(53)),
    Column('brand_paidsearch_visits', Double(53)),
    Column('total_competitor_prescription', Double(53)),
    Column('new_prescriptions', Double(53)),
    Column('brand_prescribed', Double(53)),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('physician_age', Double(53)),
    Column('total_prescriptions', Double(53)),
    Column('unit_price', Double(53))
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_quarter_year = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_quarter_year', Base.metadata,
    Column('physician_id', BigInteger),
    Column('year', BigInteger),
    Column('quarter', BigInteger),
    Column('new_prescriptions', BigInteger)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_shap_affiliation = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_shap_affiliation', Base.metadata,
    Column('physician_id', BigInteger),
    Column('total_representative_visits', BigInteger),
    Column('total_sample_dropped', BigInteger),
    Column('saving_cards_dropped', BigInteger),
    Column('vouchers_dropped', BigInteger),
    Column('total_seminar_as_attendee', BigInteger),
    Column('total_seminar_as_speaker', BigInteger),
    Column('physician_hospital_affiliation', BigInteger),
    Column('physician_in_group_practice', BigInteger),
    Column('brand_web_impressions', BigInteger),
    Column('brand_ehr_impressions', BigInteger),
    Column('brand_enews_impressions', BigInteger),
    Column('brand_mobile_impressions', BigInteger),
    Column('brand_organic_web_visits', BigInteger),
    Column('brand_paidsearch_visits', BigInteger),
    Column('total_competitor_prescription', BigInteger),
    Column('new_prescriptions', BigInteger),
    Column('brand_prescribed', BigInteger),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('physician_age', Double(53)),
    Column('total_prescriptions', BigInteger),
    Column('unit_price', BigInteger),
    Column('physician_gender_M', BigInteger),
    Column('physician_tenure_30-39', BigInteger),
    Column('physician_tenure_Above 40', BigInteger),
    Column('physician_tenure_less than 15', BigInteger),
    Column('physician_speciality_other', BigInteger),
    Column('physician_speciality_urology', BigInteger),
    Column('year_2019', BigInteger),
    Column('year_2020', BigInteger),
    Column('quarter_2', BigInteger),
    Column('quarter_3', BigInteger),
    Column('quarter_4', BigInteger),
    Column('proba_0', Double(53)),
    Column('proba_1', Double(53)),
    Column('prediction', BigInteger),
    Column('explanations', Text),
    Column('affiliation', Text)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_shap_physaffil = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_shap_physaffil', Base.metadata,
    Column('physician_id', BigInteger),
    Column('total_representative_visits', BigInteger),
    Column('total_sample_dropped', BigInteger),
    Column('saving_cards_dropped', BigInteger),
    Column('vouchers_dropped', BigInteger),
    Column('total_seminar_as_attendee', BigInteger),
    Column('total_seminar_as_speaker', BigInteger),
    Column('physician_hospital_affiliation', BigInteger),
    Column('physician_in_group_practice', BigInteger),
    Column('brand_web_impressions', BigInteger),
    Column('brand_ehr_impressions', BigInteger),
    Column('brand_enews_impressions', BigInteger),
    Column('brand_mobile_impressions', BigInteger),
    Column('brand_organic_web_visits', BigInteger),
    Column('brand_paidsearch_visits', BigInteger),
    Column('total_competitor_prescription', BigInteger),
    Column('new_prescriptions', BigInteger),
    Column('brand_prescribed', BigInteger),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('physician_age', Double(53)),
    Column('total_prescriptions', BigInteger),
    Column('unit_price', BigInteger),
    Column('physician_gender_M', BigInteger),
    Column('physician_tenure_30-39', BigInteger),
    Column('physician_tenure_Above 40', BigInteger),
    Column('physician_tenure_less than 15', BigInteger),
    Column('physician_speciality_other', BigInteger),
    Column('physician_speciality_urology', BigInteger),
    Column('year_2019', BigInteger),
    Column('year_2020', BigInteger),
    Column('quarter_2', BigInteger),
    Column('quarter_3', BigInteger),
    Column('quarter_4', BigInteger),
    Column('proba_0', Double(53)),
    Column('proba_1', Double(53)),
    Column('prediction', Text),
    Column('explanations', Text)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_sum_of_shap = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_sum_of_shap', Base.metadata,
    Column('brand_prescribed', BigInteger),
    Column('feature_key', Text),
    Column('SHAP_val', Double(53))
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_test = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_test', Base.metadata,
    Column('physician_id', BigInteger),
    Column('total_representative_visits', BigInteger),
    Column('total_sample_dropped', BigInteger),
    Column('saving_cards_dropped', BigInteger),
    Column('vouchers_dropped', BigInteger),
    Column('total_seminar_as_attendee', BigInteger),
    Column('total_seminar_as_speaker', BigInteger),
    Column('physician_hospital_affiliation', BigInteger),
    Column('physician_in_group_practice', BigInteger),
    Column('brand_web_impressions', BigInteger),
    Column('brand_ehr_impressions', BigInteger),
    Column('brand_enews_impressions', BigInteger),
    Column('brand_mobile_impressions', BigInteger),
    Column('brand_organic_web_visits', BigInteger),
    Column('brand_paidsearch_visits', BigInteger),
    Column('total_competitor_prescription', BigInteger),
    Column('new_prescriptions', BigInteger),
    Column('brand_prescribed', BigInteger),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('physician_age', Double(53)),
    Column('total_prescriptions', BigInteger),
    Column('unit_price', BigInteger),
    Column('physician_gender_M', Text),
    Column('physician_tenure_30-39', Text),
    Column('physician_tenure_Above 40', Text),
    Column('physician_tenure_less than 15', Text),
    Column('physician_speciality_other', Text),
    Column('physician_speciality_urology', Text),
    Column('year_2019', Text),
    Column('year_2020', Text),
    Column('quarter_2', Text),
    Column('quarter_3', Text),
    Column('quarter_4', Text)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_test_scored = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_test_scored', Base.metadata,
    Column('physician_id', BigInteger),
    Column('total_representative_visits', BigInteger),
    Column('total_sample_dropped', BigInteger),
    Column('saving_cards_dropped', BigInteger),
    Column('vouchers_dropped', BigInteger),
    Column('total_seminar_as_attendee', BigInteger),
    Column('total_seminar_as_speaker', BigInteger),
    Column('physician_hospital_affiliation', BigInteger),
    Column('physician_in_group_practice', BigInteger),
    Column('brand_web_impressions', BigInteger),
    Column('brand_ehr_impressions', BigInteger),
    Column('brand_enews_impressions', BigInteger),
    Column('brand_mobile_impressions', BigInteger),
    Column('brand_organic_web_visits', BigInteger),
    Column('brand_paidsearch_visits', BigInteger),
    Column('total_competitor_prescription', BigInteger),
    Column('new_prescriptions', BigInteger),
    Column('brand_prescribed', BigInteger),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('physician_age', Double(53)),
    Column('total_prescriptions', BigInteger),
    Column('unit_price', BigInteger),
    Column('physician_gender_M', BigInteger),
    Column('physician_tenure_30-39', BigInteger),
    Column('physician_tenure_Above 40', BigInteger),
    Column('physician_tenure_less than 15', BigInteger),
    Column('physician_speciality_other', BigInteger),
    Column('physician_speciality_urology', BigInteger),
    Column('year_2019', BigInteger),
    Column('year_2020', BigInteger),
    Column('quarter_2', BigInteger),
    Column('quarter_3', BigInteger),
    Column('quarter_4', BigInteger),
    Column('proba_0', Double(53)),
    Column('proba_1', Double(53)),
    Column('prediction', Text),
    Column('explanations', Text),
    Column('smmd_savedModelId', Text),
    Column('smmd_modelVersion', Text),
    Column('smmd_fullModelId', Text),
    Column('smmd_predictionTime', DateTime(True))
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_test_scored_prep = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_test_scored_prep', Base.metadata,
    Column('physician_id', BigInteger),
    Column('total_representative_visits', BigInteger),
    Column('total_sample_dropped', BigInteger),
    Column('saving_cards_dropped', BigInteger),
    Column('vouchers_dropped', BigInteger),
    Column('total_seminar_as_attendee', BigInteger),
    Column('total_seminar_as_speaker', BigInteger),
    Column('physician_hospital_affiliation', BigInteger),
    Column('physician_in_group_practice', BigInteger),
    Column('brand_web_impressions', BigInteger),
    Column('brand_ehr_impressions', BigInteger),
    Column('brand_enews_impressions', BigInteger),
    Column('brand_mobile_impressions', BigInteger),
    Column('brand_organic_web_visits', BigInteger),
    Column('brand_paidsearch_visits', BigInteger),
    Column('total_competitor_prescription', BigInteger),
    Column('new_prescriptions', BigInteger),
    Column('brand_prescribed', BigInteger),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('physician_age', Double(53)),
    Column('total_prescriptions', BigInteger),
    Column('unit_price', BigInteger),
    Column('physician_gender_M', BigInteger),
    Column('physician_tenure_30-39', BigInteger),
    Column('physician_tenure_Above 40', BigInteger),
    Column('physician_tenure_less than 15', BigInteger),
    Column('physician_speciality_other', BigInteger),
    Column('physician_speciality_urology', BigInteger),
    Column('year_2019', BigInteger),
    Column('year_2020', BigInteger),
    Column('quarter_2', BigInteger),
    Column('quarter_3', BigInteger),
    Column('quarter_4', BigInteger),
    Column('proba_0', Double(53)),
    Column('proba_1', Double(53)),
    Column('prediction', Text)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_test_scored_shap = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_test_scored_shap', Base.metadata,
    Column('physician_id', BigInteger),
    Column('total_representative_visits', BigInteger),
    Column('total_sample_dropped', BigInteger),
    Column('saving_cards_dropped', BigInteger),
    Column('vouchers_dropped', BigInteger),
    Column('total_seminar_as_attendee', BigInteger),
    Column('total_seminar_as_speaker', BigInteger),
    Column('physician_hospital_affiliation', BigInteger),
    Column('physician_in_group_practice', BigInteger),
    Column('brand_web_impressions', BigInteger),
    Column('brand_ehr_impressions', BigInteger),
    Column('brand_enews_impressions', BigInteger),
    Column('brand_mobile_impressions', BigInteger),
    Column('brand_organic_web_visits', BigInteger),
    Column('brand_paidsearch_visits', BigInteger),
    Column('total_competitor_prescription', BigInteger),
    Column('new_prescriptions', BigInteger),
    Column('brand_prescribed', BigInteger),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('physician_age', Double(53)),
    Column('total_prescriptions', BigInteger),
    Column('unit_price', BigInteger),
    Column('physician_gender_M', BigInteger),
    Column('physician_tenure_30-39', BigInteger),
    Column('physician_tenure_Above 40', BigInteger),
    Column('physician_tenure_less than 15', BigInteger),
    Column('physician_speciality_other', BigInteger),
    Column('physician_speciality_urology', BigInteger),
    Column('year_2019', BigInteger),
    Column('year_2020', BigInteger),
    Column('quarter_2', BigInteger),
    Column('quarter_3', BigInteger),
    Column('quarter_4', BigInteger),
    Column('proba_0', Double(53)),
    Column('proba_1', Double(53)),
    Column('prediction', Text),
    Column('feature_key', Text),
    Column('SHAP_val', Double(53)),
    Column('sign', Text)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_train = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_train', Base.metadata,
    Column('physician_id', BigInteger),
    Column('total_representative_visits', BigInteger),
    Column('total_sample_dropped', BigInteger),
    Column('saving_cards_dropped', BigInteger),
    Column('vouchers_dropped', BigInteger),
    Column('total_seminar_as_attendee', BigInteger),
    Column('total_seminar_as_speaker', BigInteger),
    Column('physician_hospital_affiliation', BigInteger),
    Column('physician_in_group_practice', BigInteger),
    Column('brand_web_impressions', BigInteger),
    Column('brand_ehr_impressions', BigInteger),
    Column('brand_enews_impressions', BigInteger),
    Column('brand_mobile_impressions', BigInteger),
    Column('brand_organic_web_visits', BigInteger),
    Column('brand_paidsearch_visits', BigInteger),
    Column('total_competitor_prescription', BigInteger),
    Column('new_prescriptions', BigInteger),
    Column('brand_prescribed', BigInteger),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('physician_age', Double(53)),
    Column('total_prescriptions', BigInteger),
    Column('unit_price', BigInteger),
    Column('physician_gender_M', Text),
    Column('physician_tenure_30-39', Text),
    Column('physician_tenure_Above 40', Text),
    Column('physician_tenure_less than 15', Text),
    Column('physician_speciality_other', Text),
    Column('physician_speciality_urology', Text),
    Column('year_2019', Text),
    Column('year_2020', Text),
    Column('quarter_2', Text),
    Column('quarter_3', Text),
    Column('quarter_4', Text)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_transactions_pre = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_transactions_pre', Base.metadata,
    Column('physician_id', BigInteger),
    Column('product_id', Text),
    Column('year', BigInteger),
    Column('quarter', BigInteger),
    Column('total_prescriptions', BigInteger)
)


t_node_92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_year_wise_mean = Table(
    'node-92e17488_TEAMINITIATIVEBRANDADOPTIONMODEL_year_wise_mean', Base.metadata,
    Column('year', BigInteger),
    Column('physician_id', Double(53)),
    Column('quarter', Double(53)),
    Column('total_representative_visits', Double(53)),
    Column('total_sample_dropped', Double(53)),
    Column('saving_cards_dropped', Double(53)),
    Column('vouchers_dropped', Double(53)),
    Column('total_seminar_as_attendee', Double(53)),
    Column('total_seminar_as_speaker', Double(53)),
    Column('physician_hospital_affiliation', Double(53)),
    Column('physician_in_group_practice', Double(53)),
    Column('brand_web_impressions', Double(53)),
    Column('brand_ehr_impressions', Double(53)),
    Column('brand_enews_impressions', Double(53)),
    Column('brand_mobile_impressions', Double(53)),
    Column('brand_organic_web_visits', Double(53)),
    Column('brand_paidsearch_visits', Double(53)),
    Column('total_competitor_prescription', Double(53)),
    Column('new_prescriptions', Double(53)),
    Column('brand_prescribed', Double(53)),
    Column('total_patient_with_insurance_plan', Double(53)),
    Column('urban_population_perc_in_physician_locality', Double(53)),
    Column('percent_population_with_health_insurance_in_last10q', Double(53)),
    Column('physician_age', Double(53)),
    Column('total_prescriptions', Double(53)),
    Column('unit_price', Double(53))
)


t_node_fa02ac96_PROJECT1_drug_class_filtered = Table(
    'node-fa02ac96_PROJECT1_drug_class_filtered', Base.metadata,
    Column('id', Integer),
    Column('name', String(500)),
    Column('is_group', SmallInteger),
    Column('source', String(100))
)


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


t_snapshot_recipe = Table(
    'snapshot_recipe', Base.metadata,
    Column('row_id', Integer),
    Column('recipe_id', Text),
    Column('ing_id', Text),
    Column('quantity', Integer),
    Column('dbt_scd_id', Text),
    Column('dbt_updated_at', DateTime),
    Column('dbt_valid_from', DateTime),
    Column('dbt_valid_to', DateTime)
)


t_snapshot_test = Table(
    'snapshot_test', Base.metadata,
    Column('id', Integer),
    Column('date', Text),
    Column('value', Integer),
    Column('dbt_scd_id', Text),
    Column('dbt_updated_at', Text),
    Column('dbt_valid_from', Text),
    Column('dbt_valid_to', Text)
)


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


t_test_1_1 = Table(
    'test_1_1', Base.metadata,
    Column('id', Integer),
    Column('drug_class2', String(500)),
    Column('ddi_risk', String(200))
)


t_test_1_2 = Table(
    'test_1_2', Base.metadata,
    Column('drug_class_id', Integer),
    Column('ddi_risk', String(200)),
    Column('name', String(500))
)


t_test_2_1 = Table(
    'test_2_1', Base.metadata,
    Column('id', Integer),
    Column('meddra_name', String(200)),
    Column('struct_id', Integer)
)


t_test_2_2 = Table(
    'test_2_2', Base.metadata,
    Column('struct_id', Integer),
    Column('meddra_name', String(200)),
    Column('name', String(250))
)


t_test_3 = Table(
    'test_3', Base.metadata,
    Column('struct_id', Integer),
    Column('drug_class_id', Integer),
    Column('drug_name', String(500)),
    Column('struct_name', String(250)),
    Column('comparison', Text)
)


t_test_coffee_recipe = Table(
    'test_coffee_recipe', Base.metadata,
    Column('row_id', Integer),
    Column('recipe_id', Text),
    Column('ing_id', Text),
    Column('quantity', Integer)
)


t_test_snap = Table(
    'test_snap', Base.metadata,
    Column('id', Integer),
    Column('date', Text),
    Column('value', Integer)
)


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
