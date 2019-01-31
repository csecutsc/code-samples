# Continuous Deployment(CD) Seminar

## Intro:

## Pre-requisites:
Note: Docker made it super easy now to get both Docker and Kubernetes in a single
install, if your machine supports it and you are on Windows or OSX
go with Option 1, I will be personally using Option 2 on Windows as
I need virtualbox for my other development tasks.
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

### If you're using Minikube/microk8s:
Note: If you are on ubuntu instructions listed above the following
commands should be the same except `minikube` would be replaced by
`microk8s`
1. Verify your kubernetes cluster is up and running
    ````cmd
    λ minikube status
    λ minikube start
    ````
2. Check if cluster is running
    ```cmd
    λ kubectl get all -o wide
    ```
3.  Install metrics-server and dashboard for autoscaling metrics
and easier cluster management
    ```cmd
    λ minikube addons install metrics-server dashboard
    ```
    In Ubuntu using microk8s it's a bit different
    ```cmd
    λ microk8s.enable metrics-server dashboard
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
    λ kubectl create -f https://raw.githubusercontent.com/csecutsc/code-samples/master/CD/sudoku-solver-server/config.yaml
    ```

5. Now within a few seconds with the magic of Kubernetes you will have a fully
deployed application which auto-scales depending on cpu utilization metrics from
Grafana(could use Prometheus too or your custom metrics pipeline)

6. View the deployment as it happens by either doing:
    ```cmd
    λ watch -n 2 kubectl get all -o wide
    ```
    or if you want a more visual experience
    ```cmd
    λ minikube dashboard
    ```
    and click on the `Overview` tab on the left menu

### If you're using Docker-on-Windows or Docker-on-Mac:
Now remember when I told you option 1 is the easiest, well I kinda lied 
due to time constraints. If you want to see auto horizontal pod scaling 
and web CLI in action you need to install a few addons which normally
ship with Minikube. Such as `metrics-server` and `dashboard`.

1. Install dashboard 
    * Create dashboard deployment
        ```cmd
        λ kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
        ```
    * Get pod name of dashboard
         ```cmd
         λ kubectl get pods — namespace=kube-system
         λ NAME                                       READY STATUS RESTARTS AGE
           kubernetes-dashboard-7798c48646      1/1   Running 0       3m
         ```
         Copy the name of the pod that has the word `dashboard`
     * Now port let's proxy the internal pod which has our dashboard in another terminal
        ```cmd
        λ kubectl port-forward kubernetes-dashboard-7798c48646 8443:8443 — namespace=kube-system
        ```
     * Now open https://localhost:8443/ to verify dashboard loaded, skip authentication
 2. Install metrics-server
    * Follow the docs -> [Docs](https://github.com/kubernetes-incubator/metrics-server)
 3. If you manage to install metrics-server then run `config.yaml` via kubectl, if not just
 use `config-no-autoscale.yaml`
    * If using `config.yaml` run the following command:
        ```
        λ kubectl create -f https://raw.githubusercontent.com/csecutsc/code-samples/master/CD/sudoku-solver-server/config.yaml
        ```
    *  If using `config-no-autoscale.yaml` run the following command:
        ```
        λ kubectl create -f https://raw.githubusercontent.com/csecutsc/code-samples/master/CD/sudoku-solver-server/config-no-autoscale.yaml
        ``` 
## Test
* I have created a test program using go to load test API's using concurrent
requests via goroutines, you can download the compiled executables from the
releases page for your corresponding OS.

* You can test by doing the following on your cluster: 
    ```cmd
    λ kubectl get all -o wide
      NAME                                                        READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
      pod/sudoku-solver-server-demo-deployment-557cbd86d8-bjm49   1/1     Running   0          11m   172.17.0.8   minikube   <none>           <none>
      
      NAME                                        TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE    SELECTOR
      service/kubernetes                          ClusterIP   10.96.0.1      <none>        443/TCP          4h4m   <none>
      service/sudoku-solver-server-demo-service   NodePort    10.102.129.5   <none>        8000:30100/TCP   11m    app=sudoku-solver-server-demo
      
      NAME                                                   READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS                       IMAGES                          SELECTOR
      deployment.apps/sudoku-solver-server-demo-deployment   1/1     1            1           11m   sudoku-solver-server-demo-node   bhowmikp/sudoku-solver-server   app=sudoku-solver-server-demo
      
      NAME                                                              DESIRED   CURRENT   READY   AGE   CONTAINERS                       IMAGES                          SELECTOR
      replicaset.apps/sudoku-solver-server-demo-deployment-557cbd86d8   1         1         1       11m   sudoku-solver-server-demo-node   bhowmikp/sudoku-solver-server   app=sudoku-solver-server-demo,pod-template-hash=557cbd86d8
      
      NAME                                                                       REFERENCE                                         TARGETS                           MINPODS   MAXPODS   REPLICAS   AGE
      horizontalpodautoscaler.autoscaling/sudoku-solver-server-demo-autoscaler   Deployment/sudoku-solver-server-demo-deployment   <unknown>/1000Mi, <unknown>/10%   1         10        1          11m
    
    λ kubectl port-forward service/sudoku-solver-server-demo-service 30100:8000
    [now open a new terminal in the same folder as load_runner]
    λ cd Downloads
    λ load_runner 100 http://localhost:30100/?board=..529.6......753.99...3...8.896.......79.28.......7.9.6...4...5..472......1.692..
    ```
* Voila if everything went well you have just successfully gotten a taste of production deployments

# End Credits
If time permits I want to showcase a video of one of my personal hero's Kelsey Hightower,
 he is the author of some great opensource projects such as [nocode](https://github.com/kelseyhightower/nocode)
 and [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way):<br/><br/>
 [Link to Video](https://youtu.be/kOa_llowQ1c?t=1020)
 
 Lastly thank you CSEC team for organizing this event, special thanks to Brian and Prantar
 for making our production series a success.
 
