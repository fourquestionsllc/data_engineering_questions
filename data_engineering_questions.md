# Topic: AWS RDS

## question:

A company wants to move away from Oracle to Aurora and assign an architect to do the assessment. They have been given a few top features to analyze and find those that are unfit for Aurora. Help them explore the following features and find the unfit ones.

(Select all that apply)

A. Authentication using lAM is unavailable when it comes to Aurora cluster users

B. Encryption at rest is possible using KMS.

C. Replicas, Automated backups and snapshots can also be encrypted.

D. Clients are responsible for protecting the instance with a security group

E. Admin gets privileges to connect to the Aurora cluster via SSH.

## answer:

To assess the compatibility of Aurora with Oracle, let's examine each feature for its availability or limitations in Aurora. Here’s a breakdown of each option:

A. Authentication using IAM is unavailable when it comes to Aurora cluster users

Incorrect: Aurora does support IAM database authentication for both MySQL and PostgreSQL-compatible Aurora databases, allowing users to authenticate via AWS IAM rather than traditional database credentials. So, this statement is untrue; IAM authentication is available.

B. Encryption at rest is possible using KMS

Correct: Aurora supports encryption at rest through AWS Key Management Service (KMS). This feature is available and commonly used for data protection in Aurora clusters.

C. Replicas, Automated backups, and snapshots can also be encrypted

Correct: In Aurora, if encryption at rest is enabled, all associated replicas, automated backups, and snapshots are also encrypted using KMS. This feature is fully supported.

D. Clients are responsible for protecting the instance with a security group

Correct: AWS RDS and Aurora both require users to configure security groups to control access. This aligns with AWS’s shared responsibility model, where clients handle the network-level security configuration.

E. Admin gets privileges to connect to the Aurora cluster via SSH

Incorrect: Aurora is a managed database service, and as such, users do not have access to the underlying operating system. SSH access is not available for Aurora clusters, unlike self-managed databases where admins might access the OS.

Answer

The unfit options for Aurora are:

A. Authentication using IAM is unavailable when it comes to Aurora cluster users (This is incorrect; IAM authentication is available.)

E. Admin gets privileges to connect to the Aurora cluster via SSH (SSH access is not available on Aurora).


# Topic: Terraform

## Question:

Fill in the blanks to protect the declared database password variable so that it is not exposed on CLloutput.
(There are multiple drop-downs below, Select a correct response for each drop-down)

```hcl
variable "db password" {
  description="Database administrator password"
  type = ??
  ?? =??
}
```

## Answer:

To securely manage a sensitive variable like a database password in Terraform, we can use the following code:

```hcl
variable "db_password" {
  description = "Database administrator password"
  type        = string
  sensitive   = true
}
```

Here’s a breakdown of the responses for each drop-down:

* type: string — the password should be defined as a string.
* sensitive: true — marking the variable as sensitive will prevent it from being displayed in CLI output.

This configuration ensures that the password is treated as a sensitive string variable, reducing the risk of exposure in Terraform outputs or logs.

# Topic: AWs Redshift

## Question: 

We have to apply column-level encoding to three of our tables which have major varchar and charcolumns available.

Which encoding should we apply in this scenario?

A. LZ0 Encoding

B. Zstandard (ZSTD) Encoding Algorithm

C. Delta Encoding

D. Byte-Dictionary Encoding

## answer: 

The best choice for encoding tables with primarily VARCHAR and CHAR columns is:

B. Zstandard (ZSTD) Encoding Algorithm

Explanation:

Zstandard (ZSTD) Encoding is highly efficient for compressing variable-length strings, such as VARCHAR and CHAR data, as it provides a good balance of compression ratio and performance. ZSTD is commonly recommended for columnar storage in data warehouses, especially for string data, due to its effectiveness in reducing storage costs without significant performance degradation.

Reasons the other options are less suitable:

A. LZ0 Encoding: This is an older compression method with less efficient compression compared to ZSTD, and it's not typically recommended for variable-length text columns.

C. Delta Encoding: Delta encoding works well with sequential numeric data but is not suitable for VARCHAR or CHAR columns.

D. Byte-Dictionary Encoding: While useful for columns with many repeating values, it’s not as effective as ZSTD for general-purpose text data in VARCHAR and CHAR columns.

Therefore, Zstandard (ZSTD) Encoding is the most appropriate choice here.
