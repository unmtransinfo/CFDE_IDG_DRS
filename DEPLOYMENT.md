# AWS App Runner Deployment Guide

This guide will walk you through deploying the CFDE IDG DRS API to AWS App Runner using ECR.

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
   ```bash
   aws configure
   ```
3. **Docker** installed and running
4. **Database** - You need a PostgreSQL database accessible from AWS

## Deployment Steps

### Step 1: Configure Database Connection

Before deploying, you need to update the database configuration:

1. Edit `app/database.py` and add your database URL, OR
2. Set it as an environment variable in AWS App Runner (recommended)

The DATABASE_URL format should be:
```
postgresql://username:password@host:port/database_name
```

### Step 2: Build and Push Docker Image to ECR

Run the deployment script:

```bash
./deploy_to_ecr.sh
```

This script will:
- Check if AWS CLI and Docker are installed
- Auto-detect your AWS Account ID
- Create an ECR repository (if it doesn't exist)
- Build the Docker image
- Push the image to ECR

**Note:** You may want to edit the script to change:
- `AWS_REGION` (default: us-east-1)
- `ECR_REPOSITORY_NAME` (default: cfde-idg-drs-api)

### Step 3: Create AWS App Runner Service

#### Option A: Using AWS Console (Recommended for first-time)

1. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner/)

2. Click **"Create service"**

3. **Source Settings:**
   - Repository type: **Container registry**
   - Provider: **Amazon ECR**
   - Container image URI: Browse and select `cfde-idg-drs-api:latest`
   - Deployment trigger: **Manual** (or Automatic if you want auto-deploy on new images)
   - ECR access role: Create new role or use existing

4. **Service Settings:**
   - Service name: `cfde-idg-drs-api`
   - Virtual CPU: **1 vCPU** (can adjust based on load)
   - Memory: **2 GB** (can adjust based on load)
   - Port: **8000**

5. **Environment Variables:**
   Add the following environment variable:
   - Key: `DATABASE_URL`
   - Value: `postgresql://username:password@host:port/database_name`

6. **Auto Scaling:**
   - Min instances: **1**
   - Max instances: **5** (adjust based on expected load)
   - Max concurrency: **100** (requests per instance)

7. **Health Check:**
   - Protocol: **HTTP**
   - Path: **/**
   - Interval: **10 seconds**
   - Timeout: **5 seconds**
   - Healthy threshold: **1**
   - Unhealthy threshold: **3**

8. Click **"Create & deploy"**

#### Option B: Using AWS CLI

```bash
# Set variables
SERVICE_NAME="cfde-idg-drs-api"
AWS_REGION="us-east-1"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
IMAGE_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/cfde-idg-drs-api:latest"
DATABASE_URL="postgresql://username:password@host:port/database_name"

# Create service
aws apprunner create-service \
  --service-name $SERVICE_NAME \
  --region $AWS_REGION \
  --source-configuration '{
    "ImageRepository": {
      "ImageIdentifier": "'$IMAGE_URI'",
      "ImageConfiguration": {
        "Port": "8000",
        "RuntimeEnvironmentVariables": {
          "DATABASE_URL": "'$DATABASE_URL'"
        }
      },
      "ImageRepositoryType": "ECR"
    },
    "AutoDeploymentsEnabled": false
  }' \
  --instance-configuration '{
    "Cpu": "1 vCPU",
    "Memory": "2 GB"
  }' \
  --health-check-configuration '{
    "Protocol": "HTTP",
    "Path": "/",
    "Interval": 10,
    "Timeout": 5,
    "HealthyThreshold": 1,
    "UnhealthyThreshold": 3
  }' \
  --auto-scaling-configuration-arn "arn:aws:apprunner:$AWS_REGION:$AWS_ACCOUNT_ID:autoscalingconfiguration/DefaultConfiguration/1/00000000000000000000000000000001"
```

### Step 4: Verify Deployment

1. Wait for the service to be deployed (this may take 5-10 minutes)

2. Once deployed, App Runner will provide a URL like:
   ```
   https://xxxxxxxxxx.us-east-1.awsapprunner.com
   ```

3. Test the API:
   ```bash
   curl https://your-app-runner-url.awsapprunner.com/
   ```

   Should return:
   ```json
   {"status": "ok"}
   ```

4. Test an endpoint:
   ```bash
   curl https://your-app-runner-url.awsapprunner.com/structures?limit=5
   ```

### Step 5: Update Deployment (When Making Changes)

When you update your code:

1. Run the deployment script again:
   ```bash
   ./deploy_to_ecr.sh
   ```

2. Go to App Runner console and click **"Deploy"** to pull the new image, OR

3. Use AWS CLI:
   ```bash
   aws apprunner start-deployment --service-arn <your-service-arn> --region us-east-1
   ```

## Database Considerations

### Option 1: AWS RDS PostgreSQL (Recommended)

1. Create an RDS PostgreSQL instance in the same VPC
2. Configure security groups to allow App Runner to access RDS
3. Use the RDS endpoint as your DATABASE_URL

### Option 2: External Database

If using an external database:
- Ensure it's accessible from AWS
- Configure firewall rules to allow AWS IP ranges
- Use SSL connection if possible

## Security Best Practices

1. **Never hardcode database credentials** - Use environment variables
2. **Use AWS Secrets Manager** for sensitive data (optional but recommended)
3. **Enable VPC connector** if database is in private VPC
4. **Use HTTPS only** - App Runner provides this by default
5. **Enable encryption** - ECR encryption is enabled by default in the script

## Cost Estimation

AWS App Runner pricing (as of 2024):
- **Compute**: $0.064/vCPU-hour + $0.007/GB-hour
- **Build**: Free (using ECR)
- **Data transfer**: Standard AWS rates

Estimated monthly cost for 1 vCPU, 2 GB, running 24/7:
- ~$50-70/month (plus database costs)

## Monitoring and Logs

1. **CloudWatch Logs**: Automatically enabled
   - View in AWS Console → CloudWatch → Log groups → `/aws/apprunner/<service-name>`

2. **Metrics**: Available in CloudWatch
   - Request count
   - Response time
   - Error rates
   - Instance metrics

3. **View logs via CLI**:
   ```bash
   aws logs tail /aws/apprunner/cfde-idg-drs-api/application --follow
   ```

## Troubleshooting

### Service fails to start
- Check CloudWatch logs for errors
- Verify DATABASE_URL is correctly set
- Ensure database is accessible

### Database connection errors
- Verify database credentials
- Check security group rules
- Ensure database accepts connections from App Runner

### Image pull errors
- Verify ECR repository permissions
- Check that image exists in ECR
- Ensure App Runner has ECR access role

## Custom Domain (Optional)

1. Go to App Runner service → Custom domains
2. Add your domain
3. Update DNS with provided CNAME records
4. Wait for validation

## Useful Commands

```bash
# List App Runner services
aws apprunner list-services --region us-east-1

# Describe service
aws apprunner describe-service --service-arn <arn> --region us-east-1

# Pause service (to save costs)
aws apprunner pause-service --service-arn <arn> --region us-east-1

# Resume service
aws apprunner resume-service --service-arn <arn> --region us-east-1

# Delete service
aws apprunner delete-service --service-arn <arn> --region us-east-1

# List ECR images
aws ecr list-images --repository-name cfde-idg-drs-api --region us-east-1
```

## Support

For issues or questions:
- Check AWS App Runner documentation
- Review CloudWatch logs
- Check API health endpoint: `https://your-url.awsapprunner.com/`
