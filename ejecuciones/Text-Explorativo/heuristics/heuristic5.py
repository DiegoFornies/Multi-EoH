
def heuristic(input_data):
    """
    A heuristic for the FJSSP minimizing makespan, idle time, and balancing load.
    Assigns operations to machines based on earliest finish time, job order and machine balance.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    machine_assignments = {m: [] for m in range(n_machines)} #Keep the schedule for each machine.

    for job_id in jobs:
        schedule[job_id] = []

    #Operations of each job are scheduled sequentially.
    for job_id, operations in jobs.items():
        for op_idx, operation in enumerate(operations):
            available_machines = operation[0]
            processing_times = operation[1]

            # Find the machine that allows the earliest possible finish time
            best_machine = None
            min_finish_time = float('inf')

            for i, machine_id in enumerate(available_machines):
                processing_time = processing_times[i]
                start_time = max(machine_available_times[machine_id], job_completion_times[job_id])
                finish_time = start_time + processing_time

                if finish_time < min_finish_time:
                    min_finish_time = finish_time
                    best_machine = machine_id
                    best_processing_time = processing_time
                    best_start_time = start_time


            # Schedule the operation on the best machine
            operation_number = op_idx + 1
            schedule[job_id].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            #Update machine and job completion times
            machine_available_times[best_machine] = best_start_time + best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time
            machine_assignments[best_machine].append(job_id)

    return schedule
