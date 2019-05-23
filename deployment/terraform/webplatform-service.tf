resource "kubernetes_service" "webplatform_service" {

  metadata {
    name = "terraform-webplatform-service"
    namespace = "${var.webplatform_namespace}"
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
