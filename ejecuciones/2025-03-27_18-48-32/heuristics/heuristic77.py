
def heuristic(input_data):
    """Schedules jobs, minimizing makespan and balancing load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in jobs:
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            # Select machine with earliest possible finish time
            best_machine = None
            earliest_finish = float('inf')

            for i, machine in enumerate(possible_machines):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                finish_time = start_time + possible_times[i]

                if finish_time < earliest_finish:
                    earliest_finish = finish_time
                    best_machine = machine

            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            processing_time = possible_times[possible_machines.index(best_machine)]
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
