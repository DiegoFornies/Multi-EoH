
def heuristic(input_data):
    """FJSSP heuristic: Earliest start, load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_loads = {m: 0 for m in range(n_machines)}

    for job_id in jobs:
        schedule[job_id] = []
        job_completion_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            earliest_start_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time)

                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
                elif start_time == earliest_start_time and (best_machine is None or machine_loads[machine] < machine_loads[best_machine]):
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = max(machine_available_time[best_machine], job_completion_time)
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            machine_loads[best_machine] += best_processing_time
            job_completion_time = end_time

    return schedule
