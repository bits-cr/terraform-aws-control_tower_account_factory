# terraform-docs

[![Build Status](https://github.com/terraform-docs/terraform-docs/workflows/ci/badge.svg)](https://github.com/terraform-docs/terraform-docs/actions) [![GoDoc](https://pkg.go.dev/badge/github.com/terraform-docs/terraform-docs)](https://pkg.go.dev/github.com/terraform-docs/terraform-docs) [![Go Report Card](https://goreportcard.com/badge/github.com/terraform-docs/terraform-docs)](https://goreportcard.com/report/github.com/terraform-docs/terraform-docs) [![Codecov Report](https://codecov.io/gh/terraform-docs/terraform-docs/branch/master/graph/badge.svg)](https://codecov.io/gh/terraform-docs/terraform-docs) [![License](https://img.shields.io/github/license/terraform-docs/terraform-docs)](https://github.com/terraform-docs/terraform-docs/blob/master/LICENSE) [![Latest release](https://img.shields.io/github/v/release/terraform-docs/terraform-docs)](https://github.com/terraform-docs/terraform-docs/releases)

![terraform-docs-teaser](./images/terraform-docs-teaser.png)

Sponsored by [Scalr - Terraform Automation & Collaboration Software](https://scalr.com/?utm_source=terraform-docs)

<a href="https://www.scalr.com/?utm_source=terraform-docs" target="_blank"><img src="https://bit.ly/2T7Qm3U" alt="Scalr - Terraform Automation & Collaboration Software" width="175" height="40" /></a>

## What is terraform-docs

A utility to generate documentation from Terraform modules in various output formats.

## Installation

macOS users can install using [Homebrew]:

```bash
brew install terraform-docs
```

or

```bash
brew install terraform-docs/tap/terraform-docs
```

Windows users can install using [Scoop]:

```bash
scoop bucket add terraform-docs https://github.com/terraform-docs/scoop-bucket
scoop install terraform-docs
```

or [Chocolatey]:

```bash
choco install terraform-docs
```

Stable binaries are also available on the [releases] page. To install, download the
binary for your platform from "Assets" and place this into your `$PATH`:

```bash
curl -Lo ./terraform-docs.tar.gz https://github.com/terraform-docs/terraform-docs/releases/download/v0.16.0/terraform-docs-v0.16.0-$(uname)-amd64.tar.gz
tar -xzf terraform-docs.tar.gz
chmod +x terraform-docs
mv terraform-docs /usr/local/terraform-docs
```

**NOTE:** Windows releases are in `ZIP` format.

The latest version can be installed using `go install` or `go get`:

```bash
# go1.17+
go install github.com/terraform-docs/terraform-docs@v0.16.0
```

```bash
# go1.16
GO111MODULE="on" go get github.com/terraform-docs/terraform-docs@v0.16.0
```

**NOTE:** please use the latest Go to do this, minimum `go1.16` is required.

This will put `terraform-docs` in `$(go env GOPATH)/bin`. If you encounter the error
`terraform-docs: command not found` after installation then you may need to either add
that directory to your `$PATH` as shown [here] or do a manual installation by cloning
the repo and run `make build` from the repository which will put `terraform-docs` in:

```bash
$(go env GOPATH)/src/github.com/terraform-docs/terraform-docs/bin/$(uname | tr '[:upper:]' '[:lower:]')-amd64/terraform-docs
```

## Usage

### Running the binary directly

To run and generate documentation into README within a directory:

```bash
terraform-docs markdown table --output-file README.md --output-mode inject /path/to/module
```

Check [`output`] configuration for more details and examples.

### Using docker

terraform-docs can be run as a container by mounting a directory with `.tf`
files in it and run the following command:

```bash
docker run --rm --volume "$(pwd):/terraform-docs" -u $(id -u) quay.io/terraform-docs/terraform-docs:0.16.0 markdown /terraform-docs
```

If `output.file` is not enabled for this module, generated output can be redirected
back to a file:

```bash
docker run --rm --volume "$(pwd):/terraform-docs" -u $(id -u) quay.io/terraform-docs/terraform-docs:0.16.0 markdown /terraform-docs > doc.md
```

**NOTE:** Docker tag `latest` refers to _latest_ stable released version and `edge`
refers to HEAD of `master` at any given point in time.

### Using GitHub Actions

To use terraform-docs GitHub Action, configure a YAML workflow file (e.g.
`.github/workflows/documentation.yml`) with the following:

```yaml
name: Generate terraform docs
on:
  - pull_request

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
      with:
        ref: ${{ github.event.pull_request.head.ref }}

    - name: Render terraform docs and push changes back to PR
      uses: terraform-docs/gh-actions@main
      with:
        working-dir: .
        output-file: README.md
        output-method: inject
        git-push: "true"
```

Read more about [terraform-docs GitHub Action] and its configuration and
examples.

### pre-commit hook

With pre-commit, you can ensure your Terraform module documentation is kept
up-to-date each time you make a commit.

First [install pre-commit] and then create or update a `.pre-commit-config.yaml`
in the root of your Git repo with at least the following content:

```yaml
repos:
  - repo: https://github.com/terraform-docs/terraform-docs
    rev: "v0.16.0"
    hooks:
      - id: terraform-docs-go
        args: ["markdown", "table", "--output-file", "README.md", "./mymodule/path"]
```

Then run:

```bash
pre-commit install
pre-commit install-hooks
```

Further changes to your module's `.tf` files will cause an update to documentation
when you make a commit.

## Configuration

terraform-docs can be configured with a yaml file. The default name of this file is
`.terraform-docs.yml` and the path order for locating it is:

1. root of module directory
1. `.config/` folder at root of module directory
1. current directory
1. `.config/` folder at current directory
1. `$HOME/.tfdocs.d/`

```yaml
formatter: "" # this is required

version: ""

header-from: main.tf
footer-from: ""

recursive:
  enabled: false
  path: modules

sections:
  hide: []
  show: []

content: ""

output:
  file: ""
  mode: inject
  template: |-
    <!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.6.1, < 2.0.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 6.0.0, < 7.0.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | >= 6.0.0, < 7.0.0 |
| <a name="provider_local"></a> [local](#provider\_local) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_aft_account_provisioning_framework"></a> [aft\_account\_provisioning\_framework](#module\_aft\_account\_provisioning\_framework) | ./modules/aft-account-provisioning-framework | n/a |
| <a name="module_aft_account_request_framework"></a> [aft\_account\_request\_framework](#module\_aft\_account\_request\_framework) | ./modules/aft-account-request-framework | n/a |
| <a name="module_aft_backend"></a> [aft\_backend](#module\_aft\_backend) | ./modules/aft-backend | n/a |
| <a name="module_aft_code_repositories"></a> [aft\_code\_repositories](#module\_aft\_code\_repositories) | ./modules/aft-code-repositories | n/a |
| <a name="module_aft_customizations"></a> [aft\_customizations](#module\_aft\_customizations) | ./modules/aft-customizations | n/a |
| <a name="module_aft_feature_options"></a> [aft\_feature\_options](#module\_aft\_feature\_options) | ./modules/aft-feature-options | n/a |
| <a name="module_aft_iam_roles"></a> [aft\_iam\_roles](#module\_aft\_iam\_roles) | ./modules/aft-iam-roles | n/a |
| <a name="module_aft_lambda_layer"></a> [aft\_lambda\_layer](#module\_aft\_lambda\_layer) | ./modules/aft-lambda-layer | n/a |
| <a name="module_aft_ssm_parameters"></a> [aft\_ssm\_parameters](#module\_aft\_ssm\_parameters) | ./modules/aft-ssm-parameters | n/a |
| <a name="module_packaging"></a> [packaging](#module\_packaging) | ./modules/aft-archives | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_partition.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/partition) | data source |
| [aws_service.home_region_validation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/service) | data source |
| [local_file.python_version](https://registry.terraform.io/providers/hashicorp/local/latest/docs/data-sources/file) | data source |
| [local_file.version](https://registry.terraform.io/providers/hashicorp/local/latest/docs/data-sources/file) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_account_customizations_repo_branch"></a> [account\_customizations\_repo\_branch](#input\_account\_customizations\_repo\_branch) | Branch to source account customizations repo from | `string` | `"main"` | no |
| <a name="input_account_customizations_repo_name"></a> [account\_customizations\_repo\_name](#input\_account\_customizations\_repo\_name) | Repository name for the account customizations files. For non-CodeCommit repos, name should be in the format of Org/Repo | `string` | `"aft-account-customizations"` | no |
| <a name="input_account_provisioning_customizations_repo_branch"></a> [account\_provisioning\_customizations\_repo\_branch](#input\_account\_provisioning\_customizations\_repo\_branch) | Branch to source account provisioning customization files | `string` | `"main"` | no |
| <a name="input_account_provisioning_customizations_repo_name"></a> [account\_provisioning\_customizations\_repo\_name](#input\_account\_provisioning\_customizations\_repo\_name) | Repository name for the account provisioning customizations files. For non-CodeCommit repos, name should be in the format of Org/Repo | `string` | `"aft-account-provisioning-customizations"` | no |
| <a name="input_account_provisioning_customizations_workspace_name"></a> [account\_provisioning\_customizations\_workspace\_name](#input\_account\_provisioning\_customizations\_workspace\_name) | Workspace name to use for the account provisioning customizations operation in Terraform Cloud or Enterprise. Note: changing this value for an existing deployment creates a new workspace and orphans the old one - it is not an in-place rename. | `string` | `"ct-aft-account-provisioning-customizations"` | no |
| <a name="input_account_request_repo_branch"></a> [account\_request\_repo\_branch](#input\_account\_request\_repo\_branch) | Branch to source account request repo from | `string` | `"main"` | no |
| <a name="input_account_request_repo_name"></a> [account\_request\_repo\_name](#input\_account\_request\_repo\_name) | Repository name for the account request files. For non-CodeCommit repos, name should be in the format of Org/Repo | `string` | `"aft-account-request"` | no |
| <a name="input_account_request_workspace_name"></a> [account\_request\_workspace\_name](#input\_account\_request\_workspace\_name) | Workspace name to use for the account request operation in Terraform Cloud or Enterprise. Note: changing this value for an existing deployment creates a new workspace and orphans the old one - it is not an in-place rename. | `string` | `"ct-aft-account-request"` | no |
| <a name="input_aft_backend_bucket_access_logs_object_expiration_days"></a> [aft\_backend\_bucket\_access\_logs\_object\_expiration\_days](#input\_aft\_backend\_bucket\_access\_logs\_object\_expiration\_days) | Amount of days to keep the objects stored in the access logs bucket for AFT backend buckets | `number` | `365` | no |
| <a name="input_aft_codebuild_compute_type"></a> [aft\_codebuild\_compute\_type](#input\_aft\_codebuild\_compute\_type) | The CodeBuild compute type that build projects will use. | `string` | `"BUILD_GENERAL1_MEDIUM"` | no |
| <a name="input_aft_customer_private_subnets"></a> [aft\_customer\_private\_subnets](#input\_aft\_customer\_private\_subnets) | A list of private subnets to deploy AFT resources in, if customer is providing an existing VPC. Only supported for new deployments. | `list(string)` | `[]` | no |
| <a name="input_aft_customer_vpc_id"></a> [aft\_customer\_vpc\_id](#input\_aft\_customer\_vpc\_id) | The VPC ID to deploy AFT resources in, if customer is providing an existing VPC. Only supported for new deployments. | `string` | `null` | no |
| <a name="input_aft_customization_triggers"></a> [aft\_customization\_triggers](#input\_aft\_customization\_triggers) | List of customization trigger tokens. When non-empty, matching events trigger customization re-execution with provisioning bypass. Valid tokens: account\_move. Per-account opt-out via account\_skip\_customization\_triggers attribute in aft-request. | `list(string)` | `[]` | no |
| <a name="input_aft_enable_vpc"></a> [aft\_enable\_vpc](#input\_aft\_enable\_vpc) | Flag turning use of VPC on/off for AFT | `bool` | `true` | no |
| <a name="input_aft_feature_cloudtrail_data_events"></a> [aft\_feature\_cloudtrail\_data\_events](#input\_aft\_feature\_cloudtrail\_data\_events) | Feature flag toggling CloudTrail data events on/off | `bool` | `false` | no |
| <a name="input_aft_feature_delete_default_vpcs_enabled"></a> [aft\_feature\_delete\_default\_vpcs\_enabled](#input\_aft\_feature\_delete\_default\_vpcs\_enabled) | Feature flag toggling deletion of default VPCs on/off | `bool` | `false` | no |
| <a name="input_aft_feature_enterprise_support"></a> [aft\_feature\_enterprise\_support](#input\_aft\_feature\_enterprise\_support) | Feature flag toggling Enterprise Support enrollment on/off | `bool` | `false` | no |
| <a name="input_aft_framework_repo_git_ref"></a> [aft\_framework\_repo\_git\_ref](#input\_aft\_framework\_repo\_git\_ref) | Git branch from which the AFT framework should be sourced from | `string` | `null` | no |
| <a name="input_aft_framework_repo_url"></a> [aft\_framework\_repo\_url](#input\_aft\_framework\_repo\_url) | Git repo URL where the AFT framework should be sourced from | `string` | `"https://github.com/aws-ia/terraform-aws-control_tower_account_factory.git"` | no |
| <a name="input_aft_management_account_id"></a> [aft\_management\_account\_id](#input\_aft\_management\_account\_id) | AFT Management Account ID | `string` | n/a | yes |
| <a name="input_aft_metrics_reporting"></a> [aft\_metrics\_reporting](#input\_aft\_metrics\_reporting) | Flag toggling reporting of operational metrics | `bool` | `true` | no |
| <a name="input_aft_vpc_cidr"></a> [aft\_vpc\_cidr](#input\_aft\_vpc\_cidr) | CIDR Block to allocate to the AFT VPC | `string` | `"192.168.0.0/22"` | no |
| <a name="input_aft_vpc_endpoints"></a> [aft\_vpc\_endpoints](#input\_aft\_vpc\_endpoints) | Flag turning VPC endpoints on/off for AFT VPC | `bool` | `true` | no |
| <a name="input_aft_vpc_private_subnet_01_cidr"></a> [aft\_vpc\_private\_subnet\_01\_cidr](#input\_aft\_vpc\_private\_subnet\_01\_cidr) | CIDR Block to allocate to the Private Subnet 01 | `string` | `"192.168.0.0/24"` | no |
| <a name="input_aft_vpc_private_subnet_02_cidr"></a> [aft\_vpc\_private\_subnet\_02\_cidr](#input\_aft\_vpc\_private\_subnet\_02\_cidr) | CIDR Block to allocate to the Private Subnet 02 | `string` | `"192.168.1.0/24"` | no |
| <a name="input_aft_vpc_public_subnet_01_cidr"></a> [aft\_vpc\_public\_subnet\_01\_cidr](#input\_aft\_vpc\_public\_subnet\_01\_cidr) | CIDR Block to allocate to the Public Subnet 01 | `string` | `"192.168.2.0/25"` | no |
| <a name="input_aft_vpc_public_subnet_02_cidr"></a> [aft\_vpc\_public\_subnet\_02\_cidr](#input\_aft\_vpc\_public\_subnet\_02\_cidr) | CIDR Block to allocate to the Public Subnet 02 | `string` | `"192.168.2.128/25"` | no |
| <a name="input_audit_account_id"></a> [audit\_account\_id](#input\_audit\_account\_id) | Audit Account Id | `string` | n/a | yes |
| <a name="input_backup_recovery_point_retention"></a> [backup\_recovery\_point\_retention](#input\_backup\_recovery\_point\_retention) | Number of days to keep backup recovery points in AFT DynamoDB tables. Default = Never Expire | `number` | `null` | no |
| <a name="input_backup_schedule"></a> [backup\_schedule](#input\_backup\_schedule) | Cron expression for the DynamoDB backup schedule. Default = hourly | `string` | `"cron(0 * * * ? *)"` | no |
| <a name="input_cloudwatch_log_group_enable_cmk_encryption"></a> [cloudwatch\_log\_group\_enable\_cmk\_encryption](#input\_cloudwatch\_log\_group\_enable\_cmk\_encryption) | Flag toggling CloudWatch Log Groups encryption by using the AFT customer managed key stored in KMS. Additional charges apply. Otherwise, logs will use CloudWatch managed server-side encryption. | `bool` | `false` | no |
| <a name="input_cloudwatch_log_group_retention"></a> [cloudwatch\_log\_group\_retention](#input\_cloudwatch\_log\_group\_retention) | Amount of days to keep CloudWatch Log Groups for Lambda functions. 0 = Never Expire | `string` | `"0"` | no |
| <a name="input_concurrent_account_factory_actions"></a> [concurrent\_account\_factory\_actions](#input\_concurrent\_account\_factory\_actions) | Maximum number of accounts that can be provisioned in parallel. | `number` | `5` | no |
| <a name="input_ct_home_region"></a> [ct\_home\_region](#input\_ct\_home\_region) | The region from which this module will be executed. This MUST be the same region as Control Tower is deployed. | `string` | n/a | yes |
| <a name="input_ct_management_account_id"></a> [ct\_management\_account\_id](#input\_ct\_management\_account\_id) | Control Tower Management Account Id | `string` | n/a | yes |
| <a name="input_github_enterprise_url"></a> [github\_enterprise\_url](#input\_github\_enterprise\_url) | GitHub enterprise URL, if GitHub Enterprise is being used | `string` | `"null"` | no |
| <a name="input_gitlab_selfmanaged_url"></a> [gitlab\_selfmanaged\_url](#input\_gitlab\_selfmanaged\_url) | GitLab SelfManaged URL, if GitLab SelfManaged is being used | `string` | `"null"` | no |
| <a name="input_global_codebuild_timeout"></a> [global\_codebuild\_timeout](#input\_global\_codebuild\_timeout) | Codebuild build timeout | `number` | `60` | no |
| <a name="input_global_customizations_repo_branch"></a> [global\_customizations\_repo\_branch](#input\_global\_customizations\_repo\_branch) | Branch to source global customizations repo from | `string` | `"main"` | no |
| <a name="input_global_customizations_repo_name"></a> [global\_customizations\_repo\_name](#input\_global\_customizations\_repo\_name) | Repository name for the global customization files. For non-CodeCommit repos, name should be in the format of Org/Repo | `string` | `"aft-global-customizations"` | no |
| <a name="input_log_archive_account_id"></a> [log\_archive\_account\_id](#input\_log\_archive\_account\_id) | Log Archive Account Id | `string` | n/a | yes |
| <a name="input_log_archive_bucket_object_expiration_days"></a> [log\_archive\_bucket\_object\_expiration\_days](#input\_log\_archive\_bucket\_object\_expiration\_days) | Amount of days to keep the objects stored in the AFT logging bucket | `number` | `365` | no |
| <a name="input_maximum_concurrent_customizations"></a> [maximum\_concurrent\_customizations](#input\_maximum\_concurrent\_customizations) | Maximum number of customizations/pipelines to run at once | `number` | `5` | no |
| <a name="input_sfn_s3_bucket_object_expiration_days"></a> [sfn\_s3\_bucket\_object\_expiration\_days](#input\_sfn\_s3\_bucket\_object\_expiration\_days) | Amount of days to keep the objects stored in the CodePipeline bucket for AFT Step Functions | `number` | `90` | no |
| <a name="input_sns_topic_enable_cmk_encryption"></a> [sns\_topic\_enable\_cmk\_encryption](#input\_sns\_topic\_enable\_cmk\_encryption) | Flag toggling SNS topics encryption by using the AFT Customer managed key stored in KMS. Additional charges apply. Otherwise the SNS topics are encrypted using the AWS-managed KMS key. | `bool` | `false` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | Map of tags to apply to resources deployed by AFT. | `map(any)` | `null` | no |
| <a name="input_terraform_api_endpoint"></a> [terraform\_api\_endpoint](#input\_terraform\_api\_endpoint) | API Endpoint for Terraform. Must be in the format of https://xxx.xxx. | `string` | `"https://app.terraform.io/api/v2/"` | no |
| <a name="input_terraform_distribution"></a> [terraform\_distribution](#input\_terraform\_distribution) | Terraform distribution being used for AFT - valid values are oss, tfc, or tfe | `string` | `"oss"` | no |
| <a name="input_terraform_oidc_aws_audience"></a> [terraform\_oidc\_aws\_audience](#input\_terraform\_oidc\_aws\_audience) | The audience value to use in run identity tokens for HCP dynamic credentials (OIDC). var.aft\_feature\_hcp\_oidc must be set to true to enable OIDC. | `string` | `"aws.workload.identity"` | no |
| <a name="input_terraform_oidc_hostname"></a> [terraform\_oidc\_hostname](#input\_terraform\_oidc\_hostname) | The hostname of the TFC or TFE instance to use with AWS when configuring dynamic credentials (OIDC). var.aft\_feature\_hcp\_oidc must be set to true to enable OIDC. | `string` | `"app.terraform.io"` | no |
| <a name="input_terraform_oidc_integration"></a> [terraform\_oidc\_integration](#input\_terraform\_oidc\_integration) | Enable HCP Terraform’s native OpenID Connect integration with AWS to get dynamic credentials for the AWS provider in your HCP Terraform runs | `bool` | `false` | no |
| <a name="input_terraform_org_name"></a> [terraform\_org\_name](#input\_terraform\_org\_name) | Organization name for Terraform Cloud or Enterprise | `string` | `"null"` | no |
| <a name="input_terraform_project_name"></a> [terraform\_project\_name](#input\_terraform\_project\_name) | Project name for Terraform Cloud or Enterprise - project must exist before deployment | `string` | `"Default Project"` | no |
| <a name="input_terraform_token"></a> [terraform\_token](#input\_terraform\_token) | Terraform token for Cloud or Enterprise | `string` | `"null"` | no |
| <a name="input_terraform_version"></a> [terraform\_version](#input\_terraform\_version) | Terraform version being used for AFT | `string` | `"1.6.1"` | no |
| <a name="input_tf_backend_secondary_region"></a> [tf\_backend\_secondary\_region](#input\_tf\_backend\_secondary\_region) | AFT creates a backend for state tracking for its own state as well as OSS cases. The backend's primary region is the same as the AFT region, but this defines the secondary region to replicate to. | `string` | `""` | no |
| <a name="input_vcs_provider"></a> [vcs\_provider](#input\_vcs\_provider) | Customer VCS Provider - valid inputs are codecommit, bitbucket, github, githubenterprise, gitlab, or gitLab self-managed | `string` | `"codecommit"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_account_customizations_repo_branch"></a> [account\_customizations\_repo\_branch](#output\_account\_customizations\_repo\_branch) | n/a |
| <a name="output_account_customizations_repo_name"></a> [account\_customizations\_repo\_name](#output\_account\_customizations\_repo\_name) | n/a |
| <a name="output_account_provisioning_customizations_repo_branch"></a> [account\_provisioning\_customizations\_repo\_branch](#output\_account\_provisioning\_customizations\_repo\_branch) | n/a |
| <a name="output_account_provisioning_customizations_repo_name"></a> [account\_provisioning\_customizations\_repo\_name](#output\_account\_provisioning\_customizations\_repo\_name) | n/a |
| <a name="output_account_request_repo_branch"></a> [account\_request\_repo\_branch](#output\_account\_request\_repo\_branch) | n/a |
| <a name="output_account_request_repo_name"></a> [account\_request\_repo\_name](#output\_account\_request\_repo\_name) | n/a |
| <a name="output_aft_access_logs_primary_backend_bucket_id"></a> [aft\_access\_logs\_primary\_backend\_bucket\_id](#output\_aft\_access\_logs\_primary\_backend\_bucket\_id) | n/a |
| <a name="output_aft_account_provisioning_framework_step_function_arn"></a> [aft\_account\_provisioning\_framework\_step\_function\_arn](#output\_aft\_account\_provisioning\_framework\_step\_function\_arn) | n/a |
| <a name="output_aft_admin_role_arn"></a> [aft\_admin\_role\_arn](#output\_aft\_admin\_role\_arn) | n/a |
| <a name="output_aft_audit_exec_role_arn"></a> [aft\_audit\_exec\_role\_arn](#output\_aft\_audit\_exec\_role\_arn) | n/a |
| <a name="output_aft_backend_lock_table_name"></a> [aft\_backend\_lock\_table\_name](#output\_aft\_backend\_lock\_table\_name) | n/a |
| <a name="output_aft_backend_primary_kms_key_alias_arn"></a> [aft\_backend\_primary\_kms\_key\_alias\_arn](#output\_aft\_backend\_primary\_kms\_key\_alias\_arn) | n/a |
| <a name="output_aft_backend_primary_kms_key_id"></a> [aft\_backend\_primary\_kms\_key\_id](#output\_aft\_backend\_primary\_kms\_key\_id) | n/a |
| <a name="output_aft_backend_secondary_kms_key_alias_arn"></a> [aft\_backend\_secondary\_kms\_key\_alias\_arn](#output\_aft\_backend\_secondary\_kms\_key\_alias\_arn) | n/a |
| <a name="output_aft_backend_secondary_kms_key_id"></a> [aft\_backend\_secondary\_kms\_key\_id](#output\_aft\_backend\_secondary\_kms\_key\_id) | n/a |
| <a name="output_aft_controltower_events_table_name"></a> [aft\_controltower\_events\_table\_name](#output\_aft\_controltower\_events\_table\_name) | n/a |
| <a name="output_aft_ct_management_exec_role_arn"></a> [aft\_ct\_management\_exec\_role\_arn](#output\_aft\_ct\_management\_exec\_role\_arn) | n/a |
| <a name="output_aft_customization_triggers"></a> [aft\_customization\_triggers](#output\_aft\_customization\_triggers) | n/a |
| <a name="output_aft_exec_role_arn"></a> [aft\_exec\_role\_arn](#output\_aft\_exec\_role\_arn) | n/a |
| <a name="output_aft_failure_sns_topic_arn"></a> [aft\_failure\_sns\_topic\_arn](#output\_aft\_failure\_sns\_topic\_arn) | n/a |
| <a name="output_aft_feature_cloudtrail_data_events"></a> [aft\_feature\_cloudtrail\_data\_events](#output\_aft\_feature\_cloudtrail\_data\_events) | n/a |
| <a name="output_aft_feature_delete_default_vpcs_enabled"></a> [aft\_feature\_delete\_default\_vpcs\_enabled](#output\_aft\_feature\_delete\_default\_vpcs\_enabled) | n/a |
| <a name="output_aft_feature_enterprise_support"></a> [aft\_feature\_enterprise\_support](#output\_aft\_feature\_enterprise\_support) | n/a |
| <a name="output_aft_features_step_function_arn"></a> [aft\_features\_step\_function\_arn](#output\_aft\_features\_step\_function\_arn) | n/a |
| <a name="output_aft_invoke_customizations_step_function_arn"></a> [aft\_invoke\_customizations\_step\_function\_arn](#output\_aft\_invoke\_customizations\_step\_function\_arn) | n/a |
| <a name="output_aft_kms_key_alias_arn"></a> [aft\_kms\_key\_alias\_arn](#output\_aft\_kms\_key\_alias\_arn) | n/a |
| <a name="output_aft_kms_key_id"></a> [aft\_kms\_key\_id](#output\_aft\_kms\_key\_id) | n/a |
| <a name="output_aft_log_archive_exec_role_arn"></a> [aft\_log\_archive\_exec\_role\_arn](#output\_aft\_log\_archive\_exec\_role\_arn) | n/a |
| <a name="output_aft_management_account_id"></a> [aft\_management\_account\_id](#output\_aft\_management\_account\_id) | n/a |
| <a name="output_aft_primary_backend_bucket_id"></a> [aft\_primary\_backend\_bucket\_id](#output\_aft\_primary\_backend\_bucket\_id) | n/a |
| <a name="output_aft_request_audit_table_name"></a> [aft\_request\_audit\_table\_name](#output\_aft\_request\_audit\_table\_name) | n/a |
| <a name="output_aft_request_metadata_table_name"></a> [aft\_request\_metadata\_table\_name](#output\_aft\_request\_metadata\_table\_name) | n/a |
| <a name="output_aft_request_table_name"></a> [aft\_request\_table\_name](#output\_aft\_request\_table\_name) | n/a |
| <a name="output_aft_secondary_backend_bucket_id"></a> [aft\_secondary\_backend\_bucket\_id](#output\_aft\_secondary\_backend\_bucket\_id) | n/a |
| <a name="output_aft_sns_topic_arn"></a> [aft\_sns\_topic\_arn](#output\_aft\_sns\_topic\_arn) | n/a |
| <a name="output_aft_vpc_cidr"></a> [aft\_vpc\_cidr](#output\_aft\_vpc\_cidr) | n/a |
| <a name="output_aft_vpc_private_subnet_01_cidr"></a> [aft\_vpc\_private\_subnet\_01\_cidr](#output\_aft\_vpc\_private\_subnet\_01\_cidr) | n/a |
| <a name="output_aft_vpc_private_subnet_02_cidr"></a> [aft\_vpc\_private\_subnet\_02\_cidr](#output\_aft\_vpc\_private\_subnet\_02\_cidr) | n/a |
| <a name="output_aft_vpc_public_subnet_01_cidr"></a> [aft\_vpc\_public\_subnet\_01\_cidr](#output\_aft\_vpc\_public\_subnet\_01\_cidr) | n/a |
| <a name="output_aft_vpc_public_subnet_02_cidr"></a> [aft\_vpc\_public\_subnet\_02\_cidr](#output\_aft\_vpc\_public\_subnet\_02\_cidr) | n/a |
| <a name="output_audit_account_id"></a> [audit\_account\_id](#output\_audit\_account\_id) | n/a |
| <a name="output_backup_recovery_point_retention"></a> [backup\_recovery\_point\_retention](#output\_backup\_recovery\_point\_retention) | n/a |
| <a name="output_cloudwatch_log_group_retention"></a> [cloudwatch\_log\_group\_retention](#output\_cloudwatch\_log\_group\_retention) | n/a |
| <a name="output_ct_home_region"></a> [ct\_home\_region](#output\_ct\_home\_region) | n/a |
| <a name="output_ct_management_account_id"></a> [ct\_management\_account\_id](#output\_ct\_management\_account\_id) | n/a |
| <a name="output_github_enterprise_url"></a> [github\_enterprise\_url](#output\_github\_enterprise\_url) | n/a |
| <a name="output_gitlab_selfmanaged_url"></a> [gitlab\_selfmanaged\_url](#output\_gitlab\_selfmanaged\_url) | n/a |
| <a name="output_global_customizations_repo_branch"></a> [global\_customizations\_repo\_branch](#output\_global\_customizations\_repo\_branch) | n/a |
| <a name="output_global_customizations_repo_name"></a> [global\_customizations\_repo\_name](#output\_global\_customizations\_repo\_name) | n/a |
| <a name="output_log_archive_account_id"></a> [log\_archive\_account\_id](#output\_log\_archive\_account\_id) | n/a |
| <a name="output_maximum_concurrent_customizations"></a> [maximum\_concurrent\_customizations](#output\_maximum\_concurrent\_customizations) | n/a |
| <a name="output_terraform_api_endpoint"></a> [terraform\_api\_endpoint](#output\_terraform\_api\_endpoint) | n/a |
| <a name="output_terraform_distribution"></a> [terraform\_distribution](#output\_terraform\_distribution) | n/a |
| <a name="output_terraform_org_name"></a> [terraform\_org\_name](#output\_terraform\_org\_name) | n/a |
| <a name="output_terraform_version"></a> [terraform\_version](#output\_terraform\_version) | n/a |
| <a name="output_tf_backend_secondary_region"></a> [tf\_backend\_secondary\_region](#output\_tf\_backend\_secondary\_region) | n/a |
| <a name="output_vcs_provider"></a> [vcs\_provider](#output\_vcs\_provider) | n/a |
<!-- END_TF_DOCS -->

output-values:
  enabled: false
  from: ""

sort:
  enabled: true
  by: name

settings:
  anchor: true
  color: true
  default: true
  description: false
  escape: true
  hide-empty: false
  html: true
  indent: 2
  lockfile: true
  read-comments: true
  required: true
  sensitive: true
  type: true
```

## Content Template

Generated content can be customized further away with `content` in configuration.
If the `content` is empty the default order of sections is used.

Compatible formatters for customized content are `asciidoc` and `markdown`. `content`
will be ignored for other formatters.

`content` is a Go template with following additional variables:

- `{{ .Header }}`
- `{{ .Footer }}`
- `{{ .Inputs }}`
- `{{ .Modules }}`
- `{{ .Outputs }}`
- `{{ .Providers }}`
- `{{ .Requirements }}`
- `{{ .Resources }}`

and following functions:

- `{{ include "relative/path/to/file" }}`

These variables are the generated output of individual sections in the selected
formatter. For example `{{ .Inputs }}` is Markdown Table representation of _inputs_
when formatter is set to `markdown table`.

Note that sections visibility (i.e. `sections.show` and `sections.hide`) takes
precedence over the `content`.

Additionally there's also one extra special variable avaialble to the `content`:

- `{{ .Module }}`

As opposed to the other variables mentioned above, which are generated sections
based on a selected formatter, the `{{ .Module }}` variable is just a `struct`
representing a [Terraform module].

````yaml
content: |-
  Any arbitrary text can be placed anywhere in the content

  {{ .Header }}

  and even in between sections

  {{ .Providers }}

  and they don't even need to be in the default order

  {{ .Outputs }}

  include any relative files

  {{ include "relative/path/to/file" }}

  {{ .Inputs }}

  # Examples

  ```hcl
  {{ include "examples/foo/main.tf" }}
  ```

  ## Resources

  {{ range .Module.Resources }}
  - {{ .GetMode }}.{{ .Spec }} ({{ .Position.Filename }}#{{ .Position.Line }})
  {{- end }}
````

## Build on top of terraform-docs

terraform-docs primary use-case is to be utilized as a standalone binary, but
some parts of it is also available publicly and can be imported in your project
as a library.

```go
import (
    "github.com/terraform-docs/terraform-docs/format"
    "github.com/terraform-docs/terraform-docs/print"
    "github.com/terraform-docs/terraform-docs/terraform"
)

// buildTerraformDocs for module root `path` and provided content `tmpl`.
func buildTerraformDocs(path string, tmpl string) (string, error) {
    config := print.DefaultConfig()
    config.ModuleRoot = path // module root path (can be relative or absolute)

    module, err := terraform.LoadWithOptions(config)
    if err != nil {
        return "", err
    }

    // Generate in Markdown Table format
    formatter := format.NewMarkdownTable(config)

    if err := formatter.Generate(module); err != nil {
        return "", err
    }

    // // Note: if you don't intend to provide additional template for the generated
    // // content, or the target format doesn't provide templating (e.g. json, yaml,
    // // xml, or toml) you can use `Content()` function instead of `Render()`.
    // // `Content()` returns all the sections combined with predefined order.
    // return formatter.Content(), nil

    return formatter.Render(tmpl)
}
```

## Plugin

Generated output can be heavily customized with [`content`], but if using that
is not enough for your use-case, you can write your own plugin.

In order to install a plugin the following steps are needed:

- download the plugin and place it in `~/.tfdocs.d/plugins` (or `./.tfdocs.d/plugins`)
- make sure the plugin file name is `tfdocs-format-<NAME>`
- modify [`formatter`] of `.terraform-docs.yml` file to be `<NAME>`

**Important notes:**

- if the plugin file name is different than the example above, terraform-docs won't
be able to to pick it up nor register it properly
- you can only use plugin thorough `.terraform-docs.yml` file and it cannot be used
with CLI arguments

To create a new plugin create a new repository called `tfdocs-format-<NAME>` with
following `main.go`:

```go
package main

import (
    _ "embed" //nolint

    "github.com/terraform-docs/terraform-docs/plugin"
    "github.com/terraform-docs/terraform-docs/print"
    "github.com/terraform-docs/terraform-docs/template"
    "github.com/terraform-docs/terraform-docs/terraform"
)

func main() {
    plugin.Serve(&plugin.ServeOpts{
        Name:    "<NAME>",
        Version: "0.1.0",
        Printer: printerFunc,
    })
}

//go:embed sections.tmpl
var tplCustom []byte

// printerFunc the function being executed by the plugin client.
func printerFunc(config *print.Config, module *terraform.Module) (string, error) {
    tpl := template.New(config,
        &template.Item{Name: "custom", Text: string(tplCustom)},
    )

    rendered, err := tpl.Render("custom", module)
    if err != nil {
        return "", err
    }

    return rendered, nil
}
```

Please refer to [tfdocs-format-template] for more details. You can create a new
repository from it by clicking on `Use this template` button.

## Documentation

- **Users**
  - Read the [User Guide] to learn how to use terraform-docs
  - Read the [Formats Guide] to learn about different output formats of terraform-docs
  - Refer to [Config File Reference] for all the available configuration options
- **Developers**
  - Read [Contributing Guide] before submitting a pull request

Visit [our website] for all documentation.

## Community

- Discuss terraform-docs on [Slack]

## License

MIT License - Copyright (c) 2021 The terraform-docs Authors.

[Chocolatey]: https://www.chocolatey.org
[Config File Reference]: https://terraform-docs.io/user-guide/configuration/
[`content`]: https://terraform-docs.io/user-guide/configuration/content/
[Contributing Guide]: CONTRIBUTING.md
[Formats Guide]: https://terraform-docs.io/reference/terraform-docs/
[`formatter`]: https://terraform-docs.io/user-guide/configuration/formatter/
[here]: https://golang.org/doc/code.html#GOPATH
[Homebrew]: https://brew.sh
[install pre-commit]: https://pre-commit.com/#install
[`output`]: https://terraform-docs.io/user-guide/configuration/output/
[releases]: https://github.com/terraform-docs/terraform-docs/releases
[Scoop]: https://scoop.sh/
[Slack]: https://slack.terraform-docs.io/
[terraform-docs GitHub Action]: https://github.com/terraform-docs/gh-actions
[Terraform module]: https://pkg.go.dev/github.com/terraform-docs/terraform-docs/terraform#Module
[tfdocs-format-template]: https://github.com/terraform-docs/tfdocs-format-template
[our website]: https://terraform-docs.io/
[User Guide]: https://terraform-docs.io/user-guide/introduction/
