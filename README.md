# Basic CRUD API  
  
Created for show my skills in Python + Quart.  
  
## Running  
  
Copy repository:  
```
git clone https://github.com/YAndrii27/ZeroAPI
```
Change directory to clonned repository:  
```
cd ZeroAPI
```
Install dependencies:
```
poetry install
```
Go to main work directory:
```
cd zeroapi
```
Run server:
```
poetry run hypercorn --bind localhost:8080 main:app   
```  
Open your browser and go to docs at localhost:8080/docs (replace localhost with your host adress in case you are running this on server)
