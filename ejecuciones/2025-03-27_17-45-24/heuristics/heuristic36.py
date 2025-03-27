
def heuristic(input_data):
    """Heuristic: Random machine selection with sequence feasibility."""
    import random

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}

    for job in jobs:
        schedule[job] = []

    for job_id in jobs:
        current_time = 0
        for op_index, operation in enumerate(jobs[job_id]):
            machines, times = operation
            
            # Randomly select a machine
            available_machines = []
            for i in range(len(machines)):
                available_machines.append((machines[i],times[i]))
                
            selected_machine_index = random.randint(0, len(available_machines)-1)
            selected_machine = available_machines[selected_machine_index][0]
            processing_time = available_machines[selected_machine_index][1]
            
            # Ensure operation starts after previous operation in the same job
            start_time = max(current_time, machine_available_time[selected_machine])

            end_time = start_time + processing_time

            operation_data = {
                'Operation': op_index + 1,
                'Assigned Machine': selected_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            }
            schedule[job_id].append(operation_data)

            machine_available_time[selected_machine] = end_time
            current_time = end_time
    return schedule
