  
FROM gitpod/workspace-full:latest

# If youi need a GUi, use this:
# FROM gitpod/workspace-full-vnc   

RUN apt-get update -y
RUN apt-get install -y sysvbanner
RUN echo "alias ll='ls -lrta'" >> ~/.bashrc
RUN echo "export PIP_USER=false" >> ~/.bashrc