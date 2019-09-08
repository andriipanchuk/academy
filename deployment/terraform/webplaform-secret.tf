resource "kubernetes_secret" "webplatform_secret" {
  metadata {
    name      = "webplatform-secret"
    namespace = "${var.deployment_environment}"
  }

  data {
    MYSQL_PASSWORD = "${var.mysql_password}"
    SECRET_KEY     = "${var.webplatform_secret}"
   }

  type = "Opaque"
}
