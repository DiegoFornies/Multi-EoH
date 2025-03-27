
def heuristic(input_data):
    """Heuristic for FJSSP: Random machine selection with makespan consideration."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}

    for job in jobs:
        schedule[job] = []

    import random

    for job_id in jobs:
        for op_index in range(len(jobs[job_id])):
            machines, times = jobs[job_id][op_index]
            
            # Random machine selection
            available_machines_times = list(zip(machines, times))
            chosen_machine_index = random.randint(0, len(available_machines_times) - 1)
            chosen_machine, processing_time = available_machines_times[chosen_machine_index]

            # Makespan consideration: choose the time that minimizes makespan
            start_time = machine_available_time[chosen_machine]
            if op_index > 0:
                start_time = max(start_time, schedule[job_id][-1]['End Time']) # Sequence constraint

            end_time = start_time + processing_time
           
            operation = {
                'Operation': op_index + 1,
                'Assigned Machine': chosen_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            }
            schedule[job_id].append(operation)

            machine_available_time[chosen_machine] = end_time
            
    return schedule
