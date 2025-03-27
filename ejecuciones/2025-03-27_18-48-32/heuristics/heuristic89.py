
def heuristic(input_data):
    """Heuristic for FJSSP: Shortest Processing Time (SPT) and earliest available machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}

    for job_id in jobs:
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            # Sort possible machines by processing time (SPT)
            machine_times = sorted([(possible_machines[i], possible_times[i]) for i in range(len(possible_machines))], key=lambda x: x[1])

            best_machine = None
            min_start_time = float('inf')

            # Choose machine with shortest processing time and earliest available time
            for machine_id, processing_time in machine_times:
                start_time = max(machine_available_times[machine_id], current_time)
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine_id
                    best_processing_time = processing_time

            start_time = max(machine_available_times[best_machine], current_time)
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = end_time
            current_time = end_time

    return schedule
