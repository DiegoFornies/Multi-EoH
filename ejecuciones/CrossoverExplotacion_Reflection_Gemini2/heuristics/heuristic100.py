
def heuristic(input_data):
    """
    Schedules jobs, balancing makespan, separation, and machine load
    by incorporating lookahead and simulated annealing.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    import random
    temperature = 100  # Initial temperature for simulated annealing
    cooling_rate = 0.005  # Cooling rate for simulated annealing
    
    def calculate_makespan(current_schedule):
         completion_times = {}
         for job in current_schedule:
            if current_schedule[job]:
                completion_times[job] = current_schedule[job][-1]['End Time']
         return max(completion_times.values()) if completion_times else 0

    def calculate_total_idle_time(current_schedule, input_data):
        """Calculates the total idle time between operations in the same job."""
        total_idle_time = 0
        for job_id in range(1, input_data['n_jobs'] + 1):
            job_schedule = current_schedule.get(job_id, [])
            if len(job_schedule) > 1:
                for i in range(len(job_schedule) - 1):
                    idle_time = job_schedule[i + 1]['Start Time'] - job_schedule[i]['End Time']
                    total_idle_time += idle_time
        return total_idle_time

    def calculate_machine_load_imbalance(current_schedule, input_data):
        """Calculates the imbalance in machine load."""
        machine_completion_times = {m: 0 for m in range(input_data['n_machines'])}
        for job_schedule in current_schedule.values():
            for operation in job_schedule:
                machine = operation['Assigned Machine']
                machine_completion_times[machine] = max(machine_completion_times[machine], operation['End Time'])
        
        if machine_completion_times:
            max_completion_time = max(machine_completion_times.values())
            total_load = sum(machine_completion_times.values())
            avg_load = total_load / input_data['n_machines'] if input_data['n_machines'] > 0 else 0
            
            imbalance = sum([(load - avg_load)**2 for load in machine_completion_times.values()])
            
            return imbalance
        else:
            return 0
        
    def objective_function(current_schedule, input_data):
        """Combines makespan, separation, and balance into a single objective."""
        makespan = calculate_makespan(current_schedule)
        separation = calculate_total_idle_time(current_schedule, input_data)
        balance = calculate_machine_load_imbalance(current_schedule, input_data)
        
        # Weighted combination of objectives
        weight_makespan = 1
        weight_separation = 0.05
        weight_balance = 0.02
        
        return weight_makespan * makespan + weight_separation * separation + weight_balance * balance
    
    while ready_operations:
        best_job, best_op_index = None, None
        best_machine = None
        best_start_time = float('inf')
        best_end_time = float('inf')
        best_processing_time = float('inf')
        
        current_objective = objective_function(schedule, input_data)
        
        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]
            
            for machine_id, processing_time in zip(machines, times):
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                end_time = start_time + processing_time

                # Create a temporary schedule to test the potential assignment
                temp_schedule = {k: v[:] for k, v in schedule.items()} # Deep copy

                temp_schedule[job_id].append({
                    'Operation': op_index + 1,
                    'Assigned Machine': machine_id,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })
                
                temp_objective = objective_function(temp_schedule, input_data)

                # Simulated Annealing: Accept worse solutions with some probability
                delta = temp_objective - current_objective
                if delta < 0 or random.random() < (temperature / 100):
                    if start_time < best_start_time:
                        best_job, best_op_index = job_id, op_index
                        best_machine = machine_id
                        best_start_time = start_time
                        best_end_time = end_time
                        best_processing_time = processing_time

        if best_job is not None:
            job_id, op_index = best_job, best_op_index
            best_machine_id = best_machine

            machine_available_times[best_machine_id] = best_end_time
            job_completion_times[job_id] = best_end_time
            machine_workload[best_machine_id] += best_processing_time

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine_id,
                'Start Time': best_start_time,
                'End Time': best_end_time,
                'Processing Time': best_processing_time
            })

            ready_operations.remove((job_id, op_index))

            if op_index + 1 < len(jobs_data[job_id]):
                ready_operations.append((job_id, op_index + 1))

        temperature *= (1 - cooling_rate)  # Cool the temperature

    return schedule
