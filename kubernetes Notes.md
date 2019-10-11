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
  
   Steps for maintanance in kubernetes (Blue green approach)
   1) first check all the nodes are available in the kubernetes cluster
   2) kubectl get nodes
   3) check all the application running on the nodes e.g) web 2)mysql 3)python flask
     kubectl get pods --all-namespaces
    4) Remove the particular node for maintance or apply the patch 
       kubectl drain node name<node01> --ignore-daemonsets
 Check the nodes now by executing kubectl get nodes
 kubectl get nodes
NAME      STATUS                     ROLES     AGE       VERSION
master    Ready                      master    10m       v1.11.3
node01    Ready,SchedulingDisabled   <none>    9m        v1.11.3
node02    Ready                      <none>    9m        v1.11.3
node03    Ready                      <none>    9m        v1.11.3
 
 7) Check what are the applicatons are running on the nodes now
    you will get to know particular node will be down and pod are assigned to other nodes
  8) All the patches are applied to node01 
     now execute kubectl uncordon node01
     master $ kubectl get nodes
NAME      STATUS    ROLES     AGE       VERSION
master    Ready     master    16m       v1.11.3
node01    Ready     <none>    16m       v1.11.3
node02    Ready     <none>    16m       v1.11.3
node03    Ready     <none>    16m       v1.11.3
 9) Check now how many pods are assigned to node01
    kubectl get pods -o wide
 10) why we are not scheduling any to kubernetes master
   kubectl describe node master
 11) when we bring down nodes for maintance make sure application have replica .if there is same application pod is not running then we need use kubectl drain node02 --force --ignore-daeomensets
 master $ kubectl get nodes
NAME      STATUS                     ROLES     AGE       VERSION
master    Ready                      master    35m       v1.11.3
node01    Ready                      <none>    35m       v1.11.3
node02    Ready,SchedulingDisabled   <none>    35m       v1.11.3
node03    Ready                      <none>    35m       v1.11.3
 =============
 
 kubectl software version
 v 1.11.13
 
 1 --> major
 alpha --> it is kind of bugfix version will be there
 beta --> this is all kind of bugfixed version and ready to use
 package of various components
 1)Kube-apiserver: v:13.4
 2)control-manager:v1.13.4
 3)Kube-scheduler:v1.13.4
 4)kubelet:v1.13.4
 
 5)kube-proxy::v1.13.4
 6)kubectl: 1.13.4
 7)etcd cluster : v3.2.18
 8)coreDNS:1.1.3
 
     =========================
SSL Certificate in Kubernetes
Generate key
we use openssl
1) Generate keys
2) Certificate signing request
3)Sign certificate

certificate signing details
step1: openssl genrsa -out ca.key 2048
step 2: openssl genrsa -out admin.key 2048
step 3:
 admin.csr
 openssl req -new -key admin.key -subj \ " /CN=kube-admin" -out admin .csr
 
 sign certificate
 openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt
 
 kube scheduler certificate
 WE need to create certificate for admin as admin.crt and admin.key,
 scheduler.crt and scheduler.key,controller-manager.crt and controller-manager.key
, controllermanager.crt and controller-manager.key,kube-proxy.crt and kube-proxy.key
  
  api server-kubelet-client.crt , apiserver-kubelet-clinet.key
  apiserver-etcd-client.crt , apiserver-etcd-client.key for Kube-api server
  
  for kubelet server as kubelet-client.crt and kubelet-client.key are for kubelet server
  
  curl https://kube-apiserver:6443/api/v1/pods \
      --key admin.key --cert admin.crt
      --cacert ca.crt
      
   WE will create kube-config.yaml
   apiVersion: v1
   clusters:
   - cluster:
       certificate-authority: ca.crt
       server: https://kube-apiserver:6443
     name: kubernetes
    

kube API server:
we have 2 certs 1) apiserver.crt  amnd apiserver.key
use openssl command
openssl req -new -key apiserver.key -subj \
"CN=kube-apiserver" -out apiserver.csr -config openssl.cnf
  apiserver.csr
  openssl.conf 
  [req]
   req_extensions = v3_req
   [ v3_req ]
   basicConstraints = CA:FALSE
   keyUsage = nonRepudiation
   subjectAltName = @alt_names
   [alt_names]
   DNS.1 = kubernetes
   DNS.2 = kubernetes.default
   DNS.3 = kubernetes.default.svc
   DNS.4 = kubernetes.default.svc.cluster.local
   IP.1 = 10.96.0.1
   IP.2 = 172.17.0.87
openssl x509 -req -in apiserver.csr \ 
-CA ca.crt -CAkey ca.key -out apiserver.crt



Client Certificate for clients
1) admin
    admin.crt
    admin.key
2) kube-Scheduler
    scheduler.crt
    scheduler.key
