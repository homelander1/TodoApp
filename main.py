
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from models import Base
from database import engine
from routers import todos, auth, admin, users

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get('/healthy')
def health_check():
    return {'status':'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

