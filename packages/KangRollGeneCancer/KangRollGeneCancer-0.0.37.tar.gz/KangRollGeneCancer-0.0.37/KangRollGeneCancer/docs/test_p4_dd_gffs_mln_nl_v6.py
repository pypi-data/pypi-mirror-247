
import numpy as np
# Adjusted code based on the provided specifications

# Define initial parameters for DNA damage and gene functional feature spectrum
v1_DNA_damage = 0.1
V2_GFFS = np.array([0, 1, 1, 0] + [0]*12 + [v1_DNA_damage])

# Print the Gene Functional Feature Spectrum V2
print("Gene Functional Feature Spectrum V2 (V2_GFFS):")
print(V2_GFFS)
print("------")

# Initialize the weight matrix W for mapping GFFS to adjustment factor
W_V3_adjustment = np.zeros((4, 17))
W_V3_adjustment[2, 2] = W_V3_adjustment[0, 0] = -1

# Print the weight matrix W
print("Weight Matrix W (W_V3_adjustment):")
print(W_V3_adjustment)
print("------")

# Function to compute the adjustment factor delta
def V3_compute_delta(W, V2):
    return W @ V2

# Function to adjust the Harmonic Set H3
def V3_adjust_H3(H3, delta):
    return H3 + delta * H3

# Initial state of Harmonic Set H
H_V1_initial = np.array([0.1, 10, 2.8, 0])
print("-----V1: Initial Harmonic Set H (H_V1_initial):")
print(H_V1_initial)
print("------")

# Compute the adjustment factor delta
print("-----V3.1:    Computed Adjustment Factor Delta (delta_V3):")
print('W_V3_adjustment =',W_V3_adjustment)
print('V2_GFFS =',V2_GFFS)

delta_V3 = V3_compute_delta(W_V3_adjustment, V2_GFFS)
print("-----V3.1:    Computed Adjustment Factor Delta (delta_V3): delta_V3= W @ V2 ")
print(delta_V3)
print("------")

# Adjust the Harmonic Set with the computed delta
print("-----V3.2:    Before (H3_V3_adjusted):")
print('H3（H_V1_initial）=',H_V1_initial)
print('delta_V3=',delta_V3)

H3_V3_adjusted = V3_adjust_H3(H_V1_initial, delta_V3)
print("-----V3.2:    Harmonic Set H3 adjusted with Delta (H3_V3_adjusted):")
print(H3_V3_adjusted)
print("------")




# Define the iterative function for the first layer of the network
def layer_one(u1, tau1, B1, n_iterations):
    for _ in range(n_iterations):
        u1 = u1 + tau1 * (B1 - u1)
    return u1

# Define the iterative function for the second layer of the network
def layer_two(u2, tau2, B2, n_iterations):
    for _ in range(n_iterations):
        u2 = u2 + tau2 * (B2 - u2)
    return u2

# Define function to calculate neoplastic load from MLN output (Placeholder)
def V4_calculate_NL(MLN_output):
    # Assuming the neoplastic load is the last element of the MLN output
    return MLN_output[-1]

# Function to print the details in a structured format
def print_details_V5(iteration, H_input, delta, H_adjusted, MLN_output=None, NL=None):
    print(f"迭代 {iteration}:")
    print(f"输入 Harmonic Set H: {H_input}, Delta: {delta}, 调整后 Harmonic Set H: {H_adjusted}")
    if MLN_output is not None and NL is not None:
        print(f"MLN输出: {MLN_output}, Neoplastic Load: {NL}")
    print("------")

# Integrate the two-layer network simulation into the main simulation loop
def V3_simulate_MLN(H3, iterations=10):
    # For simplicity, we're using a simple iterative approach to simulate the MLN
    u1 = H3[0]
    tau1 = H3[1]
    B1 = H3[2]

    # First layer iterations
    u1_final = layer_one(u1, tau1, B1, iterations)
    
    # Second layer starts with the result of the first
    tau2 = H3[3]
    print('-----V3_simulate_MLN----------:  \n  tau2  = ',tau2)
    B2 = 0 # Assuming a value for B2, since it's not defined
    u2_final = layer_two(u1_final, tau2, B2, iterations)
        # Print statements
    print(f"tau1: {tau1}, B1: {B1}, tau2: {tau2}, B2: {B2}")

    
    return np.array([u1_final, u2_final])

# Define the initial parameters for the layers
H_V1_initial = np.array([0.1, 0.1, 0.8, 0.1])  # Example values for H3 structure
delta_V3 = np.array([0, 0, -0.1, 0])  # Example delta values

# Simulate the Multi-Layer Network dynamics over 3 iterations
for iteration in range(3):
    print_details_V5(iteration + 1, H_V1_initial, delta_V3, H_V1_initial)
    # Compute the MLN output
    MLN_output_V3 = V3_simulate_MLN(H_V1_initial)
    # Calculate the neoplastic load
    NL_final_V4 = V4_calculate_NL(MLN_output_V3)
    print_details_V5(iteration + 1, H_V1_initial, delta_V3, H_V1_initial, MLN_output_V3, NL_final_V4)

print("Final Neoplastic Load after 3 Iterations:", NL_final_V4)







