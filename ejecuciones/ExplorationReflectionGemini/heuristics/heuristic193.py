
def heuristic(input_data):
    """Earliest Due Date (EDD) with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    job_due_dates = {}

    # Assign a random due date for each job, due date is related to total processing time
    for job_id in range(1, n_jobs + 1):
      total_processing_time = 0
      for operation_data in jobs[job_id]:
          total_processing_time += min(operation_data[1]) # take the minimum processing time for estimation
      job_due_dates[job_id] = total_processing_time * 2 # assign due date as double the processing time for example.

    # Jobs are sorted by due date
    sorted_jobs = sorted(job_due_dates.items(), key=lambda item: item[1])
    sorted_job_ids = [job_id for job_id, _ in sorted_jobs]

    for job_id in sorted_job_ids:
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_end_time = float('inf')

            # Prioritize machines with lower load
            machine_load = {}
            for machine in possible_machines:
                machine_load[machine] = machine_available_times[machine]

            sorted_machines = sorted(machine_load, key=machine_load.get) # sort by load

            for machine in sorted_machines:
                machine_index = possible_machines.index(machine)
                processing_time = possible_times[machine_index]

                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_available_times[best_machine] = best_start_time + best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

    return schedule
