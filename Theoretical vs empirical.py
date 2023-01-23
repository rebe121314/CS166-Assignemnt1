#THEORETICAL RESULTS
print("Empirical & Theoretical Analyses")

#------- Average Wait Time ---------------- 
def theoretical_avg_wait_time(rho, tau=3, sigma=1): 
    return 10*(rho*tau / 2*(1-rho)) * (1 + sigma**2 / tau**2)

theoretical_wait_times = []
for i in range(1,11): 
    rho = 1/i * 3
    theoretical_wait_times.append(theoretical_avg_wait_time(rho))

plt.figure()

plt.title('Average Wait Times for different Arrival Rates empirical and theoretical results')
plt.xlabel('Number of Cashiers')
plt.ylabel('Average Wait Times')


plt.errorbar(cashiers, waiting_times_mean, waiting_times_std, color='black', marker='o', capsize=5, linestyle='--', 
             linewidth=1, label='empirical')
plt.plot(cashiers, theoretical_wait_times, color='red', marker='o', linestyle='--', linewidth=1, label='theoretical')
#plt.ylim(-10,50) 
plt.legend()
plt.show()


# ------------ Average Queue Length -----------

def theoretical_avg_queue_length(rho, lmd, tau=3, sigma=1): 
    return 10*lmd*(rho**2 / 2*(1-rho))

theoretical_avg_queue_lengths = [] 
for i in range(1,11):  
    rho = 1/i * 3
    lmd = 1/i
    theoretical_avg_queue_lengths.append(theoretical_avg_queue_length(rho,lmd)) 

plt.figure()

plt.title('Average Queue Lengths for different Arrival Rates empirical and theoretical results')
plt.xlabel('Number of Cashiers')
plt.ylabel('Average Queue Lengths')


plt.errorbar(cashiers, queue_lengths_mean, queue_lengths_std, color='black', marker='o', capsize=5, linestyle='--', 
             linewidth=1, label='empirical')
plt.plot(cashiers, theoretical_avg_queue_lengths, color='red', marker='o', linestyle='--', linewidth=1, label='theoretical')
#plt.ylim(-10,50)
plt.legend()
plt.show()


# ------------ Wait Time of last customer after Closing Time -----------

def theoretical_wait_duration(...): 
    return ...

theoretical_wait_times = []
for i in range(1,11):  
    rho = 1/i * 3
    theoretical_wait_times.append(theoretical_wait_duration(...))

plt.figure()

plt.title('Wait time of last customer after Closing Time empirical and theoretical results')
plt.xlabel('Number of Cashiers')
plt.ylabel('wait time of last customer after closing')


plt.errorbar(cashiers, last_customer_times_mean, last_customer_times_std, color='black', marker='o', capsize=5, linestyle='--', 
             linewidth=1, label='empirical')

plt.plot(cashiers, theoretical_queue_lengths, color='red', marker='o', linestyle='--', linewidth=1, label='theoretical')
#plt.ylim(-10,50)
plt.legend()
plt.show()
