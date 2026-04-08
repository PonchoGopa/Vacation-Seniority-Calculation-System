from fastapi import FastAPI
from app.api.company_routes import router as company_router
from app.api.employee_routes import router as employee_router
from app.api.vacation_policy_routes import router as policy_router

app = FastAPI()

app.include_router(company_router)
app.include_router(employee_router)
app.include_router(policy_router)

@app.get("/")
def root():
    return {"message": "Vacation SaaS API running"}