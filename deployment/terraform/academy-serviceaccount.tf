resource "kubernetes_service_account" "academy_service_account" {
  metadata {
    name      = "${var.academy_service_account}"
    namespace = "${var.deployment_environment}"
  }

  secret {
    name = "${kubernetes_secret.academy-service-account-secret.metadata.0.name}"
  }

  automount_service_account_token = true
}

resource "kubernetes_secret" "academy-service-account-secret" {
  metadata {
    name      = "academy-service-account-secret"
    namespace = "${var.deployment_environment}"
  }
}

resource "kubernetes_cluster_role_binding" "academy-cluster-rule" {
  depends_on = [
    "kubernetes_secret.academy-service-account-secret",
  ]

  metadata {
    name = "academy-cluster-rule-${var.deployment_environment}"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = "cluster-admin"
  }

  subject {
    kind      = "ServiceAccount"
    name      = "${kubernetes_service_account.academy_service_account.metadata.0.name}"
    namespace = "${kubernetes_service_account.academy_service_account.metadata.0.namespace}"
  }
}
