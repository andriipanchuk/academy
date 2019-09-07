resource "kubernetes_service" "webplatform_service" {

  metadata {
    name = "webplatform-service"
    namespace = "${var.deployment_namespace}"
  }

  spec {
    selector { run = "webplatform"  }

    port {
      port = 7101
      target_port = 5000
    }

    type = "NodePort"
  }
}
