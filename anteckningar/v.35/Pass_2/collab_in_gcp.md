## . Team Collaboration for Group Projects

### Step 1: Project Ownership and Access Control

**Important**: Only ONE team member should create the GCP project and act as the "Project Owner". This prevents billing confusion and access conflicts.

#### Designate Project Owner
1. **Choose one team member as Project Owner**
   - This person creates the GCP project
   - This person's billing account will be used
   - This person has ultimate control over the project

2. **Project Owner responsibilities:**
   - Create and configure the GCP project
   - Set up billing and budget alerts
   - Manage team member access
   - Monitor costs and usage
   - Delete project when done (important!)

### Step 1.2: Adding Team Members to GCP Project

#### For the Project Owner:

1. **Navigate to IAM & Admin**
   - Go to "IAM & Admin" → "IAM" in the GCP Console
   - Click "GRANT ACCESS" button

2. **Add team members**
   - Enter each team member's email address (their Google account)
   - Assign appropriate roles:
     ```
     For developers:
     - BigQuery Data Editor
     - BigQuery Job User
     - Storage Object Admin (if using Cloud Storage)
     
     For read-only access:
     - BigQuery Data Viewer
     - BigQuery Metadata Viewer
     ```

3. **Best practice role assignment:**
   - **Project Owner**: Project Owner role (only one person)
   - **Developers**: Editor role or custom roles listed above
   - **Observers/Reviewers**: Viewer role

### Step 1.3: Service Account Strategy for Teams

**Option A: Shared Service Account (Recommended for Students)**

1. **Project Owner creates ONE service account**
   - Follow the service account creation steps from Section 2 in gcp_gui.md
   - Download the JSON key file

2. **Share the key file securely**
   - **DO NOT** email the key file
   - **DO NOT** put it in shared folders like Google Drive
   - **DO NOT** commit it to Git/GitHub
   - ✅ Use secure sharing methods:
     - Password-protected zip file
     - Secure file sharing service (with expiration)
     - In-person transfer via USB drive

3. **Each team member uses the same key**
   - Everyone saves it as `service-account-key.json`
   - Everyone uses the same `.env` file configuration

**Option B: Individual Service Accounts (Advanced)**

1. **Each team member creates their own service account**
   - Follow naming convention: `data-pipeline-[name]-sa`
   - Project Owner grants same permissions to each account
   - Each person downloads their own key file

### Step 1.4: Code Collaboration Setup

#### Git Repository Setup

1. **Project Owner creates repository**
   - Create a new GitHub repository (private recommended)
   - Add `.gitignore` file immediately:
   ```gitignore
   # Service account keys - NEVER COMMIT THESE!
   service-account-key.json
   *.json
   
   # Environment files
   .env
   .env.local
   
   # Docker
   .dockerignore
   
   # Python
   __pycache__/
   *.pyc
   *.pyo
   *.pyd
   .Python
   venv/
   pip-log.txt
   
   # OS
   .DS_Store
   Thumbs.db
   ```

2. **Add team members as collaborators**
   - Go to repository Settings → Collaborators
   - Add team members' GitHub usernames
   - Give "Write" access to developers

#### Environment Configuration

1. **Create template files**
   - Create `.env.template` file:
   ```bash
   # Copy this file to .env and fill in your actual values
   GCP_PROJECT_ID=your-project-id-here
   BQ_DATASET_ID=raw_data
   BQ_TABLE_ID=sample_data
   ```

2. **Each team member:**
   - Copies `.env.template` to `.env`
   - Fills in the actual project ID
   - Keeps `.env` file local (never commits it)

### Step 1.5: BigQuery Collaboration Best Practices

#### Dataset Organization

1. **Use descriptive naming convention**
   ```
   team_[group_name]_raw_data     (e.g., team_alpha_raw_data)
   team_[group_name]_processed    (e.g., team_alpha_processed)
   team_[group_name]_analytics    (e.g., team_alpha_analytics)
   ```

2. **Create separate tables for different data sources**
   ```
   api_posts_data
   api_users_data
   csv_sales_data
   ```

#### Development Workflow

1. **Use separate tables for testing**
   - Production table: `sample_data`
   - Development table: `sample_data_dev`
   - Personal testing: `sample_data_[name]`

2. **Coordinate data uploads**
   - Agree on upload schedule to avoid conflicts
   - Use different time windows for testing
   - Communicate before running large data loads

### Step 1.6: Cost Management for Teams

#### Setting Up Budget Alerts

1. **Project Owner sets realistic budget**
   - Start with $5-10 for student projects
   - Set alerts at 25%, 50%, 75%, 90%
   - Add all team members to alert emails

2. **Monitor usage regularly**
   - Check BigQuery quota usage weekly
   - Review job history for expensive queries
   - Delete unnecessary datasets/tables

