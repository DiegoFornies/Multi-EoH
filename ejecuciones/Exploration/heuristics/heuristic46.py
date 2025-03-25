
def heuristic(input_data):
    """Combines greedy scheduling with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    
    remaining_operations = {job: list(range(len(ops))) for job, ops in jobs.items()}

    while any(remaining_operations[job] for job in jobs):
        eligible_operations = []
        for job in jobs:
            if remaining_operations[job]:
                eligible_operations.append(job)

        best_job, best_machine, best_start_time, best_end_time, best_processing_time = None, None, float('inf'), float('inf'), None

        for job in eligible_operations:
            op_idx = remaining_operations[job][0]
            machines, times = jobs[job][op_idx]

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_end_time[job])
                end_time = start_time + processing_time

                #Prioritize machine with low load, breaking ties with early finish
                load_adjusted_end_time = end_time + machine_load[machine] / 100 #bias factor

                if load_adjusted_end_time < best_end_time:
                    best_job, best_machine, best_start_time, best_end_time, best_processing_time = job, machine, start_time, end_time, processing_time

        if best_job is not None:
            job = best_job
            op_idx = remaining_operations[job][0]
            machine = best_machine
            start_time = best_start_time
            end_time = best_end_time
            processing_time = best_processing_time
            
            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = end_time
            job_end_time[job] = end_time
            machine_load[machine] += processing_time
            remaining_operations[job].pop(0)

    return schedule
