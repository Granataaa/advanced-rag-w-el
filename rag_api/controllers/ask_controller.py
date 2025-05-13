from flask import request, jsonify
from rag_service import query_rag
from models.models import RagResponse

def ask_get():
    query = request.args.get('query')
    k_ric = request.args.get('k_ric')
    LLMHelp = request.args.get('LLMHelp')

    if not query:
        return {"error": "Missing 'query' parameter"}, 400
    if not k_ric:
        return {"error": "Missing 'k_ric' parameter"}, 400
    if not LLMHelp:
        return {"error": "Missing 'LLMHelp' parameter"}, 400

    res = query_rag(query, k_ric, LLMHelp)

    return RagResponse(**res).model_dump()