
def heuristic(input_data):
    """Combines SPT and least-loaded machine for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    eligible_operations = {}
    for job_id, operations in jobs.items():
        eligible_operations[job_id] = 0

    scheduled_operations = 0
    total_operations = sum(len(ops) for ops in jobs.values())

    while scheduled_operations < total_operations:
        available_operations = []
        for job_id, op_index in eligible_operations.items():
            if op_index < len(jobs[job_id]):
                available_operations.append((job_id, op_index))

        if not available_operations:
            break

        best_operation = None
        best_machine = None
        earliest_start_time = float('inf')
        shortest_processing_time = float('inf')

        for job_id, op_index in available_operations:
            machines, times = jobs[job_id][op_index]
            
            # Find the machine with the earliest available time, considering machine load
            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                processing_time = times[i]
                
                if start_time < earliest_start_time or (start_time == earliest_start_time and processing_time < shortest_processing_time):
                    earliest_start_time = start_time
                    shortest_processing_time = processing_time
                    best_operation = (job_id, op_index)
                    best_machine = machine
                    best_processing_time = processing_time

        if best_operation:
            job_id, op_index = best_operation

            if job_id not in schedule:
                schedule[job_id] = []

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id]) # Redundant
            end_time = start_time + best_processing_time
            
            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            eligible_operations[job_id] += 1
            scheduled_operations += 1

    return schedule
