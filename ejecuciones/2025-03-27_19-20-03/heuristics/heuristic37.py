
def heuristic(input_data):
    """Minimizes makespan by balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        current_time = 0
        for op_idx, operation in enumerate(jobs[job_id]):
            op_num = op_idx + 1
            machines_op = operation[0]
            times_op = operation[1]
            best_machine = None
            min_load = float('inf')
            best_time = None

            for i, machine in enumerate(machines_op):
                if machine_load[machine] < min_load:
                    min_load = machine_load[machine]
                    best_machine = machine
                    best_time = times_op[i]
            
            start_time = max(current_time, machine_load[best_machine])
            end_time = start_time + best_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })
            machine_load[best_machine] = end_time
            current_time = end_time
            job_completion[job_id] = end_time
            
    return schedule