3) kube-controller-manager:
    controller-manager.crt
    controller-manager.key
4) kube-proxy
    kube-proxy.crt
    kube-proxy.key
5) Kube-api server
    apiserver-kubelet-client.crt
    apiserver-kubelet-client.key
    apiserver-etcd-client.crt
    apiserver-etcd-client.key
 6) Kubelet Server
     kubelet-client.crt
      kubelet-client.key
      
      
      =======================================
      
      
      Server Certificate for servers:
    1)  ETCD server:
      etcdserver.crt
      etcdserver.key
     2) apiserver:
      apiserver.crt
      apiserver.key
      3) Kubelet Server:
      
      kubelet.crt
      kubelet.key
      
      ====================================================
      
 admin
           ====== kubeapi-server =======> etcd server
 
 scheduler 
 
 kubecontrooller
 Kube-proxy                                 kubelet server


Procedure for cert creation
1) Generate key:
   openssl genrsa -out admin.key 2048
   admin.key
2) openssl req -new -key admin.key -subj \
     "/CN=kube-admin" -out admin.csr
     output =admin.csr
  3) openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt
    output = admin.crt
 
 All the component required ca.crt certificate  in kubernetes
 
 
 etcd server:
 
 etcd-server
 etcdpeer1.crt etcdpeer1.key
 cat etcd.yaml
 - etcd
    - -- advertise-client-urls=https://127.0.0.1:2379
    - --key-file=/path-to-certs/etcdserver.key
    - --cert-file=/path-tocerts/etcdserver.crt
    - --client-cert-auth=true
    - --data-dir=/var/lib/etcd
    - --initial-advertise-peer-urls=https://127.0.0.1:2380
    - --initial-cluster=master=https://127.0.0.1:2380
    - --listen-client-urls=https://127.0.0.1:2379
    - --listen-peer-urls=https://127.0.0.1:2380
    - --name=master
    - --peer-cert-file=/path-to-certs/etcdpeer1.crt
    - --peer-client-cert-auth=true
    - --peer-key-file=/etc/kubernetes/pki/etcd/peer.key
    - --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    - --snapshot-count=10000
    - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
 
 
 Kube-api -server
 kubernetes
 kubernetes.default
 kubernetes.default.svc
 kubernetes.default.svc.cluster.local
 
 
 
 openssl req -new -key apiserver.key -subj \
 "/CN=kube-apiserver" -out apiserver.csr -config openssl.cnf
 
 Kubeconfig File
 ===============
 
 kube config consists of 3 section
 1) clusters(developement)
 2) Contexts( Admin@developmet
 3)Users(dev user)
 
 apiVersion: v1
 kind: Config
 clusters:
 - name: development
   cluster:
      certificate-authority: /etc/kubernetes/pki/ca.crt
      certificate-authority-data: 
       server: https://development:6443
       
 contexts:
   - name: Admin@development
     context:
       cluster:
       user: admin
       namespace: dev
 users:
 -name : admin
 user:
    client-certificate: admin.crt
    client-key: admin.key
  
 to view config
 kubectl config view
 
 kubectl config view configfilename
 
 API Groups
         core:
          /api
            |   
            |
            |
            /v1
            |
            |
            |
            |
         | --- -- ---
         |
         namespace   pods       rc
         events      endpoints   nodes
         bindings    PV          PVC
         configmaps   secrets     services
         
         /apis
         
   /apps extensions  /networking.k8.io  /storage /authentication /certificate
                         v1                                         v1
                         
                           networkpolicies                          certificatesigningrequests  
      v1
       deployments 
        list
         get
         create
       replicasets
       statefulsets
   curl http://localhost:6443 -k
       --key admin.key
       --cert admin.crt
       --cacert   ca.crt
       
       kube proxy - enable service between pod 
       kubectl proxy --> access the kubeapi servers
       
       Authorization
        admins 
        any operations can be performed
        1)Node Authorization
        2) Attribute base Authorization
        3) Role based authorization
        4) Webhook
        
        user --> kubeapi --> kubelet (Read -services,end points,nodes,pods)
                                     (write-node status,pod status
                                     
          ABAC : group of user with certain condition
          We will create a policy file .it is difficult to manage
          
        RBAC:
        We will define a role  and create a security user and create a certificate
        standard approach for kubernetes users
        
        Weebhook:
        authorized externally
        open policy agent is a tool
        2 mode (authorization-mode
        AlwaysAllow
        AlwaysDeny
        ========
        
        Networking
        ====
        
        Coredns
        network namespace
        switching
        Routing
        Default gateway
        DNS
        
        Switches
        
        A  switch (network ) B vm
        
        ip link 
        etho0
        ip add addr
        ip route add 
        route
        ip addr add 192.168.1.10/24 dev etho
        ip route add 192.168.1.10/24 via 192.168.2.1
        cat /proc/sys/net/ipv4/ip_forward
        
        DNS :
        ==============
        add ing the hostname in host under /etc/hosts
        192.168.1.11   db
        ping db
        cat /etc/resolv.conf
        nameserver 192.168.1.100
        
        
        Network namespace
        connect namespace via virtual cable
        ip link add verth-red type veth  peer name veth-blue
        ip link set veth-red netsns red
        ip netns exec red arp
        arp
        Linux bridge
        ip link aa v-net0 type bridge
        ip link
        ip link set dev v-net-0 up
        veth -red ---> veth-blue
        ip -n red link
        
        ip link add veth-red type 
        ip link set veth-red ntns red
        
        iplink set veth-blue netns blue
        ip nnetns exec blue ip route add 192.168.1.0/24 via 192.168
        iptables -t nat -A POSTROUTING -s 192..168.15.0/24 
        ipnetns exec blue ping 8.8.8.8
        port forwarding
        iptables -t nat -A PREROUTING
        Docker network
        docker run --network none nginx
        Host Network
        docker run --network host nginx
        Bridge
        docker run nginx
        docker network ls
         ip link
         ip link add dockero type bridge
         ip addr 
         ip netns
         netstat -plnt
         docker inspect 
         docker run -p 8080:80 nginx
         iptables \
            -t nat \
            -A PREROUTING
         
         
iptab;es -t 
bridge add <cid> <ns>
 Container network interface
 bridge program 
 kube-api -6443
 kubelet -10250
 kube-scheduler -10251
 controller -10252
 etcd -2389
 
 pod networking :
 every pod should have an ipaddress
 every pod should be able to communicate with every other pod in the same nodw
 every pod should be ablle to communicate every other pod
 ip link set dev vnet-0
 ip link add 
 
============================================
Kubernetes Cluster design:
Purpose of the cluster
a) learning
b)development
3)Cloud
how many nodes 
what kind of application
Network traffic
Memory

