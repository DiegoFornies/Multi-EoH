
def heuristic(input_data):
    """Dynamically chooses between SPT and least loaded machine based on operation."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            # SPT-Least Loaded Combination Selection
            best_machine = None
            best_processing_time = float('inf')
            
            if len(job_operations) - 1 > operation_index: #if it's not the last operation in a job
              least_loaded_machine = min(possible_machines, key=lambda m: machine_load[m])
              for i in range(len(possible_machines)):
                  machine = possible_machines[i]
                  processing_time = possible_times[i]
                  if machine == least_loaded_machine:
                    best_machine = machine
                    best_processing_time = processing_time
                    break
            else: #Last operation of job, use SPT for minimal makespan.
              for i in range(len(possible_machines)):
                  machine = possible_machines[i]
                  processing_time = possible_times[i]
                  if processing_time < best_processing_time:
                      best_machine = machine
                      best_processing_time = processing_time

            # Schedule operation to the best machine found
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job states
            machine_available_times[best_machine] = end_time
            machine_load[best_machine] += best_processing_time
            job_completion_times[job_id] = end_time

    return schedule
