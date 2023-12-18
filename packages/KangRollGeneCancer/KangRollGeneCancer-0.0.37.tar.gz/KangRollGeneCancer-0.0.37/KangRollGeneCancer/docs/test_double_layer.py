import numpy as np
import matplotlib.pyplot as plt

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

# Define the initial parameters for the layers
tau1 = 0.1
B1 = 0.8
tau2 = 0.1
B2 = 0.0 # Assuming B2 is zero since it's not specified
n_iterations = 10

# Start with an initial value for u1
u1_initial = 0.1

# Run the first layer to get u1 after 10 iterations
u1_final = layer_one(u1_initial, tau1, B1, n_iterations)

# Pass the final value of the first layer to the second layer as initial value
u2_initial = u1_final

# Run the second layer to get u2 after 10 iterations
u2_final = layer_two(u2_initial, tau2, B2, n_iterations)

# Print the results
print(f"Final value of u1 after 10 iterations: {u1_final}")
print(f"Final value of u2 after 10 iterations: {u2_final}")

# Now, let's simulate the network over 20 time steps to get the time series for v3
u1_values = [u1_initial]
u2_values = [u2_initial]


# Simulate the first layer over 10 time steps
for _ in range(n_iterations):
    u1_values.append(layer_one(u1_values[-1], tau1, B1, 1))

# Use the final value of the first layer as the initial value for the second layer
u2_values[0] = u1_values[-1]

# Simulate the second layer over 10 time steps
for _ in range(n_iterations):
    u2_values.append(layer_two(u2_values[-1], tau2, B2, 1))

# Plot the time series for v3
plt.figure(figsize=(10, 5))
plt.plot(u1_values, label='u1 values')
plt.plot(u2_values, label='u2 values')
plt.title('Time series of the two-layer network (v3)')
plt.xlabel('Time step')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
# plt.show()

# The final neoplastic load is assumed to be the last element of the u2 time series
v4_neoplastic_load = u2_values[-1]
print(f"Neoplastic load (v4): {v4_neoplastic_load}")

# next  -----

# Now, let's simulate the network over 20 time steps to get the time series for v3
u_values = [u1_initial]


# Simulate the first layer over 10 time steps
for _ in range(n_iterations):
    u_values.append(layer_one(u_values[-1], tau1, B1, 1))

# Use the final value of the first layer as the initial value for the second layer
u2_values[0] = u1_values[-1]

# Simulate the second layer over 10 time steps
for _ in range(n_iterations):
    u_values.append(layer_two(u_values[-1], tau2, B2, 1))

# Plot the time series for v3
plt.figure(figsize=(10, 5))
plt.plot(u1_values, label='u1 values')
plt.plot(u2_values, label='u2 values')
plt.plot(u_values, label='u values')
plt.title('Time series of the two-layer network (v3)')
plt.xlabel('month')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()

# The final neoplastic load is assumed to be the last element of the u2 time series
v4_neoplastic_load = u2_values[-1]
print(f"Neoplastic load (v4): {v4_neoplastic_load}")

