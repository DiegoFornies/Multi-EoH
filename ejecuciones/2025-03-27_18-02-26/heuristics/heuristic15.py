
def heuristic(input_data):
    """
    Schedules jobs using a heuristic that considers machine load and job completion time.
    Minimizes makespan by prioritizing operations on less loaded machines.
    """
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}  # Earliest time machine is available
    job_completion_times = {job: 0 for job in jobs_data}  # Completion time of each job
    schedule = {}

    for job_id, operations in jobs_data.items():
        schedule[job_id] = []
        for op_idx, op_data in enumerate(operations):
            machines, processing_times = op_data
            op_num = op_idx + 1

            # Find the machine that allows earliest start considering both machine availability and job completion
            best_machine = None
            min_start_time = float('inf')

            for machine_idx, machine in enumerate(machines):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_times[machine_idx] #correct processing time

            start_time = min_start_time
            end_time = start_time + best_processing_time

            # Update machine availability and job completion time
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time
            
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

    return schedule
