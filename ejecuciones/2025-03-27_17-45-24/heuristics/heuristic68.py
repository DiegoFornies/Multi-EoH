
def heuristic(input_data):
    """Heuristic: SPT with machine preference based on estimated makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Sort jobs by total processing time (SPT)
    job_order = sorted(jobs.keys(),
                       key=lambda job: sum(sum(times) for _, times in jobs[job]))

    for job_id in job_order:
        schedule[job_id] = []
        op_index = 0
        while op_index < len(jobs[job_id]):
            machines, times = jobs[job_id][op_index]

            # Machine Preference: Estimate finish time on each machine
            machine_finish_times = {}
            for machine, time in zip(machines, times):
                machine_finish_times[machine] = max(machine_available_time[machine],
                                                     job_completion_time[job_id]) + time

            # Choose machine with earliest finish time
            best_machine = min(machine_finish_times, key=machine_finish_times.get)
            best_start_time = max(machine_available_time[best_machine],
                                  job_completion_time[job_id])
            best_processing_time = machine_finish_times[best_machine] - best_start_time

            operation = {
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            }
            schedule[job_id].append(operation)

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job_id] = best_start_time + best_processing_time
            op_index += 1
    return schedule
