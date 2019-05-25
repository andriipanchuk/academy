resource "kubernetes_service_account" "webplatform_service_account" {
  metadata {
    name = "webplatform-service-account"
    namespace = "${var.webplatform_namespace}"
  }
  secret {
    name = "${kubernetes_secret.webplatform-service-account-secret.metadata.0.name}"
  }
  automount_service_account_token = true
}

resource "kubernetes_secret" "webplatform-service-account-secret" {
  metadata {
    name = "webplatform-service-account-secret"
    namespace = "${var.webplatform_namespace}"
  }
}
