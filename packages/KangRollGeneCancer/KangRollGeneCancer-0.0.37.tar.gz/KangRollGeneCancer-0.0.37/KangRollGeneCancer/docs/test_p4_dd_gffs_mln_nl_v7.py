
import numpy as np
# Adjusted code based on the provided specifications

# Define initial parameters for DNA damage and gene functional feature spectrum
v1 = 0.1   #DNA_damage
v2 = np.array([0, 1, 1, 0] + [0]*12 + [v1])   # V2: GFFS

# Print the Gene Functional Feature Spectrum V2
print("Gene Functional Feature Spectrum V2 (v2):")
print(v2)
print("------")

# Initialize the weight matrix W for mapping GFFS to adjustment factor
W_v3= np.zeros((4, 17))   # W_V3 adjustment
W_v3[2, 2] = W_v3[0, 0] = -1

# Print the weight matrix W
print("Weight Matrix W (W_v3):")
print(W_v3)
print("------")

# Function to compute the adjustment factor delta
def V3_compute_delta(W, V2):
    return W @ V2

# Function to adjust the Harmonic Set H3
def V3_adjust_H3(H3, delta):
    w= 0.1 #weight_inside = 
    return H3 + w*delta * H3

# Initial state of Harmonic Set H
H3_ini = np.array([0.1, 10, 0.8, 0])
print("-----V1: Initial Harmonic Set H (H3_ini):")
print(H3_ini)
print("------")

# Compute the adjustment factor delta
print("-----V3.1:    Computed Adjustment Factor Delta (delta_v3 ):")
print('W_v3=',W_v3)
print('v2 =',v2)

delta_v3 = V3_compute_delta(W_v3, v2)
print("-----V3.1:    Computed Adjustment Factor Delta (delta_v3 ): delta_v3 = W @ V2 ")
print(delta_v3 )
print("------")

# Adjust the Harmonic Set with the computed delta
print("-----V3.2:    Before (V3_adjust_H3---Genamonic Transfor):")
print('H3（H3_ini）=',H3_ini)
print('delta_v3 =',delta_v3 )

H3_after_genamonic_tf= V3_adjust_H3(H3_ini, delta_v3 )
print("-----V3.2:    Harmonic Set H3 adjusted with Delta (V3_adjust_H3----Genamonic Transfor):")
print('H3_after_genamonic_tf=',H3_after_genamonic_tf)
print("------")

H3_v3 = H3_after_genamonic_tf  #  H3_v3  used for v3.

print('---------Prepare for H3_v3 -------:\n')
print('-- H3_v3 = ',H3_v3)


print('------------------------------------------------DO -------M L N  -------------------------\n')
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
    # u1 = H3[0]
    u1 = 10
    tau1 = H3[0]
    B1 = H3[1]
    # Second layer starts with the result of the first
    tau2 = H3[2]
    B2 = H3[3] # Assuming a value for B2, since it's not defined

    # First layer iterations
    u1_final = layer_one(u1, tau1, B1, iterations)

    print('-----V3_simulate_MLN----------:  \n  tau2  = ',tau2)
    
    u2_final = layer_two(u1_final, tau2, B2, iterations)
        # Print statements
    print(f"tau1: {tau1}, B1: {B1}, tau2: {tau2}, B2: {B2}")    
    return np.array([u1_final, u2_final])

# # Define the initial parameters for the layers
# H3_ini = np.array([0.1, 0.1, 0.8, 0.1])  # Example values for H3 structure
# delta_v3 = np.array([0, 0, -0.1, 0])  # Example delta values

# Simulate the Multi-Layer Network dynamics over 3 iterations
for iteration in range(3):
    print_details_V5(iteration + 1, H3_v3, delta_v3 , H3_v3)
    # Compute the MLN output
    MLN_output_V3 = V3_simulate_MLN(H3_v3)
    # Calculate the neoplastic load
    print ('-----------------------do V4 - N L ---------------------\n')
    NL_final_V4 = V4_calculate_NL(MLN_output_V3)
    print_details_V5(iteration + 1, H3_v3, delta_v3, H3_v3, MLN_output_V3, NL_final_V4)

print("Final Neoplastic Load after 3 Iterations:", NL_final_V4)







