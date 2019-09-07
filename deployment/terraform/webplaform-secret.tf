resource "kubernetes_secret" "webplatform_secret" {
  metadata {
    name      = "webplatform-secret"
    namespace = "${var.deployment_namespace}"
  }

  data {
    MYSQL_PASSWORD = "${var.webplatform_password}"
    SECRET_KEY     = "${var.webplatform_secret}"
   }

  type = "Opaque"
}
