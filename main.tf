resource "null_resource" "execbluecat"{
  triggers = {
    #Forces TF to always replace this resource, thus always run the command.
    timestamp = "${timestamp()}"
  }
  provisioner "local-exec"{
    command = <<-EOT
      curl "https://raw.githubusercontent.com/jmueller-hf/terraform-cln-bluecat/v1.10.0/main.py" -o main.py
      curl "https://raw.githubusercontent.com/jmueller-hf/terraform-cln-bluecat/v1.10.0/requirements.txt" -o requirements.txt
      pip3 install -r requirements.txt
      python3 main.py --hostname "${var.hostname}" --value "${var.value}" --svcPassword "${var.password}" > /tmp/main.py.log
    EOT
  }
}
