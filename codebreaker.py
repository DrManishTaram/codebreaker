
import nest_asyncio
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# Qiskit imports
from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler

# Patch event loop for Colab
nest_asyncio.apply()

# --- FastAPI app ---
app = FastAPI()

# Request model
class DecryptRequest(BaseModel):
    ciphertext: str

@app.get("/")
def home():
    return {"message": "🚀 Quantum API is running!"}

@app.post("/decrypt")
def decrypt(req: DecryptRequest):
    """
    Example quantum step (not real decryption).
    Runs a Hadamard + measurement to simulate "quantum randomness".
    """
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    sampler = Sampler()
    result = sampler.run(qc).result()

    return {
        "ciphertext": req.ciphertext,
        "quantum_result": result.quasi_dists[0]
    }


