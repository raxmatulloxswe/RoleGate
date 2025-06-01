# RoleGate
User authentication is handled via JWT.  
Role-based permissions system enables assigning different access levels to users.  

# Setup
```bash
git clone https://github.com/raxmatulloxswe/RoleGate.git
```

```python
python3 -m venv venv
source venv/bin/activate      
venv\Scripts\activate         
pip install -r requirements.txt
```

* ```
  cp env.example .env
  ```
* ```
  migrate
  ```
* ```
  runserver
  ```
 
# with Docker-Compose
  * ```
    docker-compose up --build
    ```
    
