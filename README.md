A simple console EPP client. It sends requests and prints a readable summary of server response to the console.

## Running
Clone the repo and fill config file with your login and password. Then add client.pem and client.key files with certificate and private key respectively. Then run the app.py file.

## Supported commands:

### Domain Operations
- `domain:check`  
- `domain:info`  
- `domain:create`  
- `domain:delete`  
- `domain:renew`  
- `domain:update`  
### Host Operations
- `host:check`  
- `host:info`  
- `host:create`  
- `host:delete`  
- `host:update`  
### Contact Operations
- `contact:check`
- `contact:info`  
- `contact:create`  
- `contact:delete`  
- `contact:update`  

Each operation parses the EPP XML server response and prints a readable summary to the console.
