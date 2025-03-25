
def heuristic(input_data):
    """Heuristic using Shortest Processing Time (SPT) and Earliest Due Date (EDD)."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    job_due_dates = {} # Simulate due dates; can be replaced with actual due dates if available.

    #Estimate due dates based on total processing time of each job.
    for job_id in jobs:
      total_processing_time = 0
      for operation in jobs[job_id]:
        total_processing_time += min(operation[1]) #Considering shortest processing time
      job_due_dates[job_id] = total_processing_time * 2 # Due date is twice the estimated processing time.
    
    # Sort jobs based on EDD.
    sorted_jobs = sorted(jobs.keys(), key=lambda job_id: job_due_dates[job_id])

    for job_id in sorted_jobs:
        schedule[job_id] = []
        for operation_index, operation in enumerate(jobs[job_id]):
            machines = operation[0]
            processing_times = operation[1]

            #SPT: Choose machine with shortest processing time for the current operation.
            best_machine = None
            min_processing_time = float('inf')
            
            for i, machine in enumerate(machines):
                if processing_times[i] < min_processing_time:
                    min_processing_time = processing_times[i]
                    best_machine = machine

            # Schedule the operation
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + min_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': min_processing_time
            })

            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
