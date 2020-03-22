# your server name goes here
server=https://"$(printenv | grep KUBERNETES_SERVICE_HOST| awk -F '=' '{print $2}')":443
# the name of the secret containing the service account token goes here
name=fuchicorp-api-token-mw4wx

ca=$(kubectl get  secret/$name -n tools -o jsonpath='{.data.ca\.crt}')
token=$(kubectl get  secret/$name -n tools -o jsonpath='{.data.token}' | base64 --decode)
namespace=$(kubectl get secret/$name -n tools -o jsonpath='{.data.namespace}' | base64 --decode)

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
