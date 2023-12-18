import yaml
import socket
import argparse
import time

def load_config(yaml_file):
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def send_file(destination, file_path, max_retries=3):
    for attempt in range(max_retries):
        try:
            with socket.create_connection((destination['address'], destination['port'])) as sock:
                with open(file_path, 'rb') as file:
                    file_content = file.read()
                    sock.sendall(file_content)
                print(f"File sent successfully to {destination['address']}:{destination['port']}")
                return True
        except Exception as e:
            print(f"Error: {e}")
            print(f"Failed to connect to {destination['address']}:{destination['port']}")
            if attempt < max_retries - 1:
                print(f"Retrying in 5 seconds... (Attempt {attempt + 2}/{max_retries})")
                time.sleep(5)
    
    print(f"Max retries reached. File could not be sent to {destination['address']}:{destination['port']}")
    return False

def main():
    parser = argparse.ArgumentParser(description="Send a file to multiple destinations specified in a YAML file.")
    parser.add_argument("-c", "--yamlfile", required=True, help="Path to the YAML configuration file.")
    parser.add_argument("-f", "--sendfile", required=True, help="Path to the file to be sent.")
    args = parser.parse_args()

    config = load_config(args.yamlfile)

    if 'destinations' in config:
        for destination in config['destinations']:
            send_file(destination, args.sendfile)

if __name__ == "__main__":
    main()
