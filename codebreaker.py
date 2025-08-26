import nest_asyncio
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# Qiskit imports
from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler

# Patch event loop
nest_asyncio.apply()

# --- FastAPI app ---
app = FastAPI()

# Request model
class DecryptRequest(BaseModel):
    ciphertext: int
    key: int

@app.get("/")
def home():
    return {
        "message": "--Codebreaker-- 10-bit Encryption/Decryption with Qiskit Demonstration"
    }

@app.post("/decrypt")
def decrypt(req: DecryptRequest):
    """
    Decrypt ciphertext using 10-bit key and
    also run a simple Qiskit quantum circuit for demonstration.
    """
    # --- Classical decryption ---
    plaintext = (req.ciphertext - req.key) % 1024

    # --- Quantum demonstration (Hadamard + measurement) ---
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    sampler = Sampler()
    result = sampler.run(qc).result()
    quantum_result = result.quasi_dists[0]

    return {
        "ciphertext": req.ciphertext,
        "key": req.key,
        "plaintext": plaintext,
        "quantum_result": quantum_result
    }

