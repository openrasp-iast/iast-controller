from ninja import NinjaAPI

from controller.api import router as controller_router
from agent.api import router as agent_router
from iast.api import router as iast_router

api = NinjaAPI()

api.add_router("/", controller_router)
api.add_router("/agent", agent_router)
api.add_router("/iast", iast_router)
