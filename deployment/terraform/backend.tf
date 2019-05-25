terraform {
  backend "gcs" {}
}


data "terraform_remote_state" "state" {
  backend = "gcs"
  config {
    bucket = "fuchicorp"
    prefix = "${lookup(var.bucket_name, "${var.environment}")}"
  }
}
