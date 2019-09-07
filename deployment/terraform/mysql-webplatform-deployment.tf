resource "kubernetes_deployment" "webplatform_mysql_deployment" {


  metadata {
    namespace = "${var.deployment_namespace}"
    name = "webplatform-mysql-deployment"
    labels { run = "webplatform-mysql" }
  }

  spec {
    replicas = 1
    selector {
      match_labels { run = "webplatform-mysql" } }

    template {
      metadata {
        labels { run = "webplatform-mysql" }
      }

      spec {
        image_pull_secrets = [ { name = "nexus-creds" } ]

        container {
          image = "fsadykov/centos_mysql"
          name  = "webplatform-mysql-container"

          env { name = "MYSQL_USER"     value = "${var.mysql_user}"}
          env { name = "MYSQL_DATABASE" value = "${var.mysql_database}"}

          env_from {
            secret_ref {
              name = "${kubernetes_secret.webplatform_secret.metadata.0.name}"
            }
          }
        }
      }
    }
  }
}
