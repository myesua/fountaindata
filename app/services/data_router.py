import asyncio
from typing import List, Dict, Any
from metrics.metrics import RECORDS_PROCESSED_TOTAL 

async def route_data(source_id: str, valid_data: List[Dict[str, Any]], invalid_data: List[Dict[str, Any]]):
    valid_count = len(valid_data)
    invalid_count = len(invalid_data)
    
    RECORDS_PROCESSED_TOTAL.labels(source_id=source_id, status='valid').inc(valid_count)
    RECORDS_PROCESSED_TOTAL.labels(source_id=source_id, status='invalid').inc(invalid_count)

    await asyncio.gather(
        _push_to_clean_sink(source_id, valid_data),
        _push_to_quarantine(source_id, invalid_data)
    )

async def _push_to_clean_sink(source_id: str, data: List[Dict[str, Any]]):
    if not data: return
    print(f"[DATA ROUTER] Pushing {len(data)} valid records to CLEAN DATA queue for Source: {source_id}")
    await asyncio.sleep(0.005)

async def _push_to_quarantine(source_id: str, data: List[Dict[str, Any]]):
    if not data: return
    print(f"[DATA ROUTER] Pushing {len(data)} invalid records to QUARANTINE queue for Source: {source_id}")
    await asyncio.sleep(0.010)