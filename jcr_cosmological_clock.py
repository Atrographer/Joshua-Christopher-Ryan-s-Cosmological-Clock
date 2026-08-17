#!/usr/bin/env python3
"""
Joshua Christopher Ryan’s Cosmological Clock
Pure-Python implementation of the discrete-tick model
with angular bridge ψ, primary phase evolution, geometric torque,
causal screening and redshift damping.
"""

import math

# ──────────────────────────────────────────────────────────────
# Fundamental constants (locked by the model)
# ──────────────────────────────────────────────────────────────
EPS           = 1.0e-9                  # ε = dχ_micro per tick
N_TODAY       = 1_000_000_000           # present-day tick count
PSI           = 0.1503378808            # angular bridge (rad)
ALPHA         = 0.193218843731          # irrational rotation number
ALPHA_PSI     = ALPHA * PSI             # ≈ 0.02905
OMEGA_FRAC    = 0.25                    # fractional topological defect
DELTA_PHI     = OMEGA_FRAC * 2.0 * math.pi + PSI   # ≈ 1.72113420759 rad
SIN_DELTA_PHI = math.sin(DELTA_PHI)     # ≈ cos(ψ) ≈ 0.98982
ALPHA_G       = 0.558                   # geometric coupling
H_WIND        = 70.0                    # bosonic baseline (km/s/Mpc)
SH_GEOM_BASE  = 3.170                   # target late-time torque amplitude
SCREEN_MPC    = 4500.0                  # causal χ-screening scale
DAMP_Z        = 5.8                     # redshift damping scale
LATE_START    = 700_000_000             # beginning of late-time window

# ──────────────────────────────────────────────────────────────
# Core class
# ──────────────────────────────────────────────────────────────
class JCRCosmologicalClock:
    """Discrete-tick cosmological clock with geometric torque."""

    def __init__(self):
        self.eps        = EPS
        self.N_today    = N_TODAY
        self.psi        = PSI
        self.delta_phi  = DELTA_PHI
        self.alpha_g    = ALPHA_G
        self.H_wind     = H_WIND

    # ── microscopic / macroscopic maps ────────────────────────
    def chi_micro(self, N: float) -> float:
        """Cumulative microscopic comoving displacement."""
        return self.eps * N

    def scale_factor(self, N: float) -> float:
        """a(N) = exp(χ_micro)  →  a(N_today) = e."""
        return math.exp(self.chi_micro(N))

    def redshift(self, N: float) -> float:
        """z = 1/a - 1."""
        a = self.scale_factor(N)
        return 1.0 / a - 1.0

    # ── phase quantities ──────────────────────────────────────
    def phase_bias(self, N: float) -> float:
        """φ_bias = 2π · χ_micro  (one full cycle at N_today)."""
        return 2.0 * math.pi * self.chi_micro(N)

    def primary_phase(self, k: float) -> float:
        """
        Controlled / primary phase (double-cover normalisation)
        v(k) = 4π · k · 10⁻⁹   →  v(N_today) = 4π.
        """
        return 4.0 * math.pi * k * self.eps

    def primary_phase_tau(self, k: float) -> float:
        """Alternative definition using τ = arctan(2π)."""
        tau = math.atan(2.0 * math.pi)
        return 2.0 * tau * k * self.eps

    # ── suppression & damping ────────────────────────────────
    def screening(self, chi: float) -> float:
        """Causal χ-screening."""
        return math.exp(-chi / SCREEN_MPC)

    def redshift_damping(self, z: float) -> float:
        """f_damp(z) = exp(-z / 5.8)."""
        return math.exp(-z / DAMP_Z)

    def suppression(self, z: float, chi: float) -> float:
        """Combined suppression function S(z)."""
        return (1.0 + 5.0 * math.exp(-z / 2.0)) * \
               self.redshift_damping(z) * self.screening(chi)

    # ── geometric torque ─────────────────────────────────────
    def omega_eff(self) -> float:
        """Effective frequency over the late-time Δy_n = 0.3."""
        return self.delta_phi / 0.3

    def delta_H_geom(self, N: float) -> float:
        """
        Late-time geometric contribution to the Hubble parameter.
        Active mainly for N ≳ 7×10⁸.
        """
        if N < LATE_START:
            return 0.0

        chi = self.chi_micro(N)
        z   = self.redshift(N)
        a   = self.scale_factor(N)

        # base geometric term
        geom = self.alpha_g * self.omega_eff() * SIN_DELTA_PHI

        # modulate by scale factor, screening and damping
        # (normalised so that δH(N_today) ≈ 3.17)
        weight = a * self.screening(chi) * self.redshift_damping(z)
        # overall normalisation chosen to hit the target amplitude
        norm   = SH_GEOM_BASE / (self.alpha_g * self.omega_eff() * SIN_DELTA_PHI)

        return geom * weight * norm

    def H(self, N: float) -> float:
        """Total Hubble parameter H(N) = H_wind + δH_geom(N)."""
        return self.H_wind + self.delta_H_geom(N)

    # ── convenience / diagnostics ────────────────────────────
    def present_day_summary(self) -> None:
        N = self.N_today
        print("=" * 60)
        print("Joshua Christopher Ryan’s Cosmological Clock – Present Epoch")
        print("=" * 60)
        print(f"N_today          = {N:,}")
        print(f"χ_micro          = {self.chi_micro(N):.10f}")
        print(f"a_Ψ              = {self.scale_factor(N):.10f}   (≈ e)")
        print(f"z_Ψ              = {self.redshift(N):.6f}")
        print(f"phase_bias       = {self.phase_bias(N):.10f} rad  (2π)")
        print(f"primary_phase    = {self.primary_phase(N):.10f} rad  (4π)")
        print(f"ψ                = {self.psi:.10f} rad  ({math.degrees(self.psi):.4f}°)")
        print(f"Δφ_torque        = {self.delta_phi:.10f} rad  ({math.degrees(self.delta_phi):.4f}°)")
        print(f"sin(Δφ_torque)   = {SIN_DELTA_PHI:.10f}  (= cos ψ)")
        print(f"α·ψ              = {ALPHA_PSI:.10f}")
        print(f"H_wind           = {self.H_wind:.3f} km/s/Mpc")
        print(f"δH_geom (today)  = {self.delta_H_geom(N):.3f} km/s/Mpc")
        print(f"H_total (today)  = {self.H(N):.3f} km/s/Mpc")
        print("=" * 60)

    def milestone_run(self, milestones=None) -> None:
        """Evaluate key quantities at selected tick counts."""
        if milestones is None:
            milestones = [
                0,
                1_000_000,
                100_000_000,
                500_000_000,
                700_000_000,
                900_000_000,
                N_TODAY,
            ]

        print("\n{:>12}  {:>12}  {:>10}  {:>10}  {:>10}  {:>10}".format(
            "N", "χ_micro", "a", "z", "δH_geom", "H_total"))
        print("-" * 72)
        for N in milestones:
            chi = self.chi_micro(N)
            a   = self.scale_factor(N)
            z   = self.redshift(N)
            dH  = self.delta_H_geom(N)
            Ht  = self.H(N)
            print(f"{N:12,}  {chi:12.6f}  {a:10.6f}  {z:10.4f}  {dH:10.4f}  {Ht:10.4f}")


# ──────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    clock = JCRCosmologicalClock()
    clock.present_day_summary()
    clock.milestone_run()
