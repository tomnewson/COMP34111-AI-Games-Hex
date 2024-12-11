import subprocess
import time

def run_game(command):
    start_time = time.time()
    subprocess.run(command)
    end_time = time.time()
    return end_time - start_time

def main():
    num_runs = 10

    # First set of agents
    total_time_1 = 0
    command_1 = ["python3", "Hex.py", "-p1", "agents.Group17.GoodAgent GoodAgent", "-p2", "agents.TestAgents.ValidAgent ValidAgent"]
    for _ in range(num_runs):
        total_time_1 += run_game(command_1)
    average_time_1 = total_time_1 / num_runs

    # Second set of agents
    total_time_2 = 0
    command_2 = ["python3", "Hex.py", "-p1", "agents.Group17.ExploreAgent GoodAgent", "-p2", "agents.TestAgents.ValidAgent ValidAgent"]
    for _ in range(num_runs):
        total_time_2 += run_game(command_2)
    average_time_2 = total_time_2 / num_runs

    # Print results
    print(f"Average time taken to run the first game: {average_time_1:.5f} seconds")
    print(f"Average time taken to run the second game: {average_time_2:.5f} seconds")
    print(f"Difference in average time: {abs(average_time_1 - average_time_2):.5f} seconds")

if __name__ == "__main__":
    main()