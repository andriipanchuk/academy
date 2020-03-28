# your server name goes here
server=https://"$(printenv | grep KUBERNETES_SERVICE_HOST| awk -F '=' '{print $2}')":443
# the name of the secret containing the service account token goes here
ca="$(cat /var/run/secrets/kubernetes.io/serviceaccount/ca.crt | sed 's/-----BEGIN CERTIFICATE-----//g'|  sed 's/-----BEGIN CERTIFICATE-----//g' | base64 --decode)"
token="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
namespace="$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)"

echo "
apiVersion: v1
kind: Config
clusters:
- name: default-cluster
  cluster:
    certificate-authority-data: ${ca}
    server: ${server}
contexts:
- name: default-context
  context:
    cluster: default-cluster
    namespace: default
    user: default-user
current-context: default-context
users:
- name: default-user
  user:
    token: ${token}
" > config
