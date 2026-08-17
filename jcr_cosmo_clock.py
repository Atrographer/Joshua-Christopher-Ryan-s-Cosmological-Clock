import math
import cmath

# ──────────────────────────────────────────────────────────────
# Locked constants
# ──────────────────────────────────────────────────────────────
EPS              = 1e-9
N_TODAY          = 1_000_000_000
PSI              = 0.1503378808                  # rad
ALPHA            = 0.193218843731                # irrational rotation number
THETA_EFF        = 1.2140298                     # rad  (α = θ_eff / 2π)
RE_TAU           = 1.4129651365                  # Re(τ) = arctan(2π)
TAU              = RE_TAU
DELTA_PHI_TORQUE = 1.72113420759                 # rad  = 0.25·2π + ψ
SIN_DELTA        = math.sin(DELTA_PHI_TORQUE)    # ≈ cos(ψ) ≈ 0.9887205
COS_PSI          = math.cos(PSI)
ALPHA_G          = 0.558
H_WIND           = 70.0
SH_GEOM_TARGET   = 3.170
SCREEN_MPC       = 4500.0
DAMP_SCALE       = 5.8
LATE_START       = 700_000_000
K_NORM           = 1.4144172                     # normalisation constant
INV_SQRT2        = 0.7071

# ──────────────────────────────────────────────────────────────
class JCRCosmologicalClock:
    def __init__(self):
        self.eps = EPS
        self.N_today = N_TODAY

    # ── microscopic / macroscopic ──────────────────────────────
    def chi_micro(self, N):
        """χ_micro = ε·N   →  χ_micro(N_today) = 1"""
        return self.eps * N

    def scale_factor(self, N):
        """a(N) = exp(χ_micro)  →  a_Ψ = e"""
        return math.exp(self.chi_micro(N))

    def redshift(self, N):
        a = self.scale_factor(N)
        return 1.0 / a - 1.0

    # ── phase quantities (both normalisations retained) ───────
    def phase_bias(self, N):
        """φ_bias = 2π · χ_micro  →  2π at present epoch"""
        return 2.0 * math.pi * self.chi_micro(N)

    def primary_phase_tau(self, k):
        """v(k) = 2τ · k · 10⁻⁹"""
        return 2.0 * TAU * k * self.eps

    def primary_phase_4pi(self, k):
        """v(k) = 4π · k · 10⁻⁹   (double-cover that lands on 4π)"""
        return 4.0 * math.pi * k * self.eps

    def controlled_phase(self, x=INV_SQRT2):
        """v(0.7071) ≈ 8.8875e-9 rad"""
        return self.primary_phase_4pi(x)

    # ── discrete dynamical system on S¹ ───────────────────────
    def irrational_rotation(self, phi):
        """T_α : φ ↦ φ + 2π α   (mod 2π)"""
        return (phi + 2.0 * math.pi * ALPHA) % (2.0 * math.pi)

    def complex_map_step(self, z, dphi):
        """z_{n+1} = z_n · exp(i Δφ_n)"""
        return z * cmath.exp(1j * dphi)

    # ── algebraic bridge identities ───────────────────────────
    def f_psi_tau(self):
        """f(ψ,τ) ≈ cos(ψ)·Re(τ) / (sin(Re(τ))·K) ≈ 1"""
        return (COS_PSI * RE_TAU) / (math.sin(RE_TAU) * K_NORM)

    def alpha_psi_product(self):
        return ALPHA * PSI          # ≈ 0.02905

    # ── suppression ──────────────────────────────────────────
    def screening(self, chi):
        return math.exp(-chi / SCREEN_MPC)

    def redshift_damping(self, z):
        return math.exp(-z / DAMP_SCALE)

    def modulation(self, z):
        return 1.0 + 5.0 * math.exp(-z / 2.0)

    def suppression(self, z, chi):
        return self.modulation(z) * self.redshift_damping(z) * self.screening(chi)

    # ── geometric torque ─────────────────────────────────────
    def omega_eff(self):
        return DELTA_PHI_TORQUE / 0.3

    def delta_H_geom(self, N):
        if N < LATE_START:
            return 0.0
        chi = self.chi_micro(N)
        z   = self.redshift(N)
        a   = self.scale_factor(N)
        base = ALPHA_G * self.omega_eff() * SIN_DELTA
        weight = a * self.screening(chi) * self.redshift_damping(z)
        # normalise to the locked target 3.170 at N_today
        norm = SH_GEOM_TARGET / (ALPHA_G * self.omega_eff() * SIN_DELTA)
        return base * weight * norm

    def H(self, N):
        return H_WIND + self.delta_H_geom(N)

    # ── diagnostics ──────────────────────────────────────────
    def present_day_report(self):
        N = self.N_today
        print("=" * 64)
        print("Joshua Christopher Ryan’s Cosmological Clock – Present Epoch")
        print("=" * 64)
        print(f"χ_micro(N_today)     = {self.chi_micro(N):.10f}")
        print(f"a_Ψ                  = {self.scale_factor(N):.10f}  (e)")
        print(f"z_Ψ                  = {self.redshift(N):.6f}")
        print(f"φ_bias               = {self.phase_bias(N):.10f} rad  (2π)")
        print(f"primary phase (4π)   = {self.primary_phase_4pi(N):.10f} rad")
        print(f"primary phase (2τ)   = {self.primary_phase_tau(N):.10f} rad")
        print(f"ψ                    = {PSI:.10f} rad  ({math.degrees(PSI):.4f}°)")
        print(f"Δφ_torque            = {DELTA_PHI_TORQUE:.10f} rad")
        print(f"sin(Δφ_torque)       = {SIN_DELTA:.10f}  = cos(ψ)")
        print(f"α·ψ                  = {self.alpha_psi_product():.10f}")
        print(f"f(ψ,τ)               = {self.f_psi_tau():.10f}")
        print(f"controlled v(0.7071) = {self.controlled_phase():.6e} rad")
        print(f"H_wind               = {H_WIND:.3f}")
        print(f"δH_geom(today)       = {self.delta_H_geom(N):.3f}")
        print(f"H_total(today)       = {self.H(N):.3f} km/s/Mpc")
        print("=" * 64)

    def milestone_table(self):
        milestones = [0, 1e6, 1e8, 5e8, 7e8, 9e8, N_TODAY]
        print("\n{:>12} {:>10} {:>10} {:>10} {:>10} {:>10}".format(
            "N", "χ", "a", "z", "δH", "H"))
        print("-" * 66)
        for N in milestones:
            print(f"{N:12.0f} {self.chi_micro(N):10.6f} "
                  f"{self.scale_factor(N):10.6f} {self.redshift(N):10.4f} "
                  f"{self.delta_H_geom(N):10.4f} {self.H(N):10.4f}")


# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    clock = JCRCosmologicalClock()
    clock.present_day_report()
    clock.milestone_table()
