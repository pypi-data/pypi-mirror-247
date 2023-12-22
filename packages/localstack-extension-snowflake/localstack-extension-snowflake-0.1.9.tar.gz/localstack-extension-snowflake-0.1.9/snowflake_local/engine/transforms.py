_M='OBJECT_CONSTRUCT'
_L='javascript'
_K='expression'
_J='is_string'
_I='expressions'
_H='TABLE'
_G=False
_F='properties'
_E='postgres'
_D=True
_C=None
_B='kind'
_A='this'
import json,logging,re,textwrap
from typing import Callable
from localstack.utils.files import chmod_r,new_tmp_file,save_file
from localstack.utils.numbers import is_number
from sqlglot import exp,parse_one
from sqlglot.dialects import Snowflake
from snowflake_local.engine.db_engine import get_db_engine
from snowflake_local.engine.models import Query
from snowflake_local.engine.session import APP_STATE
LOG=logging.getLogger(__name__)
TYPE_MAPPINGS={'VARIANT':'JSONB','OBJECT':'JSONB','STRING':'TEXT','UNKNOWN':'TEXT'}
ACCOUNT_ID='TESTACC123'
class QueryTransforms:
	def apply(C,query):
		A=query;B=parse_one(A.query,read='snowflake')
		for D in C.get_transformers():B=B.transform(D,query=A)
		A.query=B.sql(dialect=_E);return A
	def get_transformers(A):return[remove_transient_keyword,remove_if_not_exists,remove_create_or_replace,replace_unknown_types,replace_unknown_user_config_params,replace_create_schema,replace_identifier_function,insert_create_table_placeholder,replace_json_field_access,replace_db_references,replace_current_warehouse,replace_current_account,update_function_language_identifier,convert_function_args_to_lowercase,create_tmp_table_for_result_scan]
class QueryTransformsPostgres(QueryTransforms):
	def get_transformers(A):return super().get_transformers()+[pg_replace_describe_table,pg_replace_show_schemas,pg_replace_show_objects,pg_replace_questionmark_placeholder,pg_replace_object_construct,pg_return_inserted_items,pg_remove_table_func_wrapper]
class QueryTransformsDuckDB(QueryTransforms):
	def get_transformers(A):return super().get_transformers()+[ddb_replace_create_database,pg_replace_show_schemas,pg_replace_show_objects]
def remove_transient_keyword(expression,**E):
	A=expression
	if not _is_create_table_expression(A):return A
	B=A.copy()
	if B.args[_F]:
		C=B.args[_F].expressions;D=exp.TransientProperty()
		if D in C:C.remove(D)
	return B
def remove_if_not_exists(expression,**D):
	C='exists';A=expression
	if not isinstance(A,exp.Create):return A
	B=A.copy()
	if B.args.get(C):B.args[C]=_G
	return B
def remove_create_or_replace(expression,**I):
	H='replace';B=expression
	if not isinstance(B,exp.Create):return B
	try:C=get_db_engine()
	except ImportError:C=_C
	A=B.copy()
	if A.args.get(H):
		A.args[H]=_G;D=A.args.get(_B)
		if C and D in(_H,'FUNCTION'):
			E=str(A.this.this);F=Query(query=f"DROP {D} IF EXISTS {E}");G=E.split('.')
			if len(G)>=3:F.database=G[0]
			C.execute_query(F)
	return A
def replace_unknown_types(expression,**E):
	B=expression
	for(D,C)in TYPE_MAPPINGS.items():
		C=getattr(exp.DataType.Type,C.upper());A=B
		if isinstance(A,exp.Alias):A=A.this
		if isinstance(A,exp.Cast)and A.to==exp.DataType.build(D):A.args['to']=exp.DataType.build(C)
		if isinstance(B,exp.ColumnDef):
			if B.args.get(_B)==exp.DataType.build(D):B.args[_B]=exp.DataType.build(C)
	return B
