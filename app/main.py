from fastapi import FastAPI
from app.api.company_routes import router as company_router
from app.api.employee_routes import router as employee_router
from app.api.vacation_policy_routes import router as policy_router
from app.api.vacation_request_routes import router as vacation_request_router

# Importar todos los modelos para que SQLAlchemy los registre correctamente
from app.models import company, employee, vacation_policy, vacation_policy_rule, vacation_request, vacation_calculation

app = FastAPI()

app.include_router(company_router)
app.include_router(employee_router)
app.include_router(policy_router)
app.include_router(vacation_request_router)

@app.get("/")
def root():
    return {"message": "Vacation SaaS API running"}