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

