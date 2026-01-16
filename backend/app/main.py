from fastapi import FastAPI,status

app = FastAPI(
    title = "Rail Reservation System",
    description="Backend for Indian Railway Style Booking System",
    version ="1.0.0"
)

@app.get("/")
def health_check():
    return {"ststus":status.HTTP_200_OK, "message":"Train Reservation backend is Running"}