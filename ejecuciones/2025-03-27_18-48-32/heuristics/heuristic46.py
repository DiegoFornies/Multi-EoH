
def heuristic(input_data):
    """Heuristic for FJSSP: Random assignment with feasibility check."""
    import random

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id, operations in jobs_data.items():
        schedule[job_id] = []
        for op_idx, op_data in enumerate(operations):
            machines, times = op_data
            
            # Random machine selection
            available_machines = []
            for i in range(len(machines)):
                available_machines.append((machines[i],times[i]))
            selected_machine_index = random.randint(0, len(available_machines)-1)

            selected_machine = available_machines[selected_machine_index][0]
            processing_time = available_machines[selected_machine_index][1]
            
            # Enforce sequence feasibility and machine feasibility.
            start_time = max(machine_available_times[selected_machine], job_completion_times[job_id])
            
            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': selected_machine,
                'Start Time': start_time,
                'End Time': start_time + processing_time,
                'Processing Time': processing_time
            })
            
            # Update available and completion times
            machine_available_times[selected_machine] = start_time + processing_time
            job_completion_times[job_id] = start_time + processing_time

    return schedule
