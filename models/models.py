from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional

from typing import Union


class Sample(BaseModel):
    sample_id : str
    qc : dict
    pct_N_bases: float
    sample_name: str
    num_aligned_reads: int
    pct_covered_bases: float
    longest_no_N_run: int
    on_target: float
    fasta: str
    variants: List[dict]
    pangolin: dict


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    fullname: Union[str, None] = None
    disabled: Union[bool, None] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    fullname: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str