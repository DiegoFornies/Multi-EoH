
def heuristic(input_data):
    """Heuristic for FJSSP: Earliest Due Date with machine consideration."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_finish_times = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    operation_count = {j: 0 for j in jobs_data}

    def calculate_due_date(job_id):
        """Estimates due date based on remaining work."""
        remaining_time = 0
        for i in range(operation_count[job_id], len(jobs_data[job_id])):
            remaining_time += min(jobs_data[job_id][i][1])
        return job_finish_times[job_id] + remaining_time

    scheduled_operations = 0
    total_operations = sum(len(ops) for ops in jobs_data.values())

    while scheduled_operations < total_operations:
        available_ops = []
        for job_id in jobs_data:
            if operation_count[job_id] < len(jobs_data[job_id]):
                available_ops.append(job_id)

        if not available_ops:
            break  # No more schedulable operations

        # Prioritize jobs with earliest due dates
        available_ops.sort(key=calculate_due_date)

        for job_id in available_ops:
            op_index = operation_count[job_id]
            machines, times = jobs_data[job_id][op_index]

            best_machine = None
            min_finish_time = float('inf')
            processing_time = None

            # Find best machine for the current operation
            for i, machine in enumerate(machines):
                start_time = max(machine_available[machine], job_finish_times[job_id])
                finish_time = start_time + times[i]

                if finish_time < min_finish_time:
                    min_finish_time = finish_time
                    best_machine = machine
                    processing_time = times[i]
            
            if best_machine is None:
                continue

            start_time = max(machine_available[best_machine], job_finish_times[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available[best_machine] = end_time
            job_finish_times[job_id] = end_time
            operation_count[job_id] += 1
            scheduled_operations += 1

    return schedule
