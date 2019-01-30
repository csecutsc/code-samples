# Continuous Deployment(CD) Seminar

## Pre-requisites:
Note: Docker made it super easy now to get both Docker and Kubernetes in a single
install, if your machine supports it and you are on Windows or OSX
go with Option 1 for your OS
### Windows:
**Note: If you want to run windows containers such as .NET Core web applications go with Option 1**
#### Windows 10 Pro/Windows Server 2019 (Hyper-V enabled):
1. Docker-for-Windows [Download](https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe)
#### Windows XP/7/8/10 Home / Server 2016:
1. chocolatey [Install](https://chocolatey.org/install)
2. Docker Toolbox for Windows [Download](https://download.docker.com/win/stable/DockerToolbox.exe)<br/>
Note: During Docker toolbox install, keep the following options checked Docker Client for windows, 
Docker Machine for Windows, Virtualbox, everything else should be unchecked
3. minikube and kubectl<br/>
`choco install minikube kubernetes-cli`<br/>
Note: Open cmd with admin rights when installing chocolatey and during `choco install <package-name>`

### Linux:
_*By far the easiest install*_
1. Docker for Linux [Install](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
2. Snap Daemon (skip if you have Ubuntu Desktop>=16.04) [install](https://docs.snapcraft.io/installing-snapd/6735)
3. microk8s(basically minikube but with more features and easier teardown)<br/>
`sudo snap install microk8s --classic`
4. kubectl<br/>
`snap alias microk8s.kubectl kubectl`

### OSX:
### Use Kubernetes on Docker-on-Mac:
1. Docker-on-Mac [Download](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
#### Use minikube:
1. Docker Toolbox for Mac [Download](https://download.docker.com/mac/stable/DockerToolbox.pkg)<br/>
Note: During Docker toolbox install, keep the following options checked Docker Client, 
Docker Machine, Virtualbox, everything else should be unchecked
2. Homebrew [Install](https://brew.sh/)
3. minikube<br/>
`brew cask install minikube`
4. kubectl<br/>
`brew install kubernetes-cli`
## Demo
Now that we are all setup, we are now going to deploy a sudoku solver
server[(Link)](https://hub.docker.com/r/bhowmikp/sudoku-solver-server) made by our site reliability engineer Prantar 

1. 

