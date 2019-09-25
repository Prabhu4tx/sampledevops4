Kubernetes Cluster Architecture
 ETCD for beginners
 ETCD in kubernetes
 Kube-api server
 controller Managers
 kube scheduler
 Kubelet
 Kube proxy
 Different components
 kube-apiserver
controller Manager

Below are the components of master
ETCD
what is etcd
key-value store
operate etcd

ETCD : etcd is a distributed key-value store that is simple,secure and fast
key-value store :
  install etcd
  1) download binaries
  2) extract
  3)etcd service(./etcd)
    default port is 2379
  To store key value in etcd
  ./etcdtl set key1 value1
  Steps for kubernetes:
  1) Authenticate User
  2) Validate request
  3)Retrieve data
  4)update etcd
  5) Scheduler

Kubectl commands
to create a pod
kubectl run nginx --image=nginx --generator=run-pod/v1
Replicaset:
 kubectl create -f replicaset-definition.yml
 kubectl get replicaset
 kubectl delete replicaset myapp-replicaset
 kubectl replace -f replicaset-definition.yml
 kubectl scale -replicas=6 -f replicaset-definition.yml

Services:
  Nodeport
  ClusterIP'
  Load Balancer
  NodePort: a service can map up by a port to node and port to service
 Nodeport(30008)-->service(80) -->pod(80)

Taint and Tolerant
Taint is for node
Tolerant is for pod
By Default Master is set as Taint 
kubectl taint nodes node01 key=value:taint-effect
three type of taint-effect
1)NoSchedule
2)PreferNoSchedule
3)Noexecute
kubectl taint nodes node1 app=blue:NoSchedule

e.g) Tolerantions syntax in pod
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: nginx-controller
    image: nginx
  tolerations:
  - key:"app"
    operator:"Equal"
    value:"blue"
    effect:"NoSchedule"
===========================
Node Selector:
 The concept of node is to assign a pod to particular using selector and mapping the label of particular node with key:value mapping
 e.g)
 Node changes
 ==============
 kubectl label node <nodename> size=large
  and in the pod template
  pod level changes
    nodeSelector:
        size: large
 Node Affinity:
 ==============================
   pods are hosted on particular node
   Using Node selector we cannot use the condition such as Large or Medium or Not small
Node Affinity provide the feature for assign a pod in a particular node
 
 under pod spec:
   affinity:
     nodeAffinity
       requiredDuringSchedulingIgnoreDuringExecution:
         nodeSelectorTerms:
         - matchExpressions:
           - key: size
              operator: In
             values:
              - Large
              - Medium
              
  Node Affinity Types:
  Available
  requiredDuringSchedulingIgnoredDuringExecution
  prefferedDuringSchedulingIgnoredDuringExecution
  
  planned:
  requireDuringSchedulingRequiredDuringExecution
  preferredDuringSchedulingRequiredDuringExecution
              
   Troubleshooting steps in Kubernetes
   1) Application failure
   2) Worker Node failure
   3)Control Plane failure
   
   
   1) Application failure
   user use to report the application failure
   a)check service status
   if it is a web application, try to access the url with nodeport
   e.g) curl http://web-service-ip:node-port
   b)Check pod
   c)check logs web
   kubectl logs -f web --previous
   Check dependent application
   
  Use case:
  User ----30081(nodeport/8080(targetport)----> web service ---------> webapp-mysql(8080)---------mysqlservice(3306)----> mysql
  
   
   
   
   
   
       
       
       
       
       
        

