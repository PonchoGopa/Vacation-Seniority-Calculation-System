from fastapi import FastAPI
from app.database import engine
from app.database import Base

# Importar modelos para que SQLAlchemy los registre
from app.models import company, employee, vacation_policy, vacation_calculation
from app.api.company_routes import router as company_router

app = FastAPI()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(company_router)

@app.get("/")
def root():
    return {"message": "Vacation SaaS API running"}
