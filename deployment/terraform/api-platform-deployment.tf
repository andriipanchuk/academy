resource "kubernetes_deployment" "api_platform_deployment" {

  depends_on = [
    "kubernetes_service_account.webplatform_service_account",
    "kubernetes_deployment.webplatform_mysql_deployment",
    "kubernetes_service.mysql_host",
    "kubernetes_secret.webplatform_secret"
    ]

  metadata {
    namespace = "${var.webplatform_namespace}"
    name = "api-platform-deployment"
    labels { run = "api-platform" }
  }

  spec {
    replicas = 1
    selector {
      match_labels { run = "api-platform" } }

    template {
      metadata {
        labels { run = "api-platform" }
      }

      spec {
        image_pull_secrets = [ { name = "nexus-creds" } ]
        service_account_name = "${kubernetes_service_account.webplatform_service_account.metadata.0.name}"

        container {
          image             = "${var.api_platform_image}"
          name              = "api-platform-container"
          command           = [ "python", "/app/app.py" ]
          image_pull_policy = "Always"

          env { name = "MYSQL_USER"     value = "${var.mysql_user}" }
          env { name = "MYSQL_DATABASE" value = "${var.mysql_database}" }
          env { name = "MYSQL_HOST"     value = "${var.mysql_host}" }

          env { name = "SERVICE_CERT_FILENAME"     value = "/var/run/secrets/kubernetes.io/serviceaccount" }


          env_from {
            secret_ref {
              name = "${kubernetes_secret.webplatform_secret.metadata.0.name}"
            }
          }

          volume_mount {
            mount_path = "/var/run/secrets/kubernetes.io/serviceaccount"
            name = "${kubernetes_service_account.webplatform_service_account.default_secret_name}"
            read_only = true
          }
        }
        volume {
          name = "${kubernetes_service_account.webplatform_service_account.default_secret_name}"
          secret {
            secret_name = "${kubernetes_service_account.webplatform_service_account.default_secret_name}"
          }
        }
      }
    }
  }
}
