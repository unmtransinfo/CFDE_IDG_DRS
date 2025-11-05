#!/usr/bin/env python3
"""
Test script for Target -> Diseases endpoint
Tests the service layer directly
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.target_service import TargetService

async def test_target_with_diseases():
    """Test getting target with disease associations"""

    print("="*60)
    print("Testing Target → Diseases Service")
    print("="*60)

    # Test with EGFR (known to have many disease associations)
    test_genes = ["EGFR", "TP53", "ACE2"]

    for gene in test_genes:
        print(f"\n{'='*60}")
        print(f"Testing: {gene}")
        print(f"{'='*60}")

        try:
            result = await TargetService.get_target_with_diseases(gene, max_diseases=5)

            if result.success and result.data:
                print(f"✅ SUCCESS")
                print(f"   Target: {result.data.target_name}")
                print(f"   Gene Symbol: {result.data.gene_symbol}")
                print(f"   UniProt ID: {result.data.uniprot_id}")
                print(f"   Development Level: {result.data.development_level}")
                print(f"   Disease Count: {result.data.disease_count}")
                print(f"\n   Associated Diseases:")
                for i, disease in enumerate(result.data.associated_diseases[:5], 1):
                    print(f"      {i}. {disease.disease_name}")
                    print(f"         MONDO ID: {disease.mondo_id}")
                    if disease.description:
                        desc = disease.description[:80] + "..." if len(disease.description) > 80 else disease.description
                        print(f"         Description: {desc}")
            else:
                print(f"❌ FAILED: {result.message}")

        except Exception as e:
            print(f"❌ ERROR: {str(e)}")

    print(f"\n{'='*60}")
    print("Test Complete!")
    print(f"{'='*60}")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_target_with_diseases())
