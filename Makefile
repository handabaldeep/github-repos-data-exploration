DISTRO:=$(shell lsb_release -cs)

install-terraform:
		sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
		wget -O- https://apt.releases.hashicorp.com/gpg | \
		gpg --dearmor | \
		sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
		echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
		https://apt.releases.hashicorp.com $(DISTRO) main" | \
		sudo tee /etc/apt/sources.list.d/hashicorp.list
		sudo apt update
		sudo apt-get install terraform

install-gcloud:
		sudo apt-get install apt-transport-https ca-certificates gnupg
		echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
		curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
		sudo apt-get update && sudo apt-get install google-cloud-cli
		gcloud init

install-python-packages:
		pip install poetry
		poetry install --without=experiment

setup: install-terraform install-gcloud install-python-packages
		echo "Setup Successful"

create-infra:
		cd terraform; terraform init; terraform plan; terraform apply

create-prefect-blocks:
		poetry run python blocks/make_gcp_blocks.py

run-elt-flow:
		poetry run python flows/elt_bq_to_gcs.py

cleanup:
		cd terraform; terraform destroy
