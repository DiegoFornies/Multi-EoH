
def heuristic(input_data):
    """Schedule by prioritizing machines with the least current workload."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_workload = {m: 0 for m in range(n_machines)}
    job_end_times = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        current_time = job_end_times[job_id]

        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            
            #Find the machine with the smallest work load
            best_machine = None
            min_workload = float('inf')

            for i, machine in enumerate(machines):
                if machine_workload[machine] < min_workload:
                    min_workload = machine_workload[machine]
                    best_machine = machine
                    best_time = times[i]

            start_time = max(current_time, machine_workload[best_machine])
            end_time = start_time + best_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_workload[best_machine] = end_time
            current_time = end_time
        
        job_end_times[job_id] = current_time

    return schedule
