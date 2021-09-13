  
FROM gitpod/workspace-full:latest

# If youi need a GUi, use this:
# FROM gitpod/workspace-full-vnc   

RUN echo "alias ll='ls -lrta'" >> ~/.bashrc
RUN echo "export PIP_USER=false" >> ~/.bashrc