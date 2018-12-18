from graphene import ObjectType, String, Boolean, ID, List, Field, Int, List, DateTime, Schema
import arxiv
import json
import os
from collections import namedtuple

def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

# class SummaryDetail(ObjectType):
#     base = String()
#     language = String()
#     value = String()
#     type = String()

class AuthorDetail(ObjectType):
    name = String()

# class Link(ObjectType):
#     type = String()
#     rel = String()
#     href = String()

class Tag(ObjectType):
    label = String()
    term = String()
    scheme = String()

class ArxivPrimaryCategory(ObjectType):
    term = String()
    scheme = String()

class TitleDetail(ObjectType):
    base = String()
    language = String()
    value = String()
    type = String()

class Paper(ObjectType):
    # summary_details = Field(SummaryDetail)
    # author = String()
    id = ID()
    # author_detail = Field(AuthorDetail)
    # guidislink = Boolean()
    # published_parsed = List(Int)
    pdf_url = String()
    # affiliation = String()
    published = String()
    arxiv_comment = String()
    # links = Field(List(Link))
    title = String()
    # journal_reference = String()
    authors = List(String)
    arxiv_url = String()
    # updated_parsed = List(Int)
    doi = String()
    tags = Field(List(Tag))
    arxiv_primary_category = Field(ArxivPrimaryCategory)
    # title_detail = Field(TitleDetail)
    updated = String()
    summary = String()

class Query(ObjectType):
    getListOfPapers = List(Paper, search_query=String(required=True), max_results=Int(required=True), start=Int(required=True),
                sort_by=String(required=False), sort_order=String(required=False))
    
    def resolve_getListOfPapers(self, info, search_query, max_results, start, sort_by, sort_order):
        entries = arxiv.query(search_query=search_query,id_list=[],max_results=max_results, start=start, sort_by=sort_by, sort_order=sort_order)
        return json2obj(json.dumps(entries))
    
    getPaper = Field(Paper, id=ID(required=True))

    def resolve_getPaper(self, info, id):
        entry = arxiv.query(id_list=[id])
        return json2obj(json.dumps(entry))[0]

my_schema = Schema(
    query=Query, types=[Paper, TitleDetail, ArxivPrimaryCategory, Tag, AuthorDetail]
)




















