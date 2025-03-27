
def heuristic(input_data):
    """FJSSP heuristic: Random machine selection with priority."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    import random

    for job_id in jobs:
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]
            
            # Prioritize machine with shortest processing time
            machine_times = {}
            for machine in possible_machines:
                 machine_times[machine] = possible_times[possible_machines.index(machine)]

            # Sort machines by processing time
            sorted_machines = sorted(machine_times.items(), key=lambda item: item[1])
            
            # Select the machine
            best_machine = sorted_machines[0][0]

            processing_time = possible_times[possible_machines.index(best_machine)]
            start_time = max(machine_available_time[best_machine], current_time)
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            current_time = end_time

    return schedule
