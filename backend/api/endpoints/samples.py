from re import M
from typing import Optional, Union
from fastapi import Depends, HTTPException, Query
from starlette.responses import JSONResponse
from api.router import APIRouter

import pandas as pd 

from crud import *

from models import *
from authentication import *

from pprint import pprint
router = APIRouter()

import time

# Gets all samples 
@router.get("/", response_model = list[Sample])
async def read_samples(
    current_user: User = Depends(get_current_active_user),
    advanced_search: Optional[bool] = False,
    ): 

    sample_list = await samples.get_samples(advanced_search)
    return sample_list

# Gets single specific sample
@router.get("/{sample_id}", response_model=list[Sample])
async def single_sample(
    sample_id: str,
    current_user: User = Depends(get_current_active_user)
    ):
    sample_info = await samples.get_single(sample_id, id_field='sample_id')
    if len(sample_info) == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sample can't be found in database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    matrix = await get_matrix()
    del matrix[0]['_id']
    df = pd.DataFrame(matrix[0])
    if sample_id in df.columns:
        distances = abs(df.subtract(df[sample_id], axis = 0)).sum()
        similar_samples = distances[abs(distances) < 10].index.tolist()
        sample_info[0]['similar_samples'] = similar_samples
    return sample_info


# Delete multiple samples
@router.delete("/", response_model=list[Sample])
async def delete_samples(
    sample_ids: list[str] | None = Query(default=None),
    current_user: User = Depends(get_current_active_user)
    ):
    if current_user['scope'] == 'user':
        raise HTTPException(status_code=403, detail="Not allowed")
    samples_to_delete = await samples.get_multiple(sample_ids, id_field='sample_id')
    await samples.delete_multiple(sample_ids, id_field='sample_id')
    return samples_to_delete

# Gets multiple specified samples
@router.get("/multiple/", response_model=list[Sample])
async def multiple_samples(
    sample_ids:list[str] | None = Query(default=None),
    current_user: User = Depends(get_current_active_user)
    ):
    return await samples.get_multiple(sample_ids, id_field='sample_id')

# Gets all samples with matching specified pango type
@router.get("/pango/", response_model=GroupedSamples)
async def get_samples_with_pangotype(
    pangolin:str ,
    current_user: User = Depends(get_current_active_user)
    ):
    samples_list = await samples.get_pangotype_samples(pangolin)
    graph_list = group_by_dict(samples_list)
    return {'samples': samples_list, 'graph': graph_list}

# Gets all samples with matching specified variant
@router.get("/variant/",response_model=GroupedSamples)
async def get_samples_with_variant(
    variant:str ,
    current_user: User = Depends(get_current_active_user)
    ):
    samples_list = await samples.get_variant_samples(variant=variant)
    graph_list = group_by_dict(samples_list)
    return {'samples': samples_list, 'graph': graph_list}

# Gets all samples with matching specified nextclade
@router.get("/nextclade/", response_model=GroupedSamples)
async def get_samples_with_nextclade(
    nextclade:str ,
    current_user: User = Depends(get_current_active_user)
    ):
    samples_list = await samples.get_nextclade_samples(nextclade=nextclade)
    graph_list = group_by_dict(samples_list)
    return {'samples': samples_list, 'graph': graph_list}

def group_by_dict(samples:dict):
    # group by key
    graph_list = {}
    for sample in samples:
        sample_time = (time.strftime('%Y-%m-%w', time.localtime(sample['collection_date']['$date']/1000))) # convert epoch to datetime
        if sample_time in graph_list:
            graph_list[sample_time] += 1
        else:
            graph_list[sample_time] = 1
    # sort by key
    graph_list = {k: v for k, v in sorted(graph_list.items(), key=lambda item: item[0])}
    graph_list = [{'date': k, 'count': v} for k, v in graph_list.items()]
    return graph_list
