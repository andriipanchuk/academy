resource "kubernetes_secret" "webplatform_secret" {
  metadata {
    name      = "webplatform-secret"
    namespace = "${var.webplatform_namespace}"
  }

  data {
    MYSQL_PASSWORD = "${var.webplatform_password}"
    SECRET_KEY     = "${var.webplatform_secret}"
   }

  type = "Opaque"
}
