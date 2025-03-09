from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from mangum import Mangum
from ticket import generate_delegate_ticket

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/api/{service}/generate-ticket")
async def generate_ticket(
    first_name: str,
    last_name: str,
    service: str = Path(..., description="The service to generate ticket for (I just have 'nexlds-ife' and 'ysf-2022' for now)")
):
    
    doc_io, file_name = generate_delegate_ticket(service, first_name, last_name)
    headers = {
        "Content-Disposition": f"inline; filename={file_name}",
        "Content-Type": "image/png"
    }
    return StreamingResponse(
        doc_io,
        headers=headers,
        media_type="image/png"
    )

# AWS Lambda handler
lambda_handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)