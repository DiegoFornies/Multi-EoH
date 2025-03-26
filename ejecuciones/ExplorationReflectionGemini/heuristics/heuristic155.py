
def heuristic(input_data):
    """Earliest Due Date (EDD) with machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    schedule = {}
    job_duedates = {}

    # Calculate job due dates (sum of processing times)
    for job_id in range(1, n_jobs + 1):
        total_processing_time = 0
        for operation_data in jobs[job_id]:
            total_processing_time += min(operation_data[1])  # Use shortest processing time
        job_duedates[job_id] = total_processing_time

    # Sort jobs by due date
    sorted_jobs = sorted(job_duedates.items(), key=lambda item: item[1])
    
    current_time = 0

    for job_id, _ in sorted_jobs:
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None
            
            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]
                
                start_time = max(machine_available_times[machine], current_time)
                
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            machine_available_times[best_machine] = min_start_time + best_processing_time
            
            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': min_start_time,
                'End Time': min_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
        current_time = 0 # Reset current time, start each job ASAP.
    return schedule
