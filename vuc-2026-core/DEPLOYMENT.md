# VUC-2026 Deployment Guide

## 🚀 Production Deployment

This guide covers the complete deployment process for the VUC-2026 autonomous YouTube content production system.

## 📋 Prerequisites

### System Requirements

- **Operating System**: Ubuntu 20.04+ or CentOS 8+
- **CPU**: Minimum 8 cores, recommended 16 cores
- **Memory**: Minimum 16GB RAM, recommended 32GB
- **Storage**: Minimum 500GB SSD, recommended 1TB SSD
- **Network**: Stable internet connection with minimum 100Mbps

### Software Requirements

- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Git**: 2.25+
- **OpenSSL**: 1.1+
- **Nginx**: 1.18+ (if not using Docker)

### Domain & SSL

- **Domain**: Registered domain (e.g., vuc-2026.com)
- **SSL Certificate**: Valid SSL certificate for HTTPS
- **DNS**: A records pointing to server IP

## 🔧 Setup Process

### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y docker.io docker-compose git curl wget openssl

# Add user to docker group
sudo usermod -aG docker $USER

# Create project directory
sudo mkdir -p /opt/vuc-2026
sudo chown $USER:$USER /opt/vuc-2026
cd /opt/vuc-2026
```

### 2. Clone Repository

```bash
# Clone the repository
git clone https://github.com/your-org/vuc-2026.git .

# Create necessary directories
mkdir -p nginx/ssl logs uploads credentials vuc_memory
mkdir -p monitoring/grafana/dashboards monitoring/grafana/provisioning
mkdir -p database/init
```

### 3. SSL Certificate Setup

#### Option A: Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Generate certificate
sudo certbot --nginx -d vuc-2026.com -d www.vuc-2026.com

# Copy certificates to project directory
sudo cp /etc/letsencrypt/live/vuc-2026.com/fullchain.pem nginx/ssl/vuc-2026.com.crt
sudo cp /etc/letsencrypt/live/vuc-2026.com/privkey.pem nginx/ssl/vuc-2026.com.key
sudo chown $USER:$USER nginx/ssl/*
```

#### Option B: Self-Signed (Development Only)

```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout nginx/ssl/vuc-2026.com.key \
    -out nginx/ssl/vuc-2026.com.crt \
    -subj "/C=TR/ST=ISTANBUL/L=ISTANBUL/O=VUC-2026/OU=IT/CN=vuc-2026.com"
```

### 4. Environment Configuration

```bash
# Copy environment template
cp .env.prod .env.local

# Edit environment file
nano .env.local
```

**Critical variables to update:**

```bash
# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
POSTGRES_PASSWORD=your-strong-postgres-password-change-this
REDIS_PASSWORD=your-strong-redis-password-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this

# API Keys
GOOGLE_API_KEY=your-google-gemini-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key
YOUTUBE_API_KEY=your-youtube-data-api-key

# Monitoring
GRAFANA_PASSWORD=your-grafana-password-change-this

# Email (optional)
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-email-password
```

### 5. Make Deployment Script Executable

```bash
chmod +x scripts/deploy.sh
```

## 🚀 Deployment Commands

### Basic Deployment

```bash
# Deploy the application
./scripts/deploy.sh deploy
```

### Available Commands

```bash
# Deploy the application
./scripts/deploy.sh deploy

# Rollback to previous version
./scripts/deploy.sh rollback

# Check deployment status
./scripts/deploy.sh status

# Create backup
./scripts/deploy.sh backup

# Run health checks
./scripts/deploy.sh health

# Cleanup Docker resources
./scripts/deploy.sh cleanup
```

## 📊 Monitoring Setup

### Grafana Dashboard

1. **Access Grafana**: `https://monitoring.vuc-2026.com/grafana`
2. **Login**: Use credentials from `.env.local`
3. **Import Dashboards**: Import from `monitoring/grafana/dashboards/`

### Prometheus Metrics

1. **Access Prometheus**: `https://monitoring.vuc-2026.com/prometheus`
2. **Browse Metrics**: Check system and application metrics
3. **Alert Rules**: Review alert rules in `monitoring/rules/`

### Key Metrics to Monitor

- **System**: CPU, Memory, Disk, Network
- **Application**: Response time, Error rate, Request rate
- **Database**: Connections, Query performance
- **Queue**: Task backlog, Worker health
- **Business**: Job success rate, Processing time

## 🔒 Security Configuration

### Firewall Setup

```bash
# Configure UFW firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow from 127.0.0.1 to any port 9090  # Prometheus
sudo ufw allow from 127.0.0.1 to any port 3001  # Grafana
```

### SSL/TLS Configuration

- **Protocol**: TLS 1.2 and 1.3 only
- **Ciphers**: Strong cipher suites
- **HSTS**: HTTP Strict Transport Security enabled
- **Certificate**: Valid SSL certificate required

