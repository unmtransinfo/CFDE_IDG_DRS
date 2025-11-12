"""
Request models for API endpoints
Defines the structure and validation for incoming request bodies
"""

from pydantic import BaseModel, validator, Field
from typing import List, Optional


class TargetBatchRequest(BaseModel):
    """
    Request model for batch target queries
    
    Example:
        {
            "gene_symbols": ["EGFR", "TP53", "BRAF"],
            "format": "json"
        }
    """
    gene_symbols: List[str] = Field(
        ...,
        description="List of gene symbols to query",
        example=["EGFR", "TP53", "BRAF"],
        min_items=1,
        max_items=100
    )
    format: Optional[str] = Field(
        "json",
        description="Response format: json, csv, or tsv",
        pattern="^(json|csv|tsv)$"
    )
    
    @validator('gene_symbols')
    def validate_gene_symbols(cls, v):
        """Validate the gene symbols list"""
        if not v:
            raise ValueError("gene_symbols cannot be empty")
        
        if len(v) > 100:
            raise ValueError("Maximum 100 gene symbols allowed per batch request")
        
        # Check for duplicates
        if len(v) != len(set(v)):
            raise ValueError("Duplicate gene symbols found in the list")
        
        # Basic validation for each gene symbol
        for symbol in v:
            if not symbol or not isinstance(symbol, str):
                raise ValueError(f"Invalid gene symbol: {symbol}")
            if len(symbol.strip()) == 0:
                raise ValueError("Gene symbols cannot be empty or whitespace")
            if len(symbol) > 20:
                raise ValueError(f"Gene symbol too long: {symbol} (max 20 characters)")
        
        return v


class LigandBatchRequest(BaseModel):
    """
    Request model for batch ligand queries
    
    Example:
        {
            "ligand_ids": ["haloperidol", "aspirin", "imatinib"],
            "format": "json"
        }
    """
    ligand_ids: List[str] = Field(
        ...,
        description="List of ligand identifiers to query",
        example=["haloperidol", "aspirin", "imatinib"],
        min_items=1,
        max_items=100
    )
    format: Optional[str] = Field(
        "json",
        description="Response format: json, csv, or tsv",
        pattern="^(json|csv|tsv)$"
    )
    
    @validator('ligand_ids')
    def validate_ligand_ids(cls, v):
        """Validate the ligand IDs list"""
        if not v:
            raise ValueError("ligand_ids cannot be empty")
        
        if len(v) > 100:
            raise ValueError("Maximum 100 ligand IDs allowed per batch request")
        
        # Check for duplicates
        if len(v) != len(set(v)):
            raise ValueError("Duplicate ligand IDs found in the list")
        
        # Basic validation for each ligand ID
        for ligand_id in v:
            if not ligand_id or not isinstance(ligand_id, str):
                raise ValueError(f"Invalid ligand ID: {ligand_id}")
            if len(ligand_id.strip()) == 0:
                raise ValueError("Ligand IDs cannot be empty or whitespace")
            if len(ligand_id) > 100:
                raise ValueError(f"Ligand ID too long: {ligand_id} (max 100 characters)")
        
        return v


class DiseaseBatchRequest(BaseModel):
    """
    Request model for batch disease queries
    
    Example:
        {
            "disease_names": ["asthma", "diabetes", "alzheimer disease"],
            "format": "json"
        }
    """
    disease_names: List[str] = Field(
        ...,
        description="List of disease names to query",
        example=["asthma", "diabetes", "alzheimer disease"],
        min_items=1,
        max_items=100
    )
    format: Optional[str] = Field(
        "json",
        description="Response format: json, csv, or tsv",
        pattern="^(json|csv|tsv)$"
    )
    
    @validator('disease_names')
    def validate_disease_names(cls, v):
        """Validate the disease names list"""
        if not v:
            raise ValueError("disease_names cannot be empty")
        
        if len(v) > 100:
            raise ValueError("Maximum 100 disease names allowed per batch request")
        
        # Check for duplicates
        if len(v) != len(set(v)):
            raise ValueError("Duplicate disease names found in the list")
        
        # Basic validation for each disease name
        for disease_name in v:
            if not disease_name or not isinstance(disease_name, str):
                raise ValueError(f"Invalid disease name: {disease_name}")
            if len(disease_name.strip()) == 0:
                raise ValueError("Disease names cannot be empty or whitespace")
            if len(disease_name) > 200:
                raise ValueError(f"Disease name too long: {disease_name} (max 200 characters)")
        
        return v