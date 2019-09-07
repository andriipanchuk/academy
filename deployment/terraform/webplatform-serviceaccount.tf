resource "kubernetes_service_account" "webplatform_service_account" {
  metadata {
    name = "webplatform-service-account"
    namespace = "${var.deployment_namespace}"
  }
  secret {
    name = "${kubernetes_secret.webplatform-service-account-secret.metadata.0.name}"
  }
  automount_service_account_token = true
}

resource "kubernetes_secret" "webplatform-service-account-secret" {
  metadata {
    name = "webplatform-service-account-secret"
    namespace = "${var.deployment_namespace}"
  }
}

resource "kubernetes_cluster_role_binding" "webplatform-cluster-rule" {
    depends_on = [
      "kubernetes_secret.webplatform-service-account-secret"
    ]
    metadata {
        name = "webplatform-cluster-rule-${var.deployment_environment}"
    }
    role_ref {
        api_group = "rbac.authorization.k8s.io"
        kind      = "ClusterRole"
        name      = "cluster-admin"
    }
    subject {
        kind      = "ServiceAccount"
        name      = "${kubernetes_service_account.webplatform_service_account.metadata.0.name}"
        namespace = "${kubernetes_service_account.webplatform_service_account.metadata.0.namespace}"
    }
}
