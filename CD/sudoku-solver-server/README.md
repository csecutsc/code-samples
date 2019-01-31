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
2. Docker Toolbox for Windows [Install](https://docs.docker.com/toolbox/toolbox_install_windows/)<br/>
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
1. Docker Toolbox for Mac [Download](https://docs.docker.com/toolbox/toolbox_install_mac)<br/>
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

1. Verify your kubernetes cluster is up and running
    ````cmd
    λ minikube status
    λ minikube start
    ````
2. Check if cluster is running
    ```cmd
    λ kubectl get all -o wide
    ```
3. Now to define our `config.yaml` file with the following
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: sudoku-solver-server-demo-service
      labels:
        app: sudoku-solver-server-demo
    spec:
      type: NodePort
      ports:
        - port: 8000
          nodePort: 30100
          protocol: TCP
      selector:
        app: sudoku-solver-server-demo
    ---
    apiVersion: autoscaling/v2beta1
    kind: HorizontalPodAutoscaler
    metadata:
      name: sudoku-solver-server-demo-autoscaler
      labels:
        app: sudoku-solver-server-demo
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: sudoku-solver-server-demo-deployment
      minReplicas: 1
      maxReplicas: 10
      metrics:
        - type: Resource
          resource:
            name: cpu
            targetAverageUtilization: 10
        - type: Resource
          resource:
            name: memory
            targetAverageValue: 1000Mi
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: sudoku-solver-server-demo-deployment
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: sudoku-solver-server-demo
      template:
        metadata:
          labels:
            app: sudoku-solver-server-demo
        spec:
          containers:
            - name: sudoku-solver-server-demo-node
              image: bhowmikp/sudoku-solver-server
              ports:
                - containerPort: 8000
    ```

4. Or we can apply the config directly from git which is a nice
feature:
```
kubectl create -f 
```