for development & testing
multi-node cluster

Producction application
up to 5000 nodes
15ok pods
200,000 container
100 pods

AWS 6 -10 m3.large 2cpv 7.5 GB

Cloud
:
GKE for GCP
KOPS for AWS
AKS for AZure
=============]

Storage:
High performance

Nodes
Virtual or Physical machine
4 Node Cluster
Master vs Worker node
Linux x89

master node can host workloads

M1                     M2
apiserver              apiserver
controllerManager      controllerManager
scheduler               scheduler 
ETCD                    ETCD

Kubernetes infrastructure:

Turnkey Solutions :                           HOSTED Solutions
Openshift/Cloud Foundary Runtime/Vagrant(1.13)    openshift online /Amazo n Elastic services
1)PROVISION VM                                 Kubernetes as a service
2)Configure Vm                                  provide provision vm
3)Scripts to Deploy Cluster                     install kubernetes
4) Maintain VM yourself                         Provides maintain VM
Kubernetes on AWS using KOPS                    AKS or GKS

https://www.objectif-libre.com/en/blog/2018/07/05/k8s-network-solutions-comparison/
1 master
2 worker node
HA(High Availability) setup

Load Balancer(nginx or HTTP proxy))
M1  portL:6443 Active         M2 Active (6443
apiserver              apiserver
controllerManager      controllerManager
scheduler               scheduler 
ETCD                    ETCD

=========
kube-controller-manager --leader-electtrue
kube-controller-manager --leader-elect-lease-duration 15s
kube-controller-manager --leader-elect-deadline 15

   
M1  portL:6443 Active         M2 Passive(6443
apiserver              apiserver
controllerManager      controllerManager
scheduler               scheduler 
ETCD                    ETCD

ETCD:
2 toplogy
1) part of master node
2) running in a seperate node(lesser risk
===
easier to setup
high risk

ETCD in HA mode
================
ETCD: distributed key-value store that is a simple,secured

key value
{
"name": "prabhu"
distributed
server1-2379(read/write)        server2-2379(read/write)     server3-2389(read/write)

RAFT protocol

Random timer -- send the request will be the leader
if another node didnt get any request by the leader , it will decide between all 3 
1       2       3 
leader
r       w       w 
w        w       down
Quoram 3  = n/2 +1 = 3/2 +1= 2.5 = 2  
Quoram 7  = 5 /2 + 1 = 3.5 = 3

master node should be always odd 

installation steps for ETCD
etcdctl
version 2 and 3 :
export ETCDCTL_API=3

======

kubectl run nginx image=nginx  --port=80  --record
kubectl set image deployment nginx nginx=nginx:1.2
kubectl rollout history deployment nginx
kubectl rollout status deployment nginx
kubectl rollout undo deployment nginx  --to-revision=2 
kubectl autoscale deployment nginx  --cpu-percent=50  -- min=1  -- max 2
kubectl run nginx3  --image=nginx  --requests=cpu=200m  --limits=cpu=300m  --requests=memory=1Gi  --limits=memory=2Gi
kubectl run hello  --schedule=”*/1 * * * *”  --restart=OnFailure  -- image=busybox  -- /bin/sh -c “date; echo Hello from the kubernetes cluster”
kubectl port-forward redis-master-765d459796–258hz 6379:6379 
kubectl get pods redis-master-765d459796–258hz -o yaml
kubectl create secret docker-registry  --dry-run=true registryhttps  --docker-server=https://example.com:5000  --docker-username=username  --docker-password=password --docker-email=docker@docker.com -o yaml
kubectl create secret generic db-user-pass  --from-file=./username.txt  --from-file=./password.txt (echo -n ‘username’ > ./username.txt, echo -n ‘password’ > ./pass)
kubectl get secrets -o yaml
kubectl create secret generic db-pass  --from-literal=username=<username>  --from-lieral=password=<somebase64password>
kubectl top node NODE_NAME
kubectl top pod  --namespace=<namespace>
kubectl top pod POD_NAME  --containers 
kubectl top pod -l name=myLabel 
Kubectl rollout resume deploy/nginx
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep username | awk ‘{print $1}’)


====

Kubernetes installation
step1:
create 5 vm 
3 master 
2 worker
step 2:
setup the ssh-setup  and distribute the public key (master1)to all the vms
Step3:
provision the certificate using openssl 
1) first certificate  
   ca.key -->private
   ca.csr -->public
   ca.crt
