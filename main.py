import uvicorn

from apps.core.bootstraps.http import bootstrap_fastapi
from apps.core.config import settings
from apps.core.router import router


app = bootstrap_fastapi(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT)
