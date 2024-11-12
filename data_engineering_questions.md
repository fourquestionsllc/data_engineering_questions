
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
