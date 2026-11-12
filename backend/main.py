
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import API routers
from backend.routes.prediction import router as prediction_router
from backend.routes.customers import router as customers_router


# ==========================================
# 1. Create FastAPI Application
# ==========================================

app = FastAPI(
    title="Mobile App Business Intelligence API",
    description="Backend API for customer intelligence and purchase prediction",
    version="1.0.0"
)


# ==========================================
# 2. Configure CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# 3. Register Prediction API V1
# ==========================================

app.include_router(
    prediction_router,
    prefix="/api/v1",
    tags=["Prediction V1"]
)


# ==========================================
# 4. Register Customer API V1
# ==========================================

app.include_router(
    customers_router,
    prefix="/api/v1",
    tags=["Customers V1"]
)


# ==========================================
# 5. Home Endpoint
# ==========================================

@app.get("/")
def home():
    return {
        "message": "Mobile App Business Intelligence API is running!"
    }


# ==========================================
# 6. Health Check Endpoint
# ==========================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
