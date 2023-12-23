_N='already exists'
_M='status'
_L='schema_name'
_K='text'
_J='FUNCTION'
_I='nullable'
_H='scale'
_G='precision'
_F='length'
_E='TABLE'
_D='kind'
_C='type'
_B=True
_A='name'
import re
from abc import ABC,abstractmethod
from localstack.utils.objects import get_all_subclasses
from sqlglot import exp,parse_one
from snowflake_local.engine.models import Query
from snowflake_local.server.conversions import to_pyarrow_table_bytes_b64
from snowflake_local.server.models import QueryResponse
class QueryResultPostprocessor(ABC):
	def should_apply(A,query,result):return _B
	@abstractmethod
	def apply(self,query,result):0
class FixShowSchemasResult(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(re.match('^\\s*SHOW\\s+.*SCHEMAS',query.original_query,flags=re.I))
	def apply(A,query,result):_replace_dict_value(result.data.rowtype,_A,_L,_A)
class FixShowObjectsResult(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(re.match('^\\s*SHOW\\s+.*OBJECTS',query.original_query,flags=re.I))
	def apply(B,query,result):A=result;_replace_dict_value(A.data.rowtype,_A,'table_schema',_L);_replace_dict_value(A.data.rowtype,_A,'table_name',_A);_replace_dict_value(A.data.rowtype,_A,'table_type',_D);_replace_dict_value(A.data.rowtype,_A,'table_catalog','database_name')
class FixCreateEntityResult(QueryResultPostprocessor):
	def should_apply(A,query,result):B=A._get_created_entity_type(query.original_query);return B in(_E,_J)
	def apply(E,query,result):
		D=result;B=query;C=E._get_created_entity_type(B.original_query);F={_E:'Table',_J:'Function'};G=F.get(C)
		if C==_E:A=_get_table_from_creation_query(B.original_query);A=A and A.upper()
		elif C==_J:H=_parse_snowflake_query(B.original_query);I=H.this;A=str(I.this).upper()
		else:A='test'
		D.data.rowset.append([f"{G} {A} successfully created."]);D.data.rowtype.append({_A:_M,_C:_K,_F:-1,_G:0,_H:0,_I:_B})
	def _get_created_entity_type(B,query):
		A=_parse_snowflake_query(query)
		if isinstance(A,exp.Create):return A.args.get(_D)
class FixDropTableResult(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(_get_table_from_drop_query(query.original_query))
	def apply(C,query,result):A=result;B=_get_table_from_drop_query(query.original_query);A.data.rowset.append([f"{B} successfully dropped."]);A.data.rowtype.append({_A:_M,_C:_K,_F:-1,_G:0,_H:0,_I:_B})
class FixAlreadyExistsErrorResponse(QueryResultPostprocessor):
	def should_apply(B,query,result):A=result;return not A.success and _N in(A.message or'')
	def apply(C,query,result):
		A=result
		def B(match):return f"SQL compilation error:\nObject '{match.group(1).upper()}' already exists."
		A.message=re.sub('.*database \\"(\\S+)\\".+',B,A.message);A.message=re.sub('.*relation \\"(\\S+)\\".+',B,A.message);A.message=re.sub('.*function \\"(\\S+)\\".+',B,A.message)
class FixInsertQueryResult(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(re.match('^\\s*INSERT\\s+.+',query.original_query,flags=re.I))
	def apply(B,query,result):A=result;A.data.rowset=[[len(A.data.rowset)]];A.data.rowtype=[{_A:'count',_C:'integer',_F:-1,_G:0,_H:0,_I:_B}]
class UpdateSessionAfterCreatingDatabase(QueryResultPostprocessor):
	REGEX=re.compile('^\\s*CREATE.*\\s+DATABASE(\\s+IF\\s+NOT\\s+EXISTS)?\\s+(\\S+)',flags=re.I)
	def should_apply(A,query,result):return bool(A.REGEX.match(query.original_query))
	def apply(B,query,result):A=query;C=B.REGEX.match(A.original_query);A.session.database=C.group(2);A.session.schema=None
class UpdateSessionAfterCreatingSchema(QueryResultPostprocessor):
	REGEX=re.compile('^\\s*CREATE.*\\s+SCHEMA(\\s+IF\\s+NOT\\s+EXISTS)?\\s+(\\S+)',flags=re.I)
	def should_apply(A,query,result):return bool(A.REGEX.match(query.original_query))
	def apply(B,query,result):A=query;C=B.REGEX.match(A.original_query);A.session.schema=C.group(2)
class AdjustQueryResultFormat(QueryResultPostprocessor):
	def apply(C,query,result):
		A=result;B=re.match('.+FROM\\s+@',query.original_query,flags=re.I);A.data.queryResultFormat='arrow'if B else'json'
		if B:A.data.rowsetBase64=to_pyarrow_table_bytes_b64(A);A.data.rowset=[];A.data.rowtype=[]
class AdjustColumnTypes(QueryResultPostprocessor):
	TYPE_MAPPINGS={'UNKNOWN':'TEXT','VARCHAR':'TEXT'}
	def apply(C,query,result):
		for A in result.data.rowtype:
			D=A.get(_C,'');B=C.TYPE_MAPPINGS.get(D)
			if B:A[_C]=B
class ReturnDescribeTableError(QueryResultPostprocessor):
	def apply(C,query,result):
		A=result;B=re.match('desc(?:ribe)?\\s+.+',query.original_query,flags=re.I)
		if B and not A.data.rowset:A.success=False
class IgnoreErrorForExistingEntity(QueryResultPostprocessor):
	REGEX=re.compile('^\\s*CREATE.*\\s+(\\S+)(\\s+IF\\s+NOT\\s+EXISTS)\\s+(\\S+)',flags=re.I)
	def should_apply(A,query,result):return bool(A.REGEX.match(query.original_query))
	def apply(B,query,result):
		A=result
		if not A.success and _N in(A.message or''):A.success=_B;A.data.rowtype=[];A.data.rowset=[]
class AddDefaultResultIfEmpty(QueryResultPostprocessor):
	def should_apply(B,query,result):
		A=_parse_snowflake_query(query.original_query)
		if isinstance(A,exp.AlterTable):return _B
		return isinstance(A,exp.Command)and str(A.this).upper()=='ALTER'
	def apply(B,query,result):
		A=result
		if not A.data.rowtype:A.data.rowtype=[{_A:'?column?',_C:_K,_F:-1,_G:0,_H:0,_I:_B}]
		A.data.rowset=[('Statement executed successfully.',)]
def apply_post_processors(query,result):
	B=result;A=query
	for D in get_all_subclasses(QueryResultPostprocessor):
		C=D()
		if C.should_apply(A,result=B):C.apply(A,result=B)
def _replace_dict_value(values,attr_key,attr_value,attr_value_replace):
	A=attr_key;B=[B for B in values if B[A]==attr_value]
	if B:B[0][A]=attr_value_replace
def _get_table_from_creation_query(query):
	A=_parse_snowflake_query(query)
	if not isinstance(A,exp.Create)or A.args.get(_D)!=_E:return
	B=A.this;C=B.this;D=C.this;E=D.this;return E
def _get_table_from_drop_query(query):
	A=_parse_snowflake_query(query)
	if not isinstance(A,exp.Drop)or A.args.get(_D)!=_E:return
	B=A.this;C=B.this;D=C.this;return D
def _get_database_from_drop_query(query):
	A=_parse_snowflake_query(query)
	if not isinstance(A,exp.Drop)or A.args.get(_D)!='DATABASE':return
	B=A.this;C=B.this;D=C.this;return D
def _parse_snowflake_query(query):
	try:return parse_one(query,read='snowflake')
	except Exception:return