def replace_unknown_user_config_params(expression,**E):
	A=expression
	if isinstance(A,exp.Command)and str(A.this).upper()=='ALTER':
		C=str(A.expression).strip();D='\\s*USER\\s+\\w+\\s+SET\\s+\\w+\\s*=\\s*[\'\\"]?(.*?)[\'\\"]?\\s*$';B=re.match(D,C,flags=re.I)
		if B:return parse_one(f"SELECT '{B.group(1)}'")
	return A
def replace_create_schema(expression,query):
	A=expression
	if not isinstance(A,exp.Create):return A
	A=A.copy();B=A.args.get(_B)
	if str(B).upper()=='SCHEMA':query.database=A.this.db;A.this.args['db']=_C
	return A
def insert_create_table_placeholder(expression,query):
	A=expression
	if not _is_create_table_expression(A):return A
	if isinstance(A.this.this,exp.Placeholder)or str(A.this.this)=='?':A=A.copy();A.this.args[_A]=query.params.pop(0)
	return A
def replace_identifier_function(expression,**C):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()=='IDENTIFIER'and A.expressions:B=A.expressions[0].copy();B.args[_J]=_G;return B
	return A
def replace_json_field_access(expression,**J):
	B=expression
	if not B.parent_select:return B
	if B.find_ancestor(exp.From):return B
	if not isinstance(B,(exp.Dot,exp.Bracket)):return B
	F=_C;C=B;G=[]
	while hasattr(C,_A):
		if isinstance(C,(exp.Column,exp.Identifier)):F=C;break
		H=C.name or C.output_name;G.insert(0,H);C=C.this
	if not F:return B
	A=''
	for D in G:
		if is_number(D):A+=f"[{D}]"
		else:A+=f".{D}"
	A=A.strip('.')
	if not A.startswith('.'):A=f".{A}"
	if not A.startswith('$'):A=f"${A}"
	class I(exp.Binary,exp.Func):_sql_names=['get_path']
	E=I();E.args[_A]=C;E.args[_K]=f"'{A}'";return E
def replace_db_references(expression,query):
	E='catalog';C=query;A=expression;D=A.args.get(E)
	if isinstance(A,exp.Table)and A.args.get('db')and D:C.database=D.this;A.args[E]=_C
	if isinstance(A,exp.UserDefinedFunction):
		B=str(A.this).split('.')
		if len(B)==3:A.this.args[_A]=B[1];C.database=B[0]
	return A
def replace_current_warehouse(expression,query):
	C=query;A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()=='CURRENT_WAREHOUSE':B=exp.Literal();B.args[_A]=C.session and C.session.warehouse or'TEST';B.args[_J]=_D;return B
	return A
def replace_current_account(expression,**D):
	A=expression;C=['CURRENT_ACCOUNT','CURRENT_ACCOUNT_NAME']
	if isinstance(A,exp.Func)and str(A.this).upper()in C:B=exp.Literal();B.args[_A]=ACCOUNT_ID;B.args[_J]=_D;return B
	return A
def update_function_language_identifier(expression,**Q):
	L='python';A=expression;M={_L:'plv8',L:'plpython3u'}
	if isinstance(A,exp.Create)and isinstance(A.this,exp.UserDefinedFunction):
		E=A.args[_F];C=E.expressions;B=[A for A in C if isinstance(A,exp.LanguageProperty)]
		if not B:F=exp.LanguageProperty();F.args[_A]='SQL';C.append(F);return A
		G=str(B[0].this).lower();N=G==L
		for(O,H)in M.items():
			if G!=O:continue
			if isinstance(B[0].this,exp.Identifier):B[0].this.args[_A]=H
			else:B[0].args[_A]=H
		I=[];J=[A for A in C if str(A.this).lower()=='handler']
		for K in C:
			if isinstance(K,(exp.LanguageProperty,exp.ReturnsProperty)):I.append(K)
		E.args[_I]=I
		if N and J:P=J[0].args['value'].this;D=textwrap.dedent(A.expression.this);D=D+f"\nreturn {P}(*args)";A.expression.args[_A]=D
	return A
