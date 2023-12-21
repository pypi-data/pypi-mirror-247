_I='sqlText'
_H='name'
_G='test'
_F=None
_E='status_code'
_D='data'
_C='POST'
_B='success'
_A=True
import gzip,json,logging
from localstack.aws.connect import connect_to
from localstack.http import Request,Response
from localstack.http import route as _route
from localstack.utils.strings import short_uid,to_str
from snowflake_local import config
from snowflake_local.constants import PATH_QUERIES,PATH_SESSION,PATH_V1_STREAMING
from snowflake_local.engine.models import Session
from snowflake_local.engine.queries import handle_query_request,insert_rows_into_table
from snowflake_local.engine.session import APP_STATE,lookup_request_session
from snowflake_local.files.staging import get_stage_s3_location
from snowflake_local.files.storage import FileRef
from snowflake_local.utils.encodings import get_parquet_from_blob
LOG=logging.getLogger(__name__)
TMP_UPLOAD_STAGE='@tmp-stage-internal'
ENCRYPTION_KEY=_G
def route(*A,**B):
	def C(fn):
		def C(handler,request,*F,**G):
			B=request;A=fn(handler,B,*F,**G)
			if not config.TRACE_LOG:return A
			C=_get_data(B)
			if isinstance(C,dict):C=json.dumps(C)
			E=_F;D=str(A)
			if isinstance(A,Response):
				E=A.status_code;D=A.data
				try:D=to_str(D)
				except Exception:pass
			LOG.debug('REQ: %s %s %s -- RES: %s %s',B.method,B.path,C,E,D);return A
		return _route(*A,**B)(C)
	return C
class RequestHandler:
	@route(PATH_SESSION,methods=[_C])
	def session_request(self,request,**D):
		B=request
		if B.args.get('delete')=='true':
			A=lookup_request_session(B)
			if A:LOG.debug('Deleting state for session %s...',A.session_id);APP_STATE.sessions.pop(A.session_id,_F)
		C={_B:_A};return Response.for_json(C,status=200)
	@route(f"{PATH_SESSION}/v1/login-request",methods=[_C])
	def session_login(self,request,**D):A=short_uid();B=short_uid();C={_D:{'nextAction':_F,'sessionId':f"'{A}'",'token':B,'masterToken':'masterToken123','parameters':[{_H:'AUTOCOMMIT','value':_A}]},_B:_A};APP_STATE.sessions[A]=Session(session_id=A,auth_token=B);return Response.for_json(C,status=200)
	@route(f"{PATH_QUERIES}/query-request",methods=[_C])
	def start_query(self,request,**J):
		B=request;C=_get_data(B);F=C.get(_I,'');G=C.get('bindings')or{};H=lookup_request_session(B);D=[]
		for I in range(1,100):
			E=G.get(str(I))
			if not E:break
			D.append(E.get('value'))
		A=handle_query_request(F,D,H);A=A.to_dict();return Response.for_json(A,status=200)
	@route(f"{PATH_QUERIES}/abort-request",methods=[_C])
	def abort_query(self,request,**A):return{_B:_A}
	@route(f"{PATH_V1_STREAMING}/client/configure",methods=[_C])
	def streaming_configure_client(self,request,**D):A=FileRef.parse(TMP_UPLOAD_STAGE);B=get_stage_s3_location(A);C={_B:_A,_E:0,'prefix':_G,'deployment_id':_G,'stage_location':B,_D:{}};return C
	@route(f"{PATH_V1_STREAMING}/channels/open",methods=[_C])
	def streaming_open_channel(self,request,**I):G='VARIANT';F='BINARY';E='variant';D='logical_type';C='physical_type';B='type';H=_get_data(request);A={_B:_A,_E:0,'client_sequencer':1,'row_sequencer':1,'encryption_key':ENCRYPTION_KEY,'encryption_key_id':123,'table_columns':[{_H:'record_metadata',B:E,C:F,D:G},{_H:'record_content',B:E,C:F,D:G}],_D:{}};A.update(H);return A
	@route(f"{PATH_V1_STREAMING}/channels/status",methods=[_C])
	def streaming_channel_status(self,request,**B):A={_B:_A,_E:0,'message':'test channel','channels':[{_E:0,'persisted_row_sequencer':1,'persisted_client_sequencer':1,'persisted_offset_token':_F}]};return A
	@route(f"{PATH_V1_STREAMING}/channels/write/blobs",methods=[_C])
	def streaming_channel_write_blobs(self,request,**T):
		H='blobs';D='/';I=_get_data(request);J=FileRef.parse(TMP_UPLOAD_STAGE);K=get_stage_s3_location(J)['location'];E=[]
		for A in I.get(H,[]):
			B=A.get('path')or D;L=B if B.startswith(D)else f"/{B}";M=K+L;N,U,O=M.partition(D);P=connect_to().s3;C=P.get_object(Bucket=N,Key=O);Q=C['Body'].read()
			try:R=get_parquet_from_blob(Q,key=ENCRYPTION_KEY,blob_path=B)
			except Exception as S:LOG.warning('Unable to parse parquet from blob: %s - %s',A,S);continue
			F=A.get('chunks')or[]
			if not F:LOG.info('Chunks information missing in incoming blob: %s',A)
			for G in F:insert_rows_into_table(table=G['table'],database=G['database'],rows=R)
			E.append({})
		C={_B:_A,_E:0,H:E};return C
	@route('/telemetry/send/sessionless',methods=[_C])
	def send_telemetry_sessionless(self,request,**B):A={_B:_A,_D:{}};return A
	@route('/monitoring/queries/<query_id>',methods=['GET'])
	def get_monitoring_query_info(self,request,query_id,**D):
		B=[];C={_B:_A,_D:{'queries':B}};A=APP_STATE.queries.get(query_id)
		if A:B.append({'id':A.query.query_id,'status':'SUCCESS','state':'SUCCEEDED',_I:A.query.original_query})
		return C
def _get_data(request):
	A=request.data
	if isinstance(A,bytes):
		try:A=gzip.decompress(A)
		except gzip.BadGzipFile:pass
		A=json.loads(to_str(A))
	return A