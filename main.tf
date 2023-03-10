resource "aws_lambda_invocation" "aRecord" {
  function_name = "cln-BlueCat-Stack-clnBlueCatARecordCreate-DzMYae1wc7Do"
  input = <<JSON
    {
    "hostname": "${var.hostname}",
    "domain": "${var.domain}",
    "ipAddress": "${var.ipAddr}"
    }
    JSON
}

resource "aws_lambda_invocation" "deploy" {
  function_name = "cln-BlueCat-Stack-clnBlueCatQuickDeploy-I9h4EumoYJw9"
  input = <<JSON
      {
      "hostname": "${var.hostname}"
      }
      JSON
}