def convert_function_args_to_lowercase(expression,**H):
	A=expression
	if isinstance(A,exp.Create)and isinstance(A.this,exp.UserDefinedFunction):
		D=A.args[_F].expressions;B=[A for A in D if isinstance(A,exp.LanguageProperty)];B=str(B[0].this).lower()if B else _C
		if B not in(_L,'plv8'):return A
		E=[A for A in A.this.expressions if isinstance(A,exp.ColumnDef)]
		for F in E:
			if not A.expression:continue
			C=str(F.this);G=A.expression.this;A.expression.args[_A]=G.replace(C.upper(),C.lower())
	return A
def create_tmp_table_for_result_scan(expression,query):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()=='RESULT_SCAN':
		E=A.expressions[0];F=E.this;B=APP_STATE.queries.get(F)
		if not B:LOG.info("Unable to find state for query ID '%s'",F);return A
		C=new_tmp_file();G=json.dumps(B.result.rows);save_file(C,G);chmod_r(C,511);E.args[_A]=C
		def H(idx,col):B=col;A=B.type_name.upper();A=TYPE_MAPPINGS.get(A)or A;return f"{f'_col{idx+1}'if B.name=='?column?'else B.name} {A}"
		D=exp.Alias();D.args[_A]=A;I=B.result.columns;J=', '.join([H(A,B)for(A,B)in enumerate(I)]);D.args['alias']=f"({J})";return D
	return A
def pg_replace_describe_table(expression,**G):
	A=expression
	if not isinstance(A,exp.Describe):return A
	C=A.args.get(_B)
	if str(C).upper()==_H:B=A.this.name;D=f"'{B}'"if B else'?';E=f"SELECT * FROM information_schema.columns WHERE table_name={D}";F=parse_one(E,read=_E);return F
	return A
def pg_replace_show_schemas(expression,**F):
	A=expression
	if not isinstance(A,exp.Command):return A
	C=str(A.this).upper();B=str(A.args.get(_K)).strip().lower();B=B.removeprefix('terse').strip()
	if C=='SHOW'and B.startswith('schemas'):D='SELECT * FROM information_schema.schemata';E=parse_one(D,read=_E);return E
	return A
def pg_replace_show_objects(expression,**H):
	A=expression
	if not isinstance(A,exp.Command):return A
	E=str(A.this).upper();B=str(A.args.get(_K)).strip().lower();B=B.removeprefix('terse').strip()
	if E=='SHOW'and B.startswith('objects'):
		C='SELECT * FROM information_schema.tables';F='^\\s*objects\\s+(\\S+)\\.(\\S+)(.*)';D=re.match(F,B)
		if D:C+=f" WHERE table_schema = '{D.group(2)}'"
		G=parse_one(C,read=_E);return G
	return A
def pg_replace_questionmark_placeholder(expression,**B):
	A=expression
	if isinstance(A,exp.Placeholder):return exp.Literal(this='%s',is_string=_G)
	return A
def pg_replace_object_construct(expression,**G):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()==_M:
		class D(exp.Func):_sql_names=['TO_JSON_STR'];arg_types={_A:_D,_I:_D}
		B=A.args[_I]
		for C in range(1,len(B),2):E=B[C];B[C]=F=D();F.args[_I]=E
	return A
def pg_return_inserted_items(expression,**B):
	A=expression
	if isinstance(A,exp.Insert):A.args['returning']=' RETURNING 1'
	return A
def pg_remove_table_func_wrapper(expression,**B):
	A=expression
	if isinstance(A,exp.Table)and str(A.this.this).upper()==_H:return A.this.expressions[0]
	return A
def ddb_replace_create_database(expression,**D):
	A=expression
	if isinstance(A,exp.Create)and str(A.args.get(_B)).upper()=='DATABASE':assert(C:=A.find(exp.Identifier)),f"No identifier in {A.sql}";B=C.this;return exp.Command(this='ATTACH',expression=exp.Literal(this=f"DATABASE ':memory:' AS {B}",is_string=_D),create_db_name=B)
	return A
def _is_create_table_expression(expression,**C):A=expression;return isinstance(A,exp.Create)and(B:=A.args.get(_B))and isinstance(B,str)and B.upper()==_H
def _patch_sqlglot():Snowflake.Parser.FUNCTIONS.pop(_M,_C)
_patch_sqlglot()