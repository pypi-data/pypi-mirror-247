from localstack.extensions.api import Extension
from localstack.extensions.api.http import RouteHandler,Router
class SnowflakeExtension(Extension):
	name='snowflake'
	def update_gateway_routes(B,router):from snowflake_local.server.routes import RequestHandler as A;router.add(A())