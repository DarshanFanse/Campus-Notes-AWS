# CampusNotes – AWS Cloud-Based Study Material Portal

CampusNotes is a lightweight, responsive study-material portal that allows students to explore subject-wise learning resources and download PDF notes from a single platform.

I developed this project independently as part of my Cloud Computing Lab, implementing the frontend and AWS cloud infrastructure.

## Features

- Six subject categories with descriptions.
- Search and filter functionality.
- Subject-wise study material pages.
- Downloadable PDF resources.
- Responsive and user-friendly interface.
- AWS-based hosting and storage integration.

## Technology Stack

**Frontend**
- HTML5
- CSS3
- JavaScript

**AWS Services**
- Amazon EC2 – Website hosting.
- Amazon S3 – Storage for study materials and project resources.
- Amazon VPC – Isolated cloud networking.
- Public Subnet – Network placement for the hosting environment.
- Internet Gateway – Internet connectivity.
- Route Tables – Network traffic routing.
- Security Groups – Inbound traffic control.
- AWS IAM Role – Controlled EC2 access to S3 resources.

## Architecture Overview

1. Created a custom VPC with a public subnet.
2. Configured an Internet Gateway and route table for internet connectivity.
3. Created a security group to control HTTP and SSH access.
4. Launched an Amazon EC2 instance to host the website.
5. Created an Amazon S3 bucket to store study materials.
6. Configured an IAM role to provide the EC2 instance with controlled S3 access.
7. Deployed the CampusNotes website and tested its functionality.

## Project Structure

```text
campus-notes-aws/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── sample-notes/
├── screenshots/
├── README.md
└── .gitignore
```

## Screenshots

Screenshots of the website and AWS infrastructure are available in the `screenshots/` directory.

## Learning Outcomes

- Practical experience with AWS cloud infrastructure.
- Understanding of VPC, subnetting and network routing.
- EC2 instance configuration and website deployment.
- S3 storage management.
- IAM roles and permission management.
- Integration of frontend applications with AWS services.

---
