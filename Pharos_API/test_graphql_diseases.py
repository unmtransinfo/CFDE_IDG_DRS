#!/usr/bin/env python3
"""
Test GraphQL query for target diseases
"""

import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.graphql_client import query_pharos

async def test_queries():
    """Test different GraphQL query structures"""

    # Test 1: Basic target query (should work)
    print("Test 1: Basic Target Query")
    query1 = """
    query GetTarget($gene_symbol: String!) {
        target(q: {sym: $gene_symbol}) {
            name
            sym
            tdl
        }
    }
    """
    try:
        result = await query_pharos(query1, {"gene_symbol": "EGFR"})
        print(f"✅ Basic query works: {result['data']['target']['name']}")
    except Exception as e:
        print(f"❌ Basic query failed: {e}")

    # Test 2: Try to get disease count
    print("\nTest 2: Target with Disease Count")
    query2 = """
    query GetTargetDiseaseCount($gene_symbol: String!) {
        target(q: {sym: $gene_symbol}) {
            name
            sym
            diseaseCount
        }
    }
    """
    try:
        result = await query_pharos(query2, {"gene_symbol": "EGFR"})
        print(f"✅ Disease count query works")
        print(f"   Result: {result}")
    except Exception as e:
        print(f"❌ Disease count query failed: {e}")

    # Test 3: Try diseases field with limit
    print("\nTest 3: Target with Top Diseases")
    query3 = """
    query GetTargetDiseases($gene_symbol: String!) {
        target(q: {sym: $gene_symbol}) {
            name
            sym
            diseases(top: 3) {
                name
                mondoID
            }
        }
    }
    """
    try:
        result = await query_pharos(query3, {"gene_symbol": "EGFR"})
        print(f"✅ Diseases query works")
        if 'data' in result and result['data'].get('target'):
            target = result['data']['target']
            print(f"   Target: {target['name']}")
            if 'diseases' in target and target['diseases']:
                print(f"   Found {len(target['diseases'])} diseases:")
                for disease in target['diseases'][:3]:
                    print(f"      - {disease.get('name')}")
            else:
                print("   No diseases found")
    except Exception as e:
        print(f"❌ Diseases query failed: {e}")

    # Test 4: Try diseases without limit
    print("\nTest 4: Target with All Diseases (no limit)")
    query4 = """
    query GetTargetDiseases($gene_symbol: String!) {
        target(q: {sym: $gene_symbol}) {
            name
            sym
            diseases {
                name
                mondoID
            }
        }
    }
    """
    try:
        result = await query_pharos(query4, {"gene_symbol": "EGFR"})
        print(f"✅ Diseases query (no limit) works")
        if 'data' in result and result['data'].get('target'):
            target = result['data']['target']
            if 'diseases' in target and target['diseases']:
                print(f"   Found {len(target['diseases'])} diseases")
    except Exception as e:
        print(f"❌ Diseases query (no limit) failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_queries())
