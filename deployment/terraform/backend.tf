terraform {
  backend "gcs" {
    bucket = "fuchicorp"
    prefix = "${lookup(var.bucket_name, "${var.environment}")}"
  }
}
