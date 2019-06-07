terraform {
  backend "gcs" {
    bucket  = "fuchicorp"
    prefix  = "dev/webplatform"
    project = "fuchicorp-project"
  }
}
