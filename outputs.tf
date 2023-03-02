output "bc_objectId" {
  value = jsondecode(resource.aws_lambda_invocation.aRecord.result)
}

output "fqdn" {
  value = "${var.hostname}.${var.domain}"
}
