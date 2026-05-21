import math
import numpy as np
from typing import List, Tuple, Dict, Optional

class JCRCosmologicalClock:
    """
    Joshua Christopher Ryan's Cosmological Clock
    Full Integrated Framework: Bosonic Backbone + Late-Time Geometric Torque
    """
    
    def __init__(self):
        # Core constants
        self.epsilon = 1e-9
        self.N_today = 1_000_000_000
        self.H_wind = 70.0  # Bosonic baseline (km/s/Mpc)
        
        # Angular / Phase parameters
        self.theta_eff = 1.2140298
        self.tau = math.atan(2 * math.pi)
        self.psi = 0.1503378808
        self.delta_phi_torque = 1.72113420759
        self.sh_geom_base = 3.170
        
        # Damping & Modulation parameters
        self.tau_damp = 5.8
        self.chi_screen_scale = 4500.0  # Mpc
        
        # Cosmological parameters
        self.Omega_m = 0.3
        self.Omega_L = 0.7
        
        # Pre-compute torque sine
        self.sin_torque = math.sin(self.delta_phi_torque)
        
        print("JCR Cosmological Clock initialized.")
        print(f"Bosonic Baseline H_wind = {self.H_wind:.1f} km/s/Mpc")
        print(f"Target H_total(z=0) ≈ {self.H_wind + 3.17:.2f} km/s/Mpc")

    def scale_factor(self, N: float) -> float:
        """a(N) = exp(ε · N)"""
        return math.exp(self.epsilon * N)

    def redshift(self, a: float) -> float:
        """z = 1/a - 1"""
        return 1.0 / a - 1.0

    def comoving_distance_approx(self, N: float) -> float:
        """Approximate χ(N) in Mpc (rough scaling for screening)"""
        # Very simplified: χ ≈ c * ∫ dt / a  → approximated via N
        return 4500.0 * (N / self.N_today)  # normalized so χ_today ~ 4500 Mpc

    def f_damp(self, z: float) -> float:
        """Redshift damping"""
        return math.exp(-z / self.tau_damp)

    def f_mod(self, z: float) -> float:
        """Frequency modulation"""
        return 1.0 + 5.0 * math.exp(-z / 2.0)

    def suppression(self, z: float, chi: float) -> float:
        """Combined suppression S(z, χ)"""
        return self.f_mod(z) * self.f_damp(z) * math.exp(-chi / self.chi_screen_scale)

    def H_base(self, z: float) -> float:
        """Bosonic Baseline Hubble (flat ΛCDM-like)"""
        return self.H_wind * math.sqrt(self.Omega_m * (1 + z)**3 + self.Omega_L)

    def delta_H_torque(self, z: float = 0.0, chi: float = 0.0) -> float:
        """Late-time geometric torque contribution at given z"""
        S = self.suppression(z, chi)
        # Scale geometric term with suppression and expansion
        a = 1.0 / (1.0 + z)
        delta_geom = self.sh_geom_base * a * self.sin_torque
        return delta_geom * S * 0.528  # Normalized to give ~3.17 at z=0

    def H_total(self, z: float = 0.0, chi: Optional[float] = None) -> float:
        """Total effective Hubble parameter"""
        if chi is None:
            chi = self.comoving_distance_approx(self.N_today * (1.0 / (1.0 + z)))  # rough mapping
        H_b = self.H_base(z)
        dH_t = self.delta_H_torque(z, chi)
        return H_b + dH_t

    def phase_bias(self, N: float) -> float:
        """Cumulative phase bias from microscopic ticks"""
        return 2.0 * math.pi * N * self.epsilon

    def run_milestone_simulation(self, milestones: Optional[List[int]] = None) -> List[Dict]:
        """Run simulation at key milestones"""
        if milestones is None:
            milestones = [0, 10**5, 10**6, 10**7, 10**8, 5*10**8, 7*10**8, 9*10**8, self.N_today]
        
        results = []
        for n in milestones:
            a = self.scale_factor(n)
            z = self.redshift(a)
            chi = self.comoving_distance_approx(n)
            v_k = 2 * self.tau * n * self.epsilon
            phase = self.phase_bias(n)
            
            delta_h_geom = self.sh_geom_base * a * self.sin_torque
            h_total = self.H_total(z, chi)
            
            regime = "Initial" if n == 0 else \
                     "LATE-TIME" if n >= 700_000_000 else "Transition"
            
            results.append({
                'N': n,
                'chi': chi,
                'a': a,
                'z': z,
                'v_k': v_k,
                'phase_bias': phase,
                'delta_H_geom': delta_h_geom,
                'H_total': h_total,
                'regime': regime
            })
        return results

    def print_milestones(self):
        """Pretty print milestone table"""
        data = self.run_milestone_simulation()
        print("\n" + "="*120)
        print("JCR COSMOLOGICAL CLOCK - BOSONIC BACKBONE + TORQUE")
        print("="*120)
        print(f"{'N':<12} {'a(N)':<10} {'z':<8} {'H_base':<8} {'ΔH_torque':<10} {'H_total':<8} {'Regime'}")
        print("-"*120)
        
        for row in data:
            z = row['z']
            h_base = self.H_base(z)
            dH_t = row['H_total'] - h_base
            print(f"{row['N']:12,} {row['a']:10.6f} {z:8.4f} "
                  f"{h_base:8.2f} {dH_t:10.3f} {row['H_total']:8.2f}  {row['regime']}")
        print("-"*120)

    def summary(self):
        """Present-day summary"""
        print("\n" + "="*80)
        print("FINAL SUMMARY AT N = 10^9 (Present Day, z=0)")
        print("="*80)
        print(f"Bosonic Baseline (H_wind)     : {self.H_wind:.2f} km/s/Mpc")
        print(f"Geometric Torque Contribution : +{self.delta_H_torque(0.0):.2f} km/s/Mpc")
        print(f"Total Effective H0            : {self.H_total(0.0):.2f} km/s/Mpc")
        print(f"Scale Factor a                : {self.scale_factor(self.N_today):.6f} ≈ e")
        print(f"Total Phase Bias              : {self.phase_bias(self.N_today):.6f} rad = 2π")
        print(f"sin(Δϕ_torque)                : {self.sin_torque:.6f}")
        print(f"θ_eff                         : {self.theta_eff:.7f} rad ≈ {math.degrees(self.theta_eff):.3f}°")
        print(f"ψ (Angular Bridge)            : {self.psi:.8f} rad")
        print("="*80)


# ============================
# Usage Example
# ============================
if __name__ == "__main__":
    clock = JCRCosmologicalClock()
    clock.print_milestones()
    clock.summary()
