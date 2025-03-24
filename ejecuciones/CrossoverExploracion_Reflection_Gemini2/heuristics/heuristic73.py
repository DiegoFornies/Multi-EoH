
def heuristic(input_data):
    """Schedules operations based on a greedy approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_times = {m: 0 for m in range(n_machines)}
    job_finish_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        for operation_id, operation in enumerate(jobs[job_id]):
            machines, times = operation
            best_machine = -1
            min_finish_time = float('inf')
            best_time = -1

            for i, machine in enumerate(machines):
                available_time = machine_times[machine]
                start_time = max(available_time, job_finish_times[job_id])
                finish_time = start_time + times[i]

                if finish_time < min_finish_time:
                    min_finish_time = finish_time
                    best_machine = machine
                    best_time = times[i]

            start_time = max(machine_times[best_machine], job_finish_times[job_id])
            end_time = start_time + best_time

            schedule[job_id].append({
                'Operation': operation_id + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_times[best_machine] = end_time
            job_finish_times[job_id] = end_time

    return schedule
