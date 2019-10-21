kubectl config set-cluster mycluster --server=https://kubernetes.default --certificate-authority=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
kubectl config set-context mycontext --cluster=mycluster
kubectl config set-credentials myuser --token="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
kubectl config set-context mycontext --user=myuser
kubectl config use-context mycontext
