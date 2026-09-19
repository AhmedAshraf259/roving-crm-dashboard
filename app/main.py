from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, bookings, customers, dashboard, leads, payments, tasks

# إنشاء الجداول في قاعدة البيانات
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Roving Travel CRM API",
    description="Backend API for Roving Travel CRM",
    version="1.0.0"
)

# تسجيل الـ Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(leads.router, prefix="/leads", tags=["Leads"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

# الـ Endpoint الرئيسي
@app.get("/")
def read_root():
    return {"status": "online", "message": "Roving CRM Backend is running successfully"}