### Access Control

- **Admin Access**: IP whitelisting for monitoring
- **API Access**: Rate limiting and authentication
- **Database**: Encrypted connections only
- **File Access**: Proper permissions and ACLs

## 🔄 Backup Strategy

### Automated Backups

```bash
# Create cron job for daily backups
crontab -e

# Add this line for daily backup at 2 AM
0 2 * * * /opt/vuc-2026/scripts/deploy.sh backup
```

### Backup Components

- **Database**: PostgreSQL dumps
- **Volumes**: Docker volumes (Redis, PostgreSQL data)
- **Configuration**: Nginx configs, environment files
- **Certificates**: SSL certificates
- **Logs**: Application and system logs

### Backup Retention

- **Daily**: Keep last 7 days
- **Weekly**: Keep last 4 weeks
- **Monthly**: Keep last 12 months
- **Off-site**: Optional cloud backup

## 📈 Performance Optimization

### System Tuning

```bash
# Optimize system limits
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Optimize network settings
echo "net.core.somaxconn = 65536" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 65536" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Docker Optimization

- **Resource Limits**: Set appropriate CPU and memory limits
- **Health Checks**: Configure proper health checks
- **Restart Policy**: Use `unless-stopped` for production
- **Log Rotation**: Prevent log files from growing too large

### Application Optimization

- **Database**: Connection pooling, query optimization
- **Cache**: Redis caching for frequently accessed data
- **Queue**: Proper Celery worker configuration
- **Static Files**: CDN or nginx caching

## 🚨 Troubleshooting

### Common Issues

#### 1. Services Not Starting

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend

# Check resource usage
docker stats
```

#### 2. Database Connection Issues

```bash
# Check database status
docker-compose -f docker-compose.prod.yml exec postgres pg_isready

# Check connections
docker-compose -f docker-compose.prod.yml exec postgres psql -U vuc_user -c "SELECT count(*) FROM pg_stat_activity;"
```

#### 3. High Memory Usage

```bash
# Check memory usage
docker stats --no-stream

# Restart services if needed
docker-compose -f docker-compose.prod.yml restart
```

#### 4. SSL Certificate Issues

```bash
# Check certificate validity
openssl x509 -in nginx/ssl/vuc-2026.com.crt -text -noout

# Renew Let's Encrypt certificate
sudo certbot renew
```

### Emergency Procedures

#### Service Recovery

```bash
# Quick restart
docker-compose -f docker-compose.prod.yml restart

# Full redeployment
./scripts/deploy.sh deploy

# Rollback
./scripts/deploy.sh rollback
```

#### Data Recovery

```bash
# Restore from backup
./scripts/deploy.sh backup  # Create backup first
# Then restore from latest backup
```

## 📞 Support

### Monitoring Alerts

- **Email**: Configure SMTP for alert notifications
- **Slack**: Optional Slack webhook integration
- **PagerDuty**: Optional PagerDuty integration

### Documentation

- **Runbooks**: Available in monitoring dashboard
- **API Docs**: `/docs` endpoint (if enabled)
- **Logs**: Centralized logging in `/var/log/vuc-2026/`

### Contact

- **Technical Support**: tech-support@vuc-2026.com
- **Emergency**: emergency@vuc-2026.com
- **Documentation**: https://docs.vuc-2026.com

## 🔄 Updates & Maintenance

### Update Process

```bash
# Pull latest code
git pull origin main

# Update dependencies
./scripts/deploy.sh deploy
```

### Maintenance Windows

- **Weekly**: System updates and security patches
- **Monthly**: Dependency updates and performance tuning
- **Quarterly**: Major version updates and feature releases

### Change Management

1. **Staging**: Test in staging environment first
2. **Backup**: Create backup before changes
3. **Deploy**: Use automated deployment script
4. **Monitor**: Watch for issues after deployment
5. **Rollback**: Be prepared to rollback if needed

## ✅ Pre-Deployment Checklist

### Security

- [ ] Environment variables configured
- [ ] SSL certificates valid
- [ ] Firewall configured
- [ ] API keys secured
- [ ] Database passwords strong

### Performance

- [ ] Resource limits set
- [ ] Monitoring configured
- [ ] Backup strategy in place
- [ ] Log rotation configured
- [ ] Cache settings optimized

### Functionality

- [ ] All services healthy
- [ ] Database migrations run
- [ ] API endpoints responding
- [ ] Frontend loading properly
- [ ] Monitoring dashboards working

### Documentation

- [ ] Runbooks updated
- [ ] Contact information current
- [ ] Backup procedures documented
- [ ] Emergency procedures tested

---

**Note**: This deployment guide is for production environments. For development or testing, use the development Docker Compose configuration.
