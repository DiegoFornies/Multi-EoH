
def heuristic(input_data):
    """Schedules jobs minimizing makespan and balancing machine load.
    Combines earliest finish time and SPT with machine load balancing.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            best_machine = None
            min_combined_score = float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available[machine], job_completion[job_id])
                end_time = start_time + processing_time
                # combine machine load and earliest end time
                combined_score = machine_load[machine] + end_time  

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time
                    best_end_time = end_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_end_time,
                'Processing Time': best_processing_time
            })

            machine_load[best_machine] += best_processing_time
            machine_available[best_machine] = best_end_time
            job_completion[job_id] = best_end_time

    return schedule
