import numpy as np




# import numpy as np

# # Define initial parameters for DNA damage and gene functional feature spectrum
# DNA_damage = 0.1
# GFFS = np.array([0, 1, 1, 0] + [0]*12 + [DNA_damage])

# # Initialize the weight matrix W for mapping GFFS to adjustment factor
# W = np.zeros((4, 17))
# W[2, 2] = W[0, 0] = -1

# # Function to compute the adjustment factor delta
# def compute_delta(W, V2):
#     return W @ V2

# # Function to adjust the Harmonic Set H3
# def adjust_harmonic_set(H3, delta):
#     return H3 + delta * H3

# # Initial state of Harmonic Set H
# H = np.array([0.1, 10, 0.8, 0])

# # Compute the adjustment factor delta
# delta = compute_delta(W, GFFS)

# # Adjust the Harmonic Set with the computed delta
# H3_adjusted = adjust_harmonic_set(H, delta)

# # Define function to simulate the Multi-Layer Network (Placeholder)
# def simulate_MLN(H3):
#     # Placeholder for actual simulation logic
#     return np.random.rand(4)

# # Define function to calculate neoplastic load from MLN output (Placeholder)
# def calculate_NL(MLN_output):
#     # Placeholder for actual neoplastic load calculation
#     return MLN_output[-1]

# # Function to print the details in a structured format
# def print_details(iteration, H_input, delta, H_adjusted, MLN_output=None, NL=None):
#     print(f"------V{iteration}--：输入: {H_input}, Delta: {delta}, 输出: {H_adjusted}")
#     if MLN_output is not None and NL is not None:
#         print(f"MLN输出: {MLN_output}, Neoplastic Load: {NL}")

# # Simulate the Multi-Layer Network dynamics over n iterations
# for iteration in range(10):
#     print_details(iteration + 1, H, delta, H3_adjusted)
#     # Compute the MLN output
#     MLN_output = simulate_MLN(H3_adjusted)
#     # Update the Harmonic Set for the next iteration
#     H3_adjusted = adjust_harmonic_set(H3_adjusted, delta)
#     # Calculate the neoplastic load
#     NL_final = calculate_NL(MLN_output)
#     print_details(iteration + 1, H, delta, H3_adjusted, MLN_output, NL_final)

# print("Final Neoplastic Load:", NL_final)



import numpy as np

# Define initial parameters for DNA damage and gene functional feature spectrum
DNA_damage = 0.1
V2_GFFS = np.array([0, 1, 1, 0] + [0]*12 + [DNA_damage])

# Initialize the weight matrix W for mapping GFFS to adjustment factor
W_V3_adjustment = np.zeros((4, 17))
W_V3_adjustment[2, 2] = W_V3_adjustment[0, 0] = -1

# Function to compute the adjustment factor delta
def V3_compute_delta(W, V2):
    return W @ V2

# Function to adjust the Harmonic Set H3
def V3_adjust_H3(H3, delta):
    return H3 + delta * H3

# Initial state of Harmonic Set H
H_V1_initial = np.array([0.1, 10, 0.8, 0])

# Compute the adjustment factor delta
delta_V3 = V3_compute_delta(W_V3_adjustment, V2_GFFS)

# Adjust the Harmonic Set with the computed delta
H3_V3_adjusted = V3_adjust_H3(H_V1_initial, delta_V3)

# Define function to simulate the Multi-Layer Network (Placeholder)
def V3_simulate_MLN(H3):
    # Placeholder for actual simulation logic
    return np.random.rand(4)

# Define function to calculate neoplastic load from MLN output (Placeholder)
def V4_calculate_NL(MLN_output):
    # Placeholder for actual neoplastic load calculation
    return MLN_output[-1]

# Function to print the details in a structured format
def print_details_V5(iteration, H_input, delta, H_adjusted, MLN_output=None, NL=None):
    print(f"------V{iteration}--：输入: {H_input}, Delta: {delta}, 输出: {H_adjusted}")
    if MLN_output is not None and NL is not None:
        print(f"MLN输出: {MLN_output}, Neoplastic Load: {NL}")

# Simulate the Multi-Layer Network dynamics over n iterations
for iteration in range(10):
    print_details_V5(iteration + 1, H_V1_initial, delta_V3, H3_V3_adjusted)
    # Compute the MLN output
    MLN_output_V3 = V3_simulate_MLN(H3_V3_adjusted)
    # Update the Harmonic Set for the next iteration
    H3_V3_adjusted = V3_adjust_H3(H3_V3_adjusted, delta_V3)
    # Calculate the neoplastic load
    NL_final_V4 = V4_calculate_NL(MLN_output_V3)
    print_details_V5(iteration + 1, H_V1_initial, delta_V3, H3_V3_adjusted, MLN_output_V3, NL_final_V4)

print("Final Neoplastic Load:", NL_final_V4)
