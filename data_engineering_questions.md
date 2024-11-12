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

We have to apply column-level encoding to three of our tables which have major varchar and char columns available.

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


# Topic: AWs Kinesis

## question:

To which of the following destination, Amazon Kinesis Data Firehose is a fully managed service for delivering real-time streaming data?

(Select all that apply)

A. Amazon Elastic Compute Cloud (Amazon EC2)

B. Amazon Elastic Container Service (Amazon ECS)

C. Amazon Simple Storage Service (Amazon S3)

D. Splunk

## answer:

The correct answers are:

C. Amazon Simple Storage Service (Amazon S3)

D. Splunk

Explanation:

Amazon Kinesis Data Firehose is a fully managed service for delivering real-time streaming data to specific destinations, which include:

Amazon S3: A common destination for storing and archiving data.

Amazon Redshift: For real-time data analytics within a data warehouse.

Amazon Elasticsearch Service (now Amazon OpenSearch Service): For search and real-time analytics.

Splunk: For real-time monitoring and analysis.

Reasons the other options are incorrect:

A. Amazon EC2: Kinesis Data Firehose does not deliver data directly to Amazon EC2 instances.

B. Amazon ECS: Kinesis Data Firehose does not deliver data directly to Amazon ECS.

Final Answer:

C. Amazon Simple Storage Service (Amazon S3)

D. Splunk


# Topic: AWS RDS

## question: 

An organization wants to move from using the RDBMs solution to Aurora since they want it to behighly available. You, as an architect, need to understand the internals of Aurora. Which of thebelow answers are incorrect about Aurora?

(Select all that apply)

A. It handles the loss of up to two copies of data without affecting the db write availability and three copies of data without affecting the read availability.

B. It handles the loss of up to two copies of data without affecting read availability and three copies of data without affecting the write availability.

C. Scale OUT if your writes are creating issues and scale UP if your reads are creating issues.

D. You can not create an unencrypted Aurora Replica for an encrypted Aurora DB cluster.

E. You can not create an encrypted Aurora Replica for an unencrypted Aurora DB cluster.

## answers:

The following answers are incorrect about Amazon Aurora:

B. It handles the loss of up to two copies of data without affecting read availability and three copies of data without affecting the write availability.

Explanation: This statement is incorrect. Amazon Aurora handles the loss of up to two copies of data without affecting write availability and up to three copies of data without affecting read availability. The roles of read and write availability are reversed in this option.

C. Scale OUT if your writes are creating issues and scale UP if your reads are creating issues.

Explanation: This statement is incorrect. In Aurora, to scale writes, you would typically scale up, as the write capacity of Aurora instances is determined by the instance size. To scale reads, you would scale out by adding more Aurora Replicas. The statement incorrectly advises scaling out for writes and scaling up for reads.

Correct statements:

A. It handles the loss of up to two copies of data without affecting the db write availability and three copies of data without affecting the read availability.

This is correct. Aurora maintains high availability and durability by storing copies of your data across multiple availability zones (AZs).

D. You cannot create an unencrypted Aurora Replica for an encrypted Aurora DB cluster.

This is correct. If the Aurora DB cluster is encrypted, all replicas of that cluster must also be encrypted.

E. You cannot create an encrypted Aurora Replica for an unencrypted Aurora DB cluster.

This is correct. If the original Aurora DB cluster is unencrypted, its replicas must also be unencrypted.

Summary of Incorrect Answers:

B. (Incorrect: Misstated read/write availability after data loss)

C. (Incorrect: Misstated scaling recommendations for write/read issues)
