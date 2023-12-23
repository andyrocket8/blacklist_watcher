# Watcher application
## Intention
Watcher application is agent application for online parsing of log files and gathering information about malicious IP addresses.

Application reports information about gathered addresses to Blacklist application using Blacklist API.

Blacklist application published on https://github.com/andyrocket8/blacklist_watcher 

## Usage
Application use YAML configuration file
Run application with 
```commandline
python ./src/main.py <config.yaml>
```
Before start install dependencies with poetry dependency manager. File pyproject.toml contains information of deployment modules needed.

## Container deployment
You can deploy application in Docker environment
Dockerfile is located in ./src folder

Build container with 
```
make build
``` 
Deploy with specifying config file in ENV variable CONFIG_FILE
```
docker run --env CONFIG_FILE=/home/core/develop/secure/stuff/file_watcher/config/config.yml -it --rm blacklist-watcher
```
Don't forget to map watched and config file folders

## Config file reference (YAML)
```
# watcher definition. Can serve several watchers, use YAML array for further description
watchers:
    # Watcher group definiton       
    - filename: /home/core/develop/secure/stuff/file_watcher/file.log  # File name for watching
      # Regex pattern for extracting information from log file. Here is Fail2ban regex pattern 
      regex: .*(Ban|Unban).([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*
      # String description to pass in Blacklist API /add and /delete methods 
      agent: Fail2Ban (development)
      # Address position in parsed regex variables
      address_description: 
        tuple_position: 1
      # Event category position in parsed regex variables
      event_description:
        tuple_position: 0
        # Mapping for encoding /add or /delete event. Extracted value mast be mapped into "block" or "unblock" category
        # "block" means /add handler execution, "unblock" - /delete execution  
        event_mapping:
          - event_string: Ban
            event_category: block
          - event_string: Unban
            event_category: unblock
    # Further watcher group definition 
    - ... 

# URI for Blacklist API access (methods are specified in src/core/settings.py) 
blacklist_uri: http://127.0.0.1:8000/blacklist
# Add following parameter if Blacklist application has authorization enabled
blacklist_token: <Blacklist agent token>

# Status file. Application stores tracking information on watched files here  
status_file: /home/core/develop/secure/stuff/file_watcher/status.json

# Logging options 
logging:
   # logging level (ERROR, INFO, WARN, DEBUG) 
   level: DEBUG
   # log file name, specify if you need log file creation
   filename: /home/core/develop/secure/stuff/file_watcher/logs/watcher.log
   # Console logging. Use Yes/No for desired option
   console: Yes
```
 
