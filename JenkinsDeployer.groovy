@Library('CommonLib@feature/kube-slave') _
def common = new com.lib.JenkinsDeployerPipeline()
common.runPipeline()
