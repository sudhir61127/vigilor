"""
RAG Tool for retrieving medical documents and patient reports.
Uses the FAISS vector store to search for relevant medical information.
"""

from typing import Optional
from app.rag.retriever import search_documents


def search_medical_reports(query: str, top_k: int = 3) -> dict:
    """
    Search the RAG vector store for relevant medical reports.
    
    Args:
        query: The search query
        top_k: Number of top results to return (default: 3)
    
    Returns:
        dict with 'success' status and 'results' or 'error'
    """
    try:
        results = search_documents(query, top_k=top_k)
        
        if not results:
            return {
                "success": False,
                "error": "No relevant medical reports found for this query."
            }
        
        # Format results for readability
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append({
                "rank": i,
                "patient_id": result.get("metadata", {}).get("patient_id", "Unknown"),
                "report_type": result.get("metadata", {}).get("report_type", "Unknown"),
                "content_preview": result.get("content", "")[:300] + "..." if len(result.get("content", "")) > 300 else result.get("content", ""),
                "relevance_score": result.get("score", 0)
            })
        
        return {
            "success": True,
            "query": query,
            "result_count": len(formatted_results),
            "results": formatted_results
        }
    
    except FileNotFoundError:
        return {
            "success": False,
            "error": "RAG index not initialized. Please run build_rag.py first."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"RAG search failed: {str(e)}"
        }


def get_patient_report(patient_id: str, report_type: str) -> dict:
    """
    Get a specific report for a patient.
    
    Args:
        patient_id: Patient identifier (e.g., 'PAT001', 'PAT-001')
        report_type: Type of report (blood, mri, ct, xray, ecg)
    
    Returns:
        dict with report content or error message
    """
    # Normalize patient ID
    if not patient_id.startswith("PAT"):
        patient_id = f"PAT{patient_id.zfill(3)}"
    
    query = f"{report_type} report for {patient_id}"
    
    try:
        results = search_documents(query, top_k=1)
        
        if results and results[0].get("metadata", {}).get("patient_id") == patient_id:
            return {
                "success": True,
                "patient_id": patient_id,
                "report_type": report_type,
                "content": results[0].get("content", ""),
                "source": results[0].get("metadata", {}).get("source", "")
            }
        
        return {
            "success": False,
            "error": f"Could not find {report_type} report for patient {patient_id}."
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to retrieve report: {str(e)}"
        }