2) Generate Admin cert
openssl genrsa -out admin.key 2048
openssl req -new -key admin.key -subj "/CN=admin/O=system:masters" -out
 admin.csr 
 openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out admin.crt
 
 3) Generate certificate for kube-controller manager
   openssl genrsa -out kube-controller-manager.key 2048
   openssl req -new -key kube-controller-manager.key -subj "/CN=system:kube-controller-manager" -out kube-controller-manager.csr
   openssl x509 -req -in kube-controller-manager.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out kubec-controller-manager.crt
   
4) Generate certificate for kube-proxy
openssl genrsa -out kube-proxy.key 2048
openssl req -new -key kube-proxy.key  -subj "/CN=system:kube-proxy" -out kube-proxy.csr
openssl x509 -req -in kube-proxy.csr -CA ca.crt -CAkey ca.key  -CAcreateserial -out kube-proxy.crt

5) Generate certificate for scheduler
openssl genrsa -out kube-scheduler.key 2048 
openssl req -new -key kube-scheduler.key -subj "/CN=kube-scheduler" -out kube-scheduler.csr
openssl x509 -req -in kube-scheduler.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out kube-scheduler.crt

6) Generate certificate for kube-api server
  we will create a openssl.conf  which includes all the details and create the certification
  prabhu4tx@master1 ~]$ cat openssl.conf 
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[req_distinguished_name]
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = kubernetes
DNS.2 = kubernetes.default
DNS.3 = kubernetes.default.svc
DNS.4 = kubernetes.default.svc.cluster.local
IP.1 = 10.96.0.1
IP.2 = 192.168.5.11
IP.3 = 192.168.5.12
IP.4 = 192.168.5.30
IP.5 = 127.0.0.1
  openssl genrsa -out kube-apiserver.key 2048
  openssl req -new -key kube-apiserver.key -subj "/CN=kube-apiserver" -out kube-apiserver.csr -config openssl.conf
  openssl x509 -req -in kube-apiserver.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out kube-apiserver.crt -extensions v3_req -extfile openssl.conf
  
  7) Generate certificate for etcd :
   we will create a openssl.conf  which includes all the details and create the certification
   openssl-etcd.conf 
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[req_distinguished_name]
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltname = @alt_names
[alt_names]
IP.1 = 192.168.5.11
IP.2 = 192.168.5.12
IP.3 = 127.0.0.1
  
   openssl genrsa -out etcd-server.key 2048
   openssl req -new -key etcd-server.key -subj "/CN=etcd-server" -out etcd-server.csr -config openssl-etcd.conf
   openssl x509 -req -in etcd-server.csr -CA ca.crt -CAkey ca.key -CAcreateserial  -out etcd-server.crt -extensions v3_req -extfile openssl-etcd.conf -days 1000
   
   8) Generate the certificate for serviceaccount
   openssl genrsa -out service-account.key 2048
   openssl req -new -key service-account.key -subj "/CN=service-accounts" -out service-account.csr
   openssl x509 -req -in service-account.csr -CA ca.crt -CAkey ca.key -CAcreateserial  -out service-account.crt -days 1000
   
  


   
   
 









































         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
        
         
         











 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 




   
   
   

       
       
       
       
       
        

