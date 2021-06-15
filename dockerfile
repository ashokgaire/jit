FROM python:latest

# copy and install required dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


#copy and run  main file
COPY jit jit
RUN chmod +x jit



