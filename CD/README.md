# Continuous Deployment(CD) Seminar

## Pre-requisites:
### Windows:
**Note: If you want to run windows containers such as .NET Core web applications go with Option 1**
#### Windows 10 Pro/Windows Server 2019 (Hyper-V enabled):
1. Docker-for-Windows [Download](https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe)
#### Windows XP/7/8/10 Home / Server 2016:
1. chocolatey [Install](https://chocolatey.org/install)
2. Virtualbox [Download](https://download.virtualbox.org/virtualbox/6.0.4/VirtualBox-6.0.4-128413-Win.exe)
3. minikube and kubectl<br/>
`choco install minikube kubernetes-cli`<br/>
Note: Open cmd with admin rights when installing chocolatey and during `choco install <package-name>`

### Linux:
_*By far the easiest install*_
1. Snap Daemon (skip if you have Ubuntu Desktop>=16.04) [install](https://docs.snapcraft.io/installing-snapd/6735)
2. microk8s<br/>
`sudo snap install microk8s --classic`
3. kubectl<br/>
`snap alias microk8s.kubectl kubectl`

### OSX:
1. Homebrew [Install](https://brew.sh/)
2. minikube<br/>
`brew cask install minikube`
3. kubectl<br/>
`brew install kubernetes-cli`

## Demo
We are now going to deploy a sudoku solver
server made by our site reliability engineer 
Prantar

