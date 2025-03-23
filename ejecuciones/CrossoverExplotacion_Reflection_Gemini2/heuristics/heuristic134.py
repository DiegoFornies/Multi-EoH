
def heuristic(input_data):
    """Heuristic combines SPT, earliest start, and machine load balance."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {}
    
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        last_end_time = 0 # Keep track of the previous op

        for op_idx, operation in enumerate(jobs_data[job_id]):
            machines = operation[0]
            processing_times = operation[1]

            best_machine = None
            min_weighted_end_time = float('inf')
            best_start_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                processing_time = processing_times[i]
                start_time = max(machine_available[machine], job_completion[job_id])
                end_time = start_time + processing_time
                
                #load penalty, idle time
                idle_time = start_time - last_end_time if op_idx > 0 else 0
                weighted_finish = end_time + 0.1 * machine_load[machine] - 0.05 * idle_time
                
                if weighted_finish < min_weighted_end_time:
                    min_weighted_end_time = weighted_finish
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            start_time = max(machine_available[best_machine], job_completion[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available[best_machine] = end_time
            job_completion[job_id] = end_time
            machine_load[best_machine] += best_processing_time
            last_end_time = end_time

    return schedule
