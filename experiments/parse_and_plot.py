import csv
import matplotlib.pyplot as plt
import numpy as np

# Define lists for nofilter experiments
nofilter_500_cycles_u = []
nofilter_500_cycles_k = []
nofilter_500_instructions_u = []
nofilter_500_instructions_k = []
nofilter_1000_cycles_u = []
nofilter_1000_cycles_k = []
nofilter_1000_instructions_u = []
nofilter_1000_instructions_k = []

# Define lists for rbac experiments
rbac_500_cycles_u = []
rbac_500_cycles_k = []
rbac_500_instructions_u = []
rbac_500_instructions_k = []
rbac_1000_cycles_u = []
rbac_1000_cycles_k = []
rbac_1000_instructions_u = []
rbac_1000_instructions_k = []

# Define a function to extract values from the CSV file
def extract_values(filename, cycles_u_list, cycles_k_list, instructions_u_list, instructions_k_list):
    with open(filename, 'r') as f:
        next(f)
        next(f)
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[3] == 'cycles:u' and row[1].isnumeric():
                cycles_u_list.append(int(row[1]))
            elif row[3] == 'cycles:k' and row[1].isnumeric():
                cycles_k_list.append(int(row[1]))
            elif row[3] == 'instructions:u' and row[1].isnumeric():
                instructions_u_list.append(int(row[1]))
            elif row[3] == 'instructions:k' and row[1].isnumeric():
                instructions_k_list.append(int(row[1]))

# Parse values from each file
extract_values('/home/mbues/Spark/UTSpark/experiments/nofilter/500.csv', nofilter_500_cycles_u, nofilter_500_cycles_k, nofilter_500_instructions_u, nofilter_500_instructions_k)
extract_values('/home/mbues/Spark/UTSpark/experiments/nofilter/1000.csv', nofilter_1000_cycles_u, nofilter_1000_cycles_k, nofilter_1000_instructions_u, nofilter_1000_instructions_k)
extract_values('/home/mbues/Spark/UTSpark/experiments/rbac/500.csv', rbac_500_cycles_u, rbac_500_cycles_k, rbac_500_instructions_u, rbac_500_instructions_k)
extract_values('/home/mbues/Spark/UTSpark/experiments/rbac/1000.csv', rbac_1000_cycles_u, rbac_1000_cycles_k, rbac_1000_instructions_u, rbac_1000_instructions_k)

# Get averages
nofilter_500_cycles_u_avg = sum(nofilter_500_cycles_u) / len(nofilter_500_cycles_u)
nofilter_500_cycles_k_avg = sum(nofilter_500_cycles_k) / len(nofilter_500_cycles_k)
nofilter_500_instructions_u_avg = sum(nofilter_500_instructions_u) / len(nofilter_500_instructions_u)
nofilter_500_instructions_k_avg = sum(nofilter_500_instructions_k) / len(nofilter_500_instructions_k)

nofilter_1000_cycles_u_avg = sum(nofilter_1000_cycles_u) / len(nofilter_1000_cycles_u)
nofilter_1000_cycles_k_avg = sum(nofilter_1000_cycles_k) / len(nofilter_1000_cycles_k)
nofilter_1000_instructions_u_avg = sum(nofilter_1000_instructions_u) / len(nofilter_1000_instructions_u)
nofilter_1000_instructions_k_avg = sum(nofilter_1000_instructions_k) / len(nofilter_1000_instructions_k)

rbac_500_cycles_u_avg = sum(rbac_500_cycles_u) / len(rbac_500_cycles_u)
rbac_500_cycles_k_avg = sum(rbac_500_cycles_k) / len(rbac_500_cycles_k)
rbac_500_instructions_u_avg = sum(rbac_500_instructions_u) / len(rbac_500_instructions_u)
rbac_500_instructions_k_avg = sum(rbac_500_instructions_k) / len(rbac_500_instructions_k)

rbac_1000_cycles_u_avg = sum(rbac_1000_cycles_u) / len(rbac_1000_cycles_u)
rbac_1000_cycles_k_avg = sum(rbac_1000_cycles_k) / len(rbac_1000_cycles_k)
rbac_1000_instructions_u_avg = sum(rbac_1000_instructions_u) / len(rbac_1000_instructions_u)
rbac_1000_instructions_k_avg = sum(rbac_1000_instructions_k) / len(rbac_1000_instructions_k)

