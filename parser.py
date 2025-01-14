import paramiko
import os

credentials_file = 'servers.txt'

laravel_base_path = '/var/www'

output_dir = "env_files"
os.makedirs(output_dir, exist_ok=True)

def get_env_files(host, username):
    try:
        print(f"Connecting to {host}...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, timeout=10)
        command = f"find {laravel_base_path} -type f -name '.env'"
        stdin, stdout, stderr = client.exec_command(command)
        find_output = stdout.read().decode('utf-8')
        find_errors = stderr.read().decode('utf-8')
        if find_errors:
            print(f"Find command errors on {host}:\n{find_errors}")

        env_files = find_output.strip().split('\n')
        if env_files and env_files[0]:  
            for file_path in env_files:
                absolute_path = os.path.join('/', file_path.strip().lstrip("./"))
                stdin, stdout, stderr = client.exec_command(f"cat {absolute_path}")

                env_content = stdout.read().decode('utf-8')
                cat_errors = stderr.read().decode('utf-8')

                if env_content:
                    folder_name = os.path.basename(os.path.dirname(absolute_path))
                    local_file_name = f"{host}.{folder_name}.env".replace("/", "_")
                    local_file_path = os.path.join(output_dir, local_file_name)

                    with open(local_file_path, "w") as local_file:
                        local_file.write(env_content)
                        print(f"Saved .env file to {local_file_path}")
                elif cat_errors:
                    print(f"Error reading {absolute_path} on {host}:\n{cat_errors}")
                else:
                    print(f"{absolute_path} on {host} is empty or not accessible.")
        else:
            print(f"No .env files found in {laravel_base_path} on {host}.")

        client.close()
    except Exception as e:
        print(f"Error connecting to {host}: {e}")

with open(credentials_file, 'r') as file:
    for line in file:
        if '@' in line:
            username, host = line.strip().split('@')
            get_env_files(host, username)
