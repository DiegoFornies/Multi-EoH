
def heuristic(input_data):
    """
    Heuristic for FJSSP using Shortest Processing Time (SPT) and earliest available machine.
    Sorts operations by shortest average processing time across available machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of all operations with job and operation index
    all_operations = []
    for job, operations in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations):
            # Calculate average processing time
            avg_time = sum(times) / len(times)
            all_operations.append((job, op_idx, machines, times, avg_time))

    # Sort operations by shortest average processing time
    all_operations.sort(key=lambda x: x[4])

    for job, op_idx, machines, times, _ in all_operations:
        # Find the earliest available machine among the possible machines
        best_machine = None
        min_start_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_processing_time = times[i]
        
        if job not in schedule:
          schedule[job] = []
        start_time = max(machine_available_time[best_machine], job_completion_time[job])

        # Update schedule
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = start_time + best_processing_time
        job_completion_time[job] = start_time + best_processing_time

    return schedule
