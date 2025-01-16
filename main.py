import paramiko
import os
import argparse
from utility import dd

def get_env_files(host, username, output_folder, base_path):
    try:
        print(f"Connecting to {host}...")
        
        
        # Setting up command
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, timeout=10)
        command = f"find {base_path} -type f -name '.env'"

        # Execute command
        stdin, stdout, stderr = client.exec_command(command)
        find_output = stdout.read().decode('utf-8')
        find_errors = stderr.read().decode('utf-8')
        if find_errors:
            print(f"Find command errors on {host}:\n{find_errors}")

        env_files = find_output.strip().split('\n')
        os.makedirs(output_folder, exist_ok=True)


        # Save data in output folder
        if env_files and env_files[0]:  
            for file_path in env_files:

                # Reading content
                absolute_path = os.path.join('/', file_path.strip().lstrip("./"))
                stdin, stdout, stderr = client.exec_command(f"cat {absolute_path}")
                env_content = stdout.read().decode('utf-8')
                cat_errors = stderr.read().decode('utf-8')

                # Writing content
                if env_content:
                    folder_name = os.path.basename(os.path.dirname(absolute_path))
                    local_file_name = f"{host}.{folder_name}.env".replace("/", "_")
                    local_file_path = os.path.join(output_folder, local_file_name)
                    with open(local_file_path, "w") as local_file:
                        local_file.write(env_content)
                        print(f"Saved .env file to {local_file_path}")
                elif cat_errors:
                    print(f"Error reading {absolute_path} on {host}:\n{cat_errors}")
                else:
                    print(f"{absolute_path} on {host} is empty or not accessible.")
        else:
            print(f"No .env files found in {base_path} on {host}.")

        client.close()
    except Exception as e:
        print(f"Error connecting to {host}: {e}")

def main():
    parser = argparse.ArgumentParser(description="A script to parse a file and output results.")
    
    parser.add_argument('--parse', type=str, required=True, help='Input file to parse')
    parser.add_argument('--out', type=str, required=True, help='Output folder')
    
    args = parser.parse_args()
    
    input_file = args.parse
    output_folder = args.out
    
    # Parse username, host, base_path seperated by @
    with open(input_file, 'r') as file:
        for line in file:
            if '@' in line:
                username, host, base_path = line.strip().split('@')
                get_env_files(host, username, output_folder, base_path)
    
    print("Processing completed.")

if __name__ == "__main__":
    main()
