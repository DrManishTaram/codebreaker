import nest_asyncio
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

# Qiskit imports
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import Sampler

# Patch event loop (important for Jupyter/Colab environments)
nest_asyncio.apply()

# --- FastAPI app ---
app = FastAPI(title="Codebreaker API", version="1.0")

# Request model.
class DecryptRequest(BaseModel):
    ciphertext: int
    key: int

# Response model
class DecryptResponse(BaseModel):
    ciphertext: int
    key: int
    plaintext: int
    quantum_result: Dict[str, float]

@app.get("/")
def home():
    return {
        "message": "--Codebreaker-- 10-bit Encryption/Decryption with Qiskit Demonstration"
    }

@app.post("/decrypt", response_model=DecryptResponse)
def decrypt(req: DecryptRequest):
    """
    Decrypt ciphertext using 10-bit key and
    also run a simple Qiskit quantum circuit for demonstration.
    """

    # --- Classical decryption (10-bit space: 0–1023) ---
    plaintext = (req.ciphertext - req.key) % 1024

    # --- Quantum demonstration (Hadamard + measurement) ---
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    # Run on AerSimulator with Sampler primitive
    simulator = AerSimulator()
    sampler = Sampler()
    result = sampler.run([qc]).result()

    # Convert keys to string for JSON safety
    quantum_result = {str(k): float(v) for k, v in result.quasi_dists[0].items()}

    return DecryptResponse(
        ciphertext=req.ciphertext,
        key=req.key,
        plaintext=plaintext,
        quantum_result=quantum_result
    )