#### Cost-Saving Tips

1. **Optimize queries**
   ```sql
   -- Good: Select only needed columns
   SELECT userId, title FROM `project.dataset.table` LIMIT 100
   
   -- Bad: Select all data
   SELECT * FROM `project.dataset.table`
   ```

2. **Use table expiration**
   - Set expiration for temporary tables
   - Clean up test data regularly

### Step 1.7: Communication and Coordination

#### Required Team Communication

1. **Before starting work:**
   - Announce what you're working on
   - Check if anyone else is using the pipeline
   - Coordinate data source changes

2. **During development:**
   - Share error messages and solutions
   - Document any changes to schemas
   - Update team on progress

3. **After completing work:**
   - Share successful configurations
   - Document any lessons learned
   - Clean up personal test data

#### Documentation Requirements

1. **Maintain team README**
   ```markdown
   # Team [Name] Data Pipeline Project
   
   ## Team Members
   - [Name] - Project Owner
   - [Name] - Developer
   - [Name] - Developer
   
   ## Current Setup
   - GCP Project ID: [project-id]
   - BigQuery Dataset: [dataset-name]
   - Data Sources: [list sources]
   
   ## How to Run
   [Step-by-step instructions]
   
   ## Current Issues
   [Any known problems]
   ```

### Step 1.8: Security Best Practices for Teams

#### Access Control

1. **Principle of least privilege**
   - Give minimum required permissions
   - Remove access when team members leave
   - Regular permission audits

2. **Key rotation schedule**
   - Rotate service account keys monthly
   - Update all team members simultaneously
   - Deactivate old keys immediately

#### Safe Development Practices

1. **Never share credentials via:**
   - Email
   - Chat applications (Slack, Discord, etc.)
   - Shared documents
   - Version control systems

2. **Always use:**
   - Secure file sharing with expiration
   - Environment variables
   - Local configuration files

### Step 1.9: Conflict Resolution

#### Common Team Conflicts and Solutions

**Problem**: Multiple people trying to upload data simultaneously
**Solution**: 
- Establish upload schedule
- Use different table names for testing
- Coordinate via team chat

**Problem**: Someone accidentally deletes important data
**Solution**:
- Enable table snapshots
- Regular data backups
- Restricted delete permissions

**Problem**: Unexpected high costs
**Solution**:
- Immediate investigation by Project Owner
- Check job history for expensive operations
- Pause all development until resolved

### Step 1.10: Project Cleanup

#### End of Project Checklist

**Project Owner responsibilities:**
- [ ] Export any important data
- [ ] Download final query results
- [ ] Save project documentation
- [ ] Remove all team member access
- [ ] Delete all datasets and tables
- [ ] DELETE THE ENTIRE PROJECT (important for billing!)

**All team members:**
- [ ] Delete local service account key files
- [ ] Remove `.env` files
- [ ] Clean up local Docker images
- [ ] Archive code repository

---

## 10. Common Student Issues and Solutions

### Issue 1: "Permission Denied" Error

**Problem**: Pipeline fails with authentication errors

**Solution**:
1. Verify service account key file is correctly placed
2. Check that the file is named exactly `service-account-key.json`
3. Ensure BigQuery API is enabled
4. Verify service account has correct roles

### Issue 2: "Table Not Found" Error

**Problem**: BigQuery table doesn't exist

**Solution**:
1. Go to BigQuery console and verify table exists
2. Check that dataset and table names match your .env file
3. Ensure you're using the correct project ID

### Issue 3: Docker Build Fails

**Problem**: Docker cannot build the image

**Solution**:
1. Ensure Docker is running
2. Check that all files are in the correct directory
3. Verify requirements.txt has correct formatting
4. Try building without cache: `docker build --no-cache -t data-pipeline .`

### Issue 4: No Data Appears in BigQuery

**Problem**: Pipeline runs but no data shows up

**Solution**:
1. Check Docker logs: `docker logs <container-id>`
2. Verify internet connection for API access
3. Check if JSONPlaceholder API is accessible
4. Look for error messages in pipeline output


---

## . Troubleshooting Checklist

**Before running the pipeline, verify:**

- [ ] GCP project is created and selected
- [ ] BigQuery API is enabled
- [ ] Service account is created with correct permissions
- [ ] Service account key is downloaded and placed correctly
- [ ] Dataset and table are created in BigQuery
- [ ] .env file has correct project ID
- [ ] Docker is installed and running
- [ ] All code files are created with correct content

**If something goes wrong:**

1. Check the Docker container logs
2. Verify your internet connection
3. Confirm all GCP resources are in the same project
4. Test BigQuery access with a simple query
5. Verify service account permissions

