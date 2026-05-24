import math

# Original numbers from your chain
a = 34.4234079
b = 0.01068679
c = 0.36787573
d = 0.02905

num = 0.015100213963290712
den = 0.041046637215325

sqrt2_approx = 1.4144472
inv_sqrt2_approx = 0.7071
one_over_e_approx = 0.367879

# Computations
step1 = a * b
step2 = c * d
ratio = num / den
exp_result = math.exp(ratio)
product = sqrt2_approx * inv_sqrt2_approx
final_e = product / one_over_e_approx

print(f"1. {a} × {b} = {step1:.8f}")
print(f"2. {c} × {d} = {step2:.8f}")
print(f"3. {num} ÷ {den} = {ratio:.8f}  (≈ 1/e)")
print(f"4. exp({ratio:.8f}) = {exp_result:.8f}")
print(f"5. {sqrt2_approx} × {inv_sqrt2_approx} = {product:.8f}")
print(f"6. {product:.8f} ÷ {one_over_e_approx} = {final_e:.8f}")
print(f"\nTrue e = {math.e:.12f}")