### PLOTTING
# Instruction count
labels = (
    "No Filter (500)",
    "No Filter (1000)",
    "RBAC (500)",
    "RBAC (1000)"
)
instr_counts = {
    "User": np.array([nofilter_500_instructions_u_avg, nofilter_1000_instructions_u_avg, 
                      rbac_500_instructions_u_avg, rbac_1000_instructions_u_avg]),
    "Kernel": np.array([nofilter_500_instructions_k_avg, nofilter_1000_instructions_k_avg,
                        rbac_500_instructions_k_avg, rbac_1000_instructions_k_avg]),
}

# total instructions per request, to be annotated on each bar
ins_per_req = []
for idx, experiment in enumerate(instr_counts["User"]): # starts at 0
    total_ins = instr_counts["User"][idx] + instr_counts["Kernel"][idx]
    if idx % 2 == 0:
        ins_per_req.append( total_ins / 500)
    else:
        ins_per_req.append( total_ins / 1000)



# Plot
width = 0.4
fig, ax = plt.subplots()
bottom = np.zeros(4)

for i, boolean in enumerate(instr_counts.keys()):
    ins_count = instr_counts[boolean]
    p = ax.bar(labels, ins_count, width, label=boolean, bottom=bottom)
    bottom += ins_count

# Add ins/req annotation
for i, count in enumerate(ins_per_req):
    rate = 500
    if i%2 == 1:
        rate *= 2
    ax.annotate(str(int(count))+ " instr/req",
                xy=(i, count*rate),
                xytext=(0, 2),
                textcoords="offset points",
                ha='center', va='bottom')


ax.set_title("Instruction Counts for 1 CPU")
ax.legend(loc="upper left")

plt.savefig('/home/mbues/Spark/UTSpark/experiments/figures/instructions-nofilter-rbac-1cpu-100-rate-500-1000.png')
plt.show()

# Cycle count
cycle_counts = {
    "User": np.array([nofilter_500_cycles_u_avg, nofilter_1000_cycles_u_avg, 
                      rbac_500_cycles_u_avg, rbac_1000_cycles_u_avg]),
    "Kernel": np.array([nofilter_500_cycles_k_avg, nofilter_1000_cycles_k_avg,
                        rbac_500_cycles_k_avg, rbac_1000_cycles_k_avg]),
}

# total cycles per request, to be annotated on each bar
cycles_per_req = []
for idx, experiment in enumerate(cycle_counts["User"]): # starts at 0
    total_cycles = cycle_counts["User"][idx] + cycle_counts["Kernel"][idx]
    if idx % 2 == 0:
        cycles_per_req.append( total_cycles / 500)
    else:
        cycles_per_req.append( total_cycles / 1000)

# Plot
width = 0.4
fig, ax = plt.subplots()
bottom = np.zeros(4)
i=1

for i, boolean in enumerate(cycle_counts.keys()):
    cycle_count = cycle_counts[boolean]
    p = ax.bar(labels, cycle_count, width, label=boolean, bottom=bottom)
    bottom += cycle_count

# Add cycles/req annotation
for i, count in enumerate(cycles_per_req):
    rate = 500
    if i%2 == 1:
        rate *= 2
    ax.annotate(str(int(count))+ " cycles/req",
                xy=(i, count*rate),
                xytext=(0, 2),
                textcoords="offset points",
                ha='center', va='bottom')


ax.set_title("Cycle Counts for 1 CPU")
ax.legend(loc="upper left")

plt.savefig('/home/mbues/Spark/UTSpark/experiments/figures/cycles-nofilter-rbac-1cpu-100-rate-500-1000.png')
plt.show()

# Print
print("nofilter_500_cycles_u:", nofilter_500_cycles_u[0:10])
print("nofilter_500_cycles_k:", nofilter_500_cycles_k[0:10])
print("nofilter_500_instructions_u:", nofilter_500_instructions_u[0:10])
print("nofilter_500_instructions_k:", nofilter_500_instructions_k[0:10])
print("nofilter_1000_cycles_u:", nofilter_1000_cycles_u[0:10])
print("nofilter_1000_cycles_k:", nofilter_1000_cycles_k[0:10])
print("nofilter_1000_instructions_u:", nofilter_1000_instructions_u[0:10])
print("nofilter_1000_instructions_k:", nofilter_1000_instructions_k[0:10])
print("rbac_500_cycles_u:", rbac_500_cycles_u[0:10])
print("rbac_500_cycles_k:", rbac_500_cycles_k[0:10])
print("rbac_500_instructions_u:", rbac_500_instructions_u[0:10])
print("rbac_500_instructions_k:", rbac_500_instructions_k[0:10])
print("rbac_1000_cycles_u:", rbac_1000_cycles_u[0:10])
print("rbac_1000_cycles_k:", rbac_1000_cycles_k[0:10])
print("rbac_1000_instructions_u:", rbac_1000_instructions_u[0:10])

