# README: Environment Files Fetcher Script

This script fetches `.env` files from remote servers using SSH. It is designed for administrators or developers who need to gather environment files from multiple servers efficiently. The script connects to each server, locates `.env` files under a specified base path, and saves them to a local folder for further use. 🎯📂🚀

---

## Features 🎉✨📑
- Connects to remote servers via SSH.
- Searches for `.env` files in the specified base path on each server.
- Downloads `.env` files and saves them locally with unique filenames.
- Handles errors gracefully, ensuring all accessible `.env` files are retrieved.

---

## Prerequisites 🛠️📦🔐

### Python Requirements 📜🐍🔢
- Python 3.6+

### Dependencies ⚙️📚💻
Install the required dependencies using:
```bash
pip install paramiko
```

### SSH Access 🌐🔑💾
Ensure you have SSH access to the target servers. You must:
1. Have the correct username and hostname for each server.
2. Ensure the SSH keys or passwords are properly configured for seamless access.

---

## Usage 🖥️📂🔍

### 1. Prepare the Input File 📝📋📄
Create a text file (e.g., `servers.txt`) containing server details. Each line should follow this format:
```plaintext
<username>@<hostname>@<base_path>
```

Example:
```plaintext
user1@192.168.1.10@/var/www
user2@remote-server.com@/home/user2
```

### 2. Run the Script 🚀💻🛠️
Execute the script with the following command:
```bash
python3 script.py --parse <input_file> --out <output_folder>
```

#### Parameters:
- `--parse`: Path to the input file containing server details.
- `--out`: Path to the local folder where `.env` files will be saved.

Example:
```bash
python3 script.py --parse servers.txt --out envfiles
```

---

## Output 📤📁✅
- `.env` files from each server are saved in the specified output folder.
- Files are named in the format:
  ```
  <hostname>.<parent_folder>.env
  ```
  Example: `192.168.1.10.www.env`

---

## Error Handling 🛠️❌🔍
- If no `.env` files are found, a message will indicate this for each server.
- Errors during SSH connection or file access are logged to the console.

---

## Example Workflow 🖥️📂📜
1. Create `servers.txt` with the following content:
   ```plaintext
   admin@192.168.1.100@/var/www
   user@10.0.0.2@/home/user
   ```

2. Run the script:
   ```bash
   python3 script.py --parse servers.txt --out envfiles
   ```

3. Check the `envfiles` directory for the downloaded `.env` files.

---

## Notes 📌⚠️🗒️
- Ensure the user running the script has permission to read `.env` files on the remote servers.
- `.env` files should be handled carefully, as they may contain sensitive information.

---

## Troubleshooting 🛠️💡🔧
- **`paramiko.ssh_exception.AuthenticationException`**: Verify your SSH credentials.
- **No `.env` files found**: Ensure the `base_path` is correct and accessible.
- **Script does not terminate**: Use the `dd` function from `utility.py` to debug issues. 🎯📊🕵️
