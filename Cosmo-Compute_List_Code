import numpy as np
import math

# Given values
psi = 0.1503378808
Re_tau = 1.4129651365
cos_psi_given = 0.9887205
sin_Re_tau_given = 0.98768834059
delta_phi_torque = 1.72113420759
a = 0.193218843731

print("=== JCR COSMOLOGICAL CLOCK - BRIDGE FUNCTION ===")
numerator = cos_psi_given * Re_tau
K = numerator / sin_Re_tau_given
k_norm = 1 / K
f = K * k_norm

print(f"cos(ψ) × Re(τ)     = {numerator:.8f}")
print(f"Core Kernel K       = {K:.8f}")
print(f"k_norm              = {k_norm:.8f}")
print(f"f(ψ,τ)              = {f:.10f}  ← EXACT")

print("\n=== IDENTITY VERIFICATION ===")
cos_psi_calc = np.cos(psi)
sin_delta = np.sin(delta_phi_torque)
print(f"cos(ψ) calculated   = {cos_psi_calc:.10f}")
print(f"sin(δφ_torque)      = {sin_delta:.10f}")
print(f"Identity holds:     {abs(cos_psi_calc - sin_delta) < 1e-10}")

print("\n=== ADDITIONAL RELATIONS ===")
print(f"2π / ψ              = {2*math.pi/psi:.8f}")
print(f"1 / ψ               = {1/psi:.8f}")
print(f"ψ × Re(τ)           = {psi*Re_tau:.8f}")
print(f"a × ψ               = {a*psi:.8f